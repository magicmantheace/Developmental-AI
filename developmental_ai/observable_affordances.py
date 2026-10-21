"""Optional numeric observation/outcome learning across generated sandbox tasks.

No hidden action name is included in a feature or an agent decision. The
simulator's engineered two-number physical measurements encode a simple shared
feature-to-outcome rule; this is NOT causal discovery or real-world safety.
"""
from __future__ import annotations

import hashlib
import json
import random

SCHEMA = "developmental-ai.observable-affordance/v1"
MODEL_SCHEMA = "developmental-ai.numeric-outcome-memory/v1"
DOMAINS = ("collect", "route", "route-reversed")
MAX_SAMPLES = 1000


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",", ":"),allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def feature_check(feature):
    if (type(feature) is not list or len(feature)!=2 or
        any(type(v) is not int or not 0<=v<=8 for v in feature)):
        raise ValueError("invalid observed numeric features")
    return feature


def check(frame):
    if (type(frame) is not dict or set(frame)!={"schema","episode","tick",
        "budget","sensors","goal","actions","done"} or frame["schema"]!=SCHEMA
        or type(frame["episode"]) is not str or len(frame["episode"])!=64
        or any(c not in "0123456789abcdef" for c in frame["episode"])
        or type(frame["tick"]) is not int or type(frame["budget"]) is not int
        or not 0<=frame["tick"]<=frame["budget"]<=8
        or type(frame["goal"]) is not int or not 1<=frame["goal"]<=4
        or type(frame["done"]) is not bool
        or type(frame["sensors"]) is not list or len(frame["sensors"])!=2
        or any(type(v) is not int or v<0 or v>4 for v in frame["sensors"])
        or type(frame["actions"]) is not list or len(frame["actions"])>12
        or (frame["done"] and frame["actions"])):
        raise ValueError("invalid observable sandbox frame")
    seen=set()
    for row in frame["actions"]:
        if (type(row) is not dict or set(row)!={"id","features"} or
            type(row["id"]) is not str or len(row["id"])!=20 or
            not row["id"].startswith("a_") or
            any(c not in "0123456789abcdef" for c in row["id"][2:]) or
            row["id"] in seen):
            raise ValueError("invalid opaque action handle")
        seen.add(row["id"])
        feature_check(row["features"])
    return frame


class ObservableWorld:
    """Independent per-episode identifiers; observable physical measurements.

    Simulator sees the engineered rule. Learner never receives domain or rule.
    Actions of the three outcome kinds are sampled without replacement from
    the same 9x9 numeric lattice, ensuring a feasible but nontrivial task.
    """
    def __init__(self,seed,split,index,domain):
        if (type(seed) is not int or split not in ("train","test") or
            type(index) is not int or not 0<=index<100000 or domain not in DOMAINS):
            raise ValueError("invalid synthetic episode")
        self.episode=digest([SCHEMA,seed,split,index,domain])
        rng=random.Random(int(self.episode[:16],16))
        self.goal=3 if domain=="collect" else 4
        self.budget=6 if domain=="collect" else 7
        self.tick=0
        self.progress=0
        self.damage=0
        self.done=False
        self._domain=domain
        lattice=[(a,b) for a in range(9) for b in range(9)]
        progress=[pair for pair in lattice if pair[1]>=pair[0]+2]
        hazard=[pair for pair in lattice if pair[0]>=pair[1]+2]
        neutral=[pair for pair in lattice if abs(pair[0]-pair[1])<2]
        is_reversed=domain=="route-reversed"
        if is_reversed:progress,hazard=hazard,progress
        count=5 if domain=="collect" else 6
        chosen=(rng.sample(progress,count)+rng.sample(hazard,3 if domain=="collect" else 4)
                +rng.sample(neutral,2))
        rng.shuffle(chosen)
        names=[f"a_{rng.getrandbits(72):018x}" for _ in chosen]
        if len(set(names))!=len(names):
            raise RuntimeError("opaque handle collision")
        self._features=dict(zip(names,chosen))
        self._used=set()

    def frame(self):
        rows=[{"id":handle,"features":list(feature)} for handle,feature in self._features.items()
              if handle not in self._used] if not self.done else []
        return check({"schema":SCHEMA,"episode":self.episode,"tick":self.tick,
                      "budget":self.budget,"goal":self.goal,
                      "sensors":[self.progress,self.damage],"actions":rows,"done":self.done})

    def step(self,action,tick):
        if (self.done or type(tick) is not int or tick!=self.tick
            or type(action) is not str or action not in self._features
            or action in self._used):
            raise ValueError("invalid or stale simulated action")
        x,y=self._features[action]
        if self._domain=="route-reversed":x,y=y,x
        if y>=x+2:self.progress+=1
        elif x>=y+2:self.damage+=1
        self._used.add(action)
        self.tick+=1
        self.done=(self.damage>0 or self.progress>=self.goal or
                   self.tick>=self.budget or len(self._used)==len(self._features))
        return self.frame()

    def success(self):
        return self.progress>=self.goal and self.damage==0


