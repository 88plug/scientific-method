with open("recs.csv","wb") as f:
    for i in range(1_500_000): f.write(f"{i%97},{i%89},{i%83},pad{i%7}\n".encode())
print("ok")
