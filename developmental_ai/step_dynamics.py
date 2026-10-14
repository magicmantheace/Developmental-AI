"""Per-observation, local-only latent-state change monitoring and candidate learning.

A beacon initializes a *known ring topology*; subsequent positions, true physics
and regime labels are never observed. This is not a general world model.
Approved model snapshots are immutable. Novel evidence can be staged and fitted
into a **quarantined candidate**, never automatically promoted or executed.
"""
from __future__ import annotations

import hashlib
import json
import math
import sqlite3
from pathlib import Path

from developmental_ai.adaptive_dynamics import canonical, index_of, reading_index
from developmental_ai.online_dynamics import ModelBank, fit, score, validate_history


def catalogue(bank):
    """Verify all immutable bank entries and bind a stable fingerprint."""
    rows=bank.conn.execute("SELECT name FROM online_models ORDER BY name").fetchall()
    if not 1 <= len(rows) <= MAX_MODELS:
        raise ValueError("model bank size out of bounds")
    models={row[0]:bank.get(row[0]) for row in rows}
    return models,digest({"schema":"online-dynamics/v1", "seed":bank.seed,
                          "models":[(name,digest(model.counts)) for name,model in models.items()]})

SCHEMA = "step-dynamics/v1"
MAX_STEPS = 40
MAX_EVENTS = 4000
MAX_SAMPLES = 500
MAX_MODELS = 16


