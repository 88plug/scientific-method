with open("nums.txt","w") as f:
    for i in range(8_000_000): f.write(f"{i%97}\n")
print("wrote nums.txt")