def outcome(before,action,after):
    check(before);check(after)
    handles={row["id"]:row["features"] for row in before["actions"]}
    if (type(action) is not str or action not in handles or
        before["episode"]!=after["episode"] or
        after["tick"]!=before["tick"]+1 or
        after["budget"]!=before["budget"] or after["goal"]!=before["goal"] or
        (not after["done"] and set(r["id"] for r in after["actions"])!=set(handles)-{action})):
        raise ValueError("invalid public sensor transition")
    delta=[v-u for u,v in zip(before["sensors"],after["sensors"])]
    if (any(v not in (0,1) for v in delta) or sum(delta)>1 or
        (not after["done"] and not after["actions"])):
        raise ValueError("invalid public outcome change")
    return {"features":list(handles[action]),"progress":bool(delta[0]),
            "damage":bool(delta[1])}


class NumericOutcomeMemory:
    """Exact replayable public measurements, no action-name identities."""
    def __init__(self):
        self.examples=[]

    def add(self,event):
        if (type(event) is not dict or set(event)!={"features","progress","damage"}
            or type(event["progress"]) is not bool or type(event["damage"]) is not bool
            or (event["progress"] and event["damage"]) or
            len(self.examples)>=MAX_SAMPLES):
            raise ValueError("invalid or oversized observed training evidence")
        feature_check(event["features"])
        self.examples.append(json.loads(canonical(event)))

    def estimate(self,features):
        feature_check(features)
        if not self.examples:
            return {"progress":0.0,"damage":0.0,"evidence":0}
        neighbors=sorted(enumerate(self.examples),key=lambda item:(
            (features[0]-item[1]["features"][0])**2+
            (features[1]-item[1]["features"][1])**2,item[0]))[:5]
        # Five nearest examples with deterministic squared-distance tie break.
        return {"progress":sum(int(r["progress"]) for _,r in neighbors)/len(neighbors),
                "damage":sum(int(r["damage"]) for _,r in neighbors)/len(neighbors),
                "evidence":len(neighbors)}

    def choose(self,frame):
        check(frame)
        if frame["done"]:
            return None
        ranked=[]
        for row in frame["actions"]:
            prediction=self.estimate(row["features"])
            # Explicit, hand-authored loss asymmetry: avoid injury first.
            score=prediction["progress"]*3-prediction["damage"]*10
            ranked.append((-score,row["id"]))
        return min(ranked)[1] if ranked else None

    def record(self):
        if not self.examples:
            raise ValueError("untrained public outcome model")
        state={"schema":MODEL_SCHEMA,"events":self.examples}
        return {"state":json.loads(canonical(state)),"sha256":digest(state)}

    @classmethod
    def restore(cls,record):
        if (type(record) is not dict or set(record)!={"state","sha256"} or
            type(record["state"]) is not dict or
            record["sha256"]!=digest(record["state"])):
            raise ValueError("invalid evidence checkpoint integrity")
        state=record["state"]
        if (set(state)!={"schema","events"} or state["schema"]!=MODEL_SCHEMA or
            type(state["events"]) is not list or not 1<=len(state["events"])<=MAX_SAMPLES):
            raise ValueError("invalid public memory schema")
        memory=cls()
        for row in state["events"]:memory.add(row)
        if memory.record()!=record:
            raise ValueError("cannot replay numeric observation memory")
        return memory
