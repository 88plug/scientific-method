# regenerates words.txt — run once before bench.sh
import random
random.seed(42)
words = ['quark','quill','zebra','apple','quest','melon','query','grape']
with open("words.txt", "w") as f:
    for _ in range(400000):
        f.write(random.choice(words) + str(random.randint(0, 999)) + "\n")
print("wrote words.txt (400k lines)")