def digest(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()


def _finite(x):
    return type(x) in (int, float) and math.isfinite(x)


def _observation(model, n, alpha, command, odometry, landmark):
    """One forward-filter update; return observation log probability and posterior."""
    next_alpha = [0.0] * n
    motion = model.motion_probs(command)
    for origin, prior in enumerate(alpha):
        if not prior:
            continue
        for cls, delta in enumerate((command, 0, -command)):
            destination = (origin + delta) % n
            emission = (motion[cls] * model.odo_probs(delta)[index_of(odometry)]
                        * model.landmark_probs(n, destination)[reading_index(landmark)])
            next_alpha[destination] += prior * emission
    evidence = sum(next_alpha)
    if not math.isfinite(evidence) or evidence <= 0.0:
        raise ValueError("invalid predictive probability")
    return math.log(evidence), [v / evidence for v in next_alpha]


class StepDetector:
    """SQLite-persisted per-step filter; refuses a changed model catalogue."""

    def __init__(self, db, bank: ModelBank, *, window=24, confirmations=3,
                 min_steps=5, floor=-3.3, margin=0.12):
        if type(window) is not int or not 2 <= window <= 64:
            raise ValueError("window out of bounds")
        if type(confirmations) is not int or not 1 <= confirmations <= 10:
            raise ValueError("confirmations out of bounds")
        if type(min_steps) is not int or not 2 <= min_steps <= window:
            raise ValueError("min_steps out of bounds")
        if not _finite(floor) or floor >= 0 or not _finite(margin) or margin < 0:
            raise ValueError("invalid scoring thresholds")
        self.models, self.catalogue = catalogue(bank)
        self.seed = bank.seed
        self.config = {"window": window, "confirmations": confirmations,
                       "min_steps": min_steps, "floor": float(floor), "margin": float(margin)}
        path = Path(db)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path)
        try:
            self.conn.execute("CREATE TABLE IF NOT EXISTS step_state(id INTEGER PRIMARY KEY CHECK(id=1), body TEXT NOT NULL, checksum TEXT NOT NULL)")
            self.conn.execute("CREATE TABLE IF NOT EXISTS step_events(seq INTEGER PRIMARY KEY, body TEXT NOT NULL, checksum TEXT NOT NULL)")
            row = self.conn.execute("SELECT body,checksum FROM step_state WHERE id=1").fetchone()
            self.state = self._blank() if row is None else json.loads(row[0])
            if row is not None and digest(self.state) != row[1]:
                raise ValueError("corrupt step checkpoint")
            self._validate_state()
            if row is not None:
                self.events()  # read and verify complete chain, not just the tail
        except Exception:
            self.conn.close()
            raise

    def _blank(self):
        return {"schema": SCHEMA, "seed": self.seed, "catalogue": self.catalogue,
                "config": self.config, "seq": 0, "episode": 0, "running": False,
                "n": None, "initial": None, "steps": [], "alpha": {}, "scores": {}, "recent": {name: [] for name in self.models},
                "active": None, "pending": None, "streak": 0, "unknown_seen": False,
                "last_event": None}

    def _validate_state(self):
        s = self.state
        if (type(s) is not dict or set(s) != set(self._blank()) or s["schema"] != SCHEMA
            or s["seed"] != self.seed or s["catalogue"] != self.catalogue
            or s["config"] != self.config):
            raise ValueError("incompatible step checkpoint")
        if (type(s["seq"]) is not int or not 0 <= s["seq"] <= MAX_EVENTS
            or type(s["episode"]) is not int or s["episode"] < 0
            or type(s["running"]) is not bool or type(s["unknown_seen"]) is not bool
            or s["active"] not in (None, *self.models)
            or s["pending"] not in (None, "unknown", *self.models)
            or type(s["streak"]) is not int or not 0 <= s["streak"] <= self.config["confirmations"]):
            raise ValueError("invalid step state")
        if (set(s["recent"]) != set(self.models) or any(type(v) is not list or
            len(v) > self.config["window"] or any(not _finite(x) for x in v)
            for v in s["recent"].values())):
            raise ValueError("invalid retained score history")
        if s["running"]:
            history = {"n": s["n"], "initial": s["initial"], "observations": s["steps"]}
            if s["steps"]:
                validate_history(history)
            elif type(s["n"]) is not int or s["n"] not in (9,11) or type(s["initial"]) is not int or not 0 <= s["initial"] < s["n"]:
                raise ValueError("invalid initial state")
            if (set(s["alpha"]) != set(self.models) or set(s["scores"]) != set(self.models)
                or len(s["steps"]) > MAX_STEPS):
                raise ValueError("invalid model state")
            for name in self.models:
                alpha, scores = s["alpha"][name], s["scores"][name]
                if (type(alpha) is not list or len(alpha) != s["n"] or any(not _finite(x) or x < 0 for x in alpha)
                    or abs(sum(alpha)-1.0) > 1e-7 or type(scores) is not list
                    or len(scores) > self.config["window"] or any(not _finite(x) for x in scores)):
                    raise ValueError("invalid filter state")
        elif (s["n"] is not None or s["initial"] is not None or s["steps"] != [] or s["alpha"] != {} or s["scores"] != {}):
            raise ValueError("inconsistent inactive state")

    def _save_event(self, event, updated):
        if self.state["seq"] >= MAX_EVENTS:
            raise ValueError("step event limit reached")
        new = json.loads(canonical(updated))
        new["seq"] += 1
        record = {"schema": SCHEMA, "seq": new["seq"], "episode": new["episode"],
                  "previous": self.state["last_event"], "scope": "simulation-only", **event}
        new["last_event"] = digest(record)
        with self.conn:
            self.conn.execute("INSERT INTO step_events VALUES(?,?,?)", (new["seq"], canonical(record), digest(record)))
            self.conn.execute("INSERT OR REPLACE INTO step_state VALUES(1,?,?)", (canonical(new), digest(new)))
        self.state = new
        return record

    def begin(self, n, initial):
        if self.state["running"]:
            raise ValueError("finish current episode first")
        if type(n) is not int or n not in (9,11) or type(initial) is not int or not 0 <= initial < n:
            raise ValueError("invalid beacon")
        new = json.loads(canonical(self.state))
        new.update({"running": True, "episode": new["episode"]+1, "n": n, "initial": initial,
                    "steps": [], "alpha": {name: [float(p == initial) for p in range(n)] for name in self.models},
                    "scores": {name: list(new["recent"][name]) for name in self.models},
                    "pending": None, "streak": 0, "unknown_seen": False})
        return self._save_event({"kind": "begin", "n": n, "initial": initial}, new)

    def step(self, command, odometry, landmark):
        if not self.state["running"]:
            raise ValueError("start an episode first")
        if len(self.state["steps"]) >= MAX_STEPS:
            raise ValueError("episode step limit")
        # This rejects malformed sensor tokens before any state mutation.
        record = (command, odometry, landmark)
        validate_history({"n": self.state["n"], "initial": self.state["initial"], "observations": [record]})
        new = json.loads(canonical(self.state))
        new["steps"].append(record)
        likelihoods = {}
        for name, model in self.models.items():
            logp, alpha = _observation(model, new["n"], new["alpha"][name], command, odometry, landmark)
            new["alpha"][name] = alpha
            values = (new["scores"][name] + [logp])[-self.config["window"]:]
            new["scores"][name] = values
            likelihoods[name] = sum(values)/len(values)
        best = sorted(likelihoods, key=lambda name: (-likelihoods[name], name))
        lead = best[0]
        runner = likelihoods[best[1]] if len(best)>1 else -math.inf
        margin = likelihoods[lead] - runner
        enough = len(new["steps"]) >= self.config["min_steps"]
        proposed = ("unknown" if likelihoods[lead] < self.config["floor"] else
                    lead if margin >= self.config["margin"] else None) if enough else None
        if proposed is None:
            new["pending"], new["streak"] = None, 0
            status = "warming" if not enough else "uncertain"
        else:
            if proposed == new["pending"]:
                new["streak"] = min(self.config["confirmations"], new["streak"]+1)
            else:
                new["pending"], new["streak"] = proposed, 1
            status = "pending"
            if new["streak"] >= self.config["confirmations"]:
                if proposed == "unknown":
                    status, new["unknown_seen"] = "unknown", True
                elif proposed != new["active"]:
                    new["active"] = proposed
                    status = "switch"
                else:
                    status = "stable"
        return self._save_event({"kind": "observation", "step": len(new["steps"]),
                                 "scores": {k:round(v,6) for k,v in sorted(likelihoods.items())},
                                 "candidate": proposed, "active": new["active"],
                                 "status": status}, new)

    def finish(self, staging=None):
        """Complete the episode and optionally stage unfamiliar evidence for review."""
        if not self.state["running"] or not self.state["steps"]:
            raise ValueError("no completed observations")
        history = {"n": self.state["n"], "initial": self.state["initial"],
                   "observations": self.state["steps"]}
        staged = False
        if staging is not None and self.state["unknown_seen"]:
            # Stage first; if storage fails, the episode remains open/retryable.
            staging.add(history, catalogue=self.catalogue)
            staged = True
        new = json.loads(canonical(self.state))
        new.update({"running": False, "n": None, "initial": None, "steps": [],
                    "alpha": {}, "recent": json.loads(canonical(new["scores"])),
                    "scores": {}, "pending": None, "streak": 0, "unknown_seen": False})
        return self._save_event({"kind": "finish", "staged": staged, "active": new["active"]}, new)

    def events(self):
        rows=self.conn.execute("SELECT seq,body,checksum FROM step_events ORDER BY seq").fetchall()
        if len(rows) != self.state["seq"]:
            raise ValueError("missing step records")
        previous = None
        events=[]
        for i, (seq,body,checksum) in enumerate(rows,1):
            event=json.loads(body)
            if seq != i or digest(event) != checksum or event.get("previous") != previous or event.get("seq") != i:
                raise ValueError("tampered step records")
            previous=checksum
            events.append(event)
        if previous != self.state["last_event"]:
            raise ValueError("mismatched event checkpoint")
        return events

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self,*_):
        self.close()


