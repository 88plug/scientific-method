import sys
with open("input.txt","w") as f:
    for i in range(2_000_000): f.write(f"record-{i:07d} payload {"x"*40}\n")
print("wrote input.txt")
