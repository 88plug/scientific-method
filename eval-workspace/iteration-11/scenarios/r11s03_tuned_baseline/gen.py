import json,random
rng=random.Random(3)
with open("data.jsonl","w") as f:
    for i in range(400000): f.write(json.dumps({"id":i,"score":rng.randint(0,100)})+"\n")
print("ok")
