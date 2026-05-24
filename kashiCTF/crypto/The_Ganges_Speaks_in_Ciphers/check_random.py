import random

target = bytes.fromhex("200100081e")

for seed in range(10000):
    random.seed(seed)
    r = random.getrandbits(59*8).to_bytes(59, 'big') # This might not be how randbytes works
    # randbytes(59) is better
    random.seed(seed)
    r0 = random.randbytes(5).hex()
    # But wait, randbytes is Python 3.9+
    # Let's use a more portable way
    random.seed(seed)
    r = bytes([random.randint(0, 255) for _ in range(5)])
    # Wait, maybe the seeds are 3 and 4?
    # Let's try XORing randbytes(seed3) and randbytes(seed4)
    pass

# Better:
import random

def get_rand(seed, n):
    random.seed(seed)
    return bytes([random.randint(0, 255) for _ in range(n)])

for s1 in range(10):
    for s2 in range(s1 + 1, 10):
        r1 = get_rand(s1, 5)
        r2 = get_rand(s2, 5)
        diff = bytes(a ^ b for a, b in zip(r1, r2))
        if diff.startswith(bytes.fromhex("200100081e")[:2]):
             print(f"Seeds {s1}, {s2} diff: {diff.hex()}")
