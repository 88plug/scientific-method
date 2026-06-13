"""Single FIFO worker queue shared by interactive (p99 target 50ms) and
batch jobs (each 200-800ms of work). Mixed load: 50 interactive/s (1-5ms
each), 2 batch/s. Baseline FIFO: interactive p99 blows past 50ms (head-of-
line blocking behind batch). Non-preemptive once started; you control
enqueue/dequeue policy (and may use multiple logical queues / admission).
Acceptance:
  - interactive p99 <= 50ms
  - batch throughput >= 80% of FIFO baseline's batch throughput
score(policy) -> dict. policy.dequeue(queues, now) picks next job.
"""
import random
def gen(seed=18, seconds=60):
    rng=random.Random(seed); jobs=[]
    for ms in range(seconds*1000):
        if rng.random()<0.05: jobs.append({"t":ms,"kind":"int","len":rng.randint(1,5)})
        if rng.random()<0.002: jobs.append({"t":ms,"kind":"batch","len":rng.randint(200,800)})
    return jobs
class FIFO:
    def enqueue(self,q,job): q.setdefault("all",[]).append(job)
    def dequeue(self,q,now):
        return ("all",0) if q.get("all") else None
def score(policy):
    jobs=gen(); q={}; i=0; now=0; busy_until=0; done=[]
    while i<len(jobs) or any(q.values()):
        if i<len(jobs) and jobs[i]["t"]<=now:
            policy.enqueue(q,jobs[i]); i+=1; continue
        if now>=busy_until:
            pick=policy.dequeue(q,now)
            if pick:
                name,idx=pick; j=q[name].pop(idx)
                done.append({**j,"wait":now-j["t"]})
                busy_until=now+j["len"]
        now+=1
    iw=sorted(d["wait"]+d["len"] for d in done if d["kind"]=="int")
    bdone=len([d for d in done if d["kind"]=="batch"])
    return {"interactive_p99_ms":iw[int(len(iw)*0.99)],"batch_done":bdone}
if __name__=='__main__': print("baseline:",score(FIFO()))