class CandidateStore:
    """Unapproved, observational training data and candidate model. No auto-promote."""
    def __init__(self, db, seed, catalogue):
        if type(seed) is not int or type(catalogue) is not str or len(catalogue) != 64:
            raise ValueError("invalid candidate binding")
        self.seed, self.catalogue = seed, catalogue
        path=Path(db)
        path.parent.mkdir(parents=True,exist_ok=True)
        self.conn=sqlite3.connect(path)
        try:
            self.conn.execute("CREATE TABLE IF NOT EXISTS candidate_meta(id INTEGER PRIMARY KEY CHECK(id=1), seed INTEGER, catalogue TEXT, schema TEXT)")
            self.conn.execute("CREATE TABLE IF NOT EXISTS candidate_history(hash TEXT PRIMARY KEY, body TEXT NOT NULL)")
            self.conn.execute("CREATE TABLE IF NOT EXISTS candidate_model(id INTEGER PRIMARY KEY CHECK(id=1), body TEXT NOT NULL, digest TEXT NOT NULL, samples INTEGER NOT NULL)")
            meta=self.conn.execute("SELECT seed,catalogue,schema FROM candidate_meta WHERE id=1").fetchone()
            if meta is None:
                with self.conn:
                    self.conn.execute("INSERT INTO candidate_meta VALUES (1,?,?,?)",(seed,catalogue,SCHEMA))
            elif meta != (seed,catalogue,SCHEMA):
                raise ValueError("candidate store tied to another model bank")
            self.histories()  # validate persisted provenance and payload digests
            self.get_candidate(optional=True)
        except Exception:
            self.conn.close()
            raise

    def add(self, history, *, catalogue):
        if catalogue != self.catalogue:
            raise ValueError("untrusted model catalogue")
        validate_history(history)
        if self.get_candidate(optional=True) is not None:
            raise ValueError("candidate evidence frozen after proposal")
        record=json.loads(canonical(history))
        key=digest(record)
        with self.conn:
            if self.conn.execute("SELECT COUNT(*) FROM candidate_history").fetchone()[0] >= MAX_SAMPLES:
                raise ValueError("candidate evidence limit")
            self.conn.execute("INSERT OR IGNORE INTO candidate_history VALUES(?,?)",(key,canonical(record)))
        return key

    def histories(self):
        rows=self.conn.execute("SELECT hash,body FROM candidate_history ORDER BY hash").fetchall()
        if len(rows) > MAX_SAMPLES:
            raise ValueError("too much evidence")
        histories=[]
        for key,body in rows:
            record=json.loads(body)
            if digest(record) != key:
                raise ValueError("tampered candidate evidence")
            validate_history(record)
            histories.append(record)
        return histories

    def propose(self, *, min_histories=12, iterations=7):
        if type(min_histories) is not int or not 4 <= min_histories <= MAX_SAMPLES:
            raise ValueError("invalid sample threshold")
        histories=self.histories()
        if len(histories)<min_histories:
            raise ValueError("not enough unfamiliar observations")
        if self.get_candidate(optional=True) is not None:
            raise ValueError("candidate already frozen; start new review cycle")
        model, curve=fit(histories, iterations=iterations)
        body=canonical(model.counts)
        d=hashlib.sha256(body.encode()).hexdigest()
        with self.conn:
            self.conn.execute("INSERT INTO candidate_model VALUES(1,?,?,?)",(body,d,len(histories)))
        return {"schema":SCHEMA,"status":"awaiting-human-review", "model_digest":d,
                "histories":len(histories),"fit_log_likelihood_curve":curve}

    def get_candidate(self, optional=False):
        row=self.conn.execute("SELECT body,digest,samples FROM candidate_model WHERE id=1").fetchone()
        if row is None:
            if optional:
                return None
            raise ValueError("no reviewed candidate available")
        body,d,samples=row
        if hashlib.sha256(body.encode()).hexdigest()!=d or type(samples) is not int or samples<4:
            raise ValueError("tampered candidate model")
        from developmental_ai.adaptive_dynamics import DynamicsModel
        model=DynamicsModel(json.loads(body))
        model.validate()
        return model,d

    def promote(self, bank: ModelBank, name, *, approval_digest=None):
        """Explicit local approval; never invoked by detector, learning, or CLI."""
        if bank.seed != self.seed:
            raise ValueError("seed mismatch")
        _, bank_hash = catalogue(bank)
        if bank_hash != self.catalogue:
            raise ValueError("bank changed during candidate review")
        model, d=self.get_candidate()
        frozen_samples=self.conn.execute("SELECT samples FROM candidate_model WHERE id=1").fetchone()[0]
        if frozen_samples != len(self.histories()):
            raise ValueError("candidate evidence changed during review")
        if approval_digest != d:
            raise PermissionError("explicit digest-matched review approval required")
        ModelBank._check_name(name)
        return bank.save(name,model,len(self.histories()))

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self,*_):
        self.close()
