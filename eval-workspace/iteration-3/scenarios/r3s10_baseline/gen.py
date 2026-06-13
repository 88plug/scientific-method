with open("rows.csv","w") as f:
    for i in range(3_000_000): f.write(f"{i},x,{i%7}\n")
print("ok")
