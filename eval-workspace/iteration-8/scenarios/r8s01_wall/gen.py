import json,random
random.seed(1)
with open("records.jsonl","w") as f:
    for i in range(300000):
        f.write(json.dumps({"ID":i,"Name":f"user{i%999}","Region":random.choice(["EU","US"]),"Score":i%100})+"\n")
print("ok")
