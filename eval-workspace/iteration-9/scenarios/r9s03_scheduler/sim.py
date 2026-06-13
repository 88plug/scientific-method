"""Job scheduler sim. Jobs arrive (poisson-ish): 90% short (1-3 ticks),
10% long (20-60 ticks). One worker, preemption NOT allowed once started.
Baseline: shortest-job-first by declared length -> long jobs starve under load.
Plug in a scheduler: pick(queue, now) -> index into queue to start next.
Acceptance for an invention:
  - long-job p99 WAIT <= 400 ticks (baseline: >1500, many never run in-window)
  - short-job p50 wait <= 1.5x baseline's short-job p50
score(scheduler) prints both.
"""
import random
def gen_jobs(n=3000, seed=12):
    rng=random.Random(seed); jobs=[]; t=0
    for i in range(n):
        t += rng.choice([0,0,1])
        if rng.random()<0.9: jobs.append({"id":i,"arrive":t,"len":rng.randint(1,3)})
        else: jobs.append({"id":i,"arrive":t,"len":rng.randint(20,60)})
    return jobs
def baseline_pick(queue, now):
    return min(range(len(queue)), key=lambda i: queue[i]["len"])
def score(pick=baseline_pick):
    jobs=gen_jobs(); queue=[]; t=0; i=0; running=None; done=[]
    while len(done)<len(jobs):
        while i<len(jobs) and jobs[i]["arrive"]<=t: queue.append(jobs[i]); i+=1
        if running and running["end"]<=t: done.append(running); running=None
        if not running and queue:
            k=pick(queue,t); j=queue.pop(k)
            running={"end":t+j["len"], **j, "wait":t-j["arrive"]}
        t+=1
    sw=sorted(d["wait"] for d in done if d["len"]<=3)
    lw=sorted(d["wait"] for d in done if d["len"]>3)
    return {"short_p50":sw[len(sw)//2],"long_p99":lw[int(len(lw)*0.99)]}
if __name__=='__main__': print("baseline:", score())
