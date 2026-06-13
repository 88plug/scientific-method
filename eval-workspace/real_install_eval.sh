#!/bin/bash
# Real-deployment eval: drive the INSTALLED v1.6.0 plugin via genuine `claude -p`
# from neutral /tmp sandboxes (no skill-file paths reachable). Measures real
# in-session triggering + saves outputs for grading vs existing ground truth.
set -u
WS=/home/andrew/scientific-method-plugin/eval-workspace
OUT=$WS/real-install-results
mkdir -p "$OUT"
PARSE='
import sys, json, collections
fired=False; tools=[]; res=None; text=[]
for line in sys.stdin:
    line=line.strip()
    if not line: continue
    try: d=json.loads(line)
    except: continue
    t=d.get("type")
    if t=="assistant":
        for b in d.get("message",{}).get("content",[]):
            if isinstance(b,dict):
                if b.get("type")=="tool_use":
                    tools.append(b.get("name"))
                    if b.get("name")=="Skill" and "scientific" in str(b.get("input",{})): fired=True
                if b.get("type")=="text": text.append(b.get("text",""))
    if t=="result": res=d.get("subtype") or "done"
print(json.dumps({"skill_fired":fired,"tools":dict(collections.Counter(tools)),"result":res,"final_text":(text[-1] if text else "")[:4000]}))
'
run_one () {
  local id="$1" src="$2" prompt="$3"
  local sb="/tmp/sm_re/$id"
  rm -rf "$sb"; mkdir -p "$sb"
  cp -r "$src"/. "$sb"/ 2>/dev/null
  # strip any file that names the skill/ground truth to keep it neutral
  rm -f "$sb"/VERDICT.md "$sb"/EXPERIMENTS.md 2>/dev/null
  echo "=== [$id] running real claude -p ===" >> "$OUT/progress.log"
  ( cd "$sb" && env -u CLAUDECODE timeout 420 claude -p "$prompt" \
      --model 'claude-fable-5[1m]' --output-format stream-json --verbose --add-dir "$sb" 2>/dev/null \
    | python3 -c "$PARSE" > "$OUT/$id.json" )
  echo "=== [$id] done: $(python3 -c "import json;d=json.load(open('$OUT/$id.json'));print('fired='+str(d['skill_fired']),'result='+str(d['result']))" 2>/dev/null) ===" >> "$OUT/progress.log"
}

# 5 stratified scenarios spanning the capability range; sandboxes reuse existing scenario inputs.
run_one s01_rootcause "$WS/iteration-1/scenarios/s01_redherring_deploy" \
  "Read the files here. svc-api crashed on 3 of 6 hosts right after the r1 deploy and the team wants to roll back tonight. Root cause this completely, no guessing."
run_one s02_restraint "$WS/iteration-2/scenarios/r2s03_weak_evidence" \
  "Read the files here. Assess whether the May 14 kernel update caused the sporadic 502s. We can't take prod down to bisect."
run_one s03_feedback "$WS/iteration-6/scenarios/r6s01_retry_storm" \
  "Read the files here. 25-minute brownout: incoming traffic was flat but total load hit 5x and every component met spec. The deploy is suspected. Root cause and propose the fix."
run_one s04_invention "$WS/iteration-9/scenarios/r9s04_retry_policy" \
  "Read BRIEF.md and sim.py here. Invent a client retry policy meeting all three acceptance criteria in the brief; measure it and report."
run_one s05_impossible "$WS/iteration-11/scenarios/r11s02_lowerbound" \
  "Read BRIEF.md here. Evaluate the vendor's claim with the strongest verdict you can support, with the proof shown."

echo "REAL_INSTALL_EVAL_COMPLETE" >> "$OUT/progress.log"
