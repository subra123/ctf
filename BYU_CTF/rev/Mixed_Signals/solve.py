
mapping = {
    "53a2b8": 1,
    "53a2c0": 4,
    "53a2c8": 5,
    "53a2d0": 15,
    "53a2d8": 3,
    "53a2e0": 13,
    "53a2e8": 7,
    "53a2f0": 14,
    "53a2f8": 2,
    "53a300": 17
}

with open("signals_seq.txt") as f:
    addrs = [line.strip() for line in f if line.strip()]

signals = [mapping[addr] for addr in addrs]

# VM state
memory = [f"f{i}" for i in range(256)]
ip = 0
r1 = 0
r2 = 0

i = 0
while i < len(signals):
    sig = signals[i]
    i += 1
    if sig == 1: ip += 1
    elif sig == 2: ip -= 1
    elif sig == 3: r2 = memory[ip]
    elif sig == 4: r1 = memory[ip]
    elif sig == 5: r2 = 0
    elif sig == 7: memory[ip] = r2
    elif sig == 13:
        if isinstance(r2, str) and isinstance(r1, str):
            r2 = f"({r2} ^ {r1})"
        elif isinstance(r2, str):
            r2 = f"({r2} ^ {r1})"
        elif isinstance(r1, str):
            r2 = f"({r1} ^ {r2})"
        else:
            r2 ^= r1
    elif sig == 14:
        if isinstance(r2, str) and isinstance(r1, str):
            r2 = f"({r2} | {r1})"
        elif isinstance(r2, str):
            r2 = f"({r2} | {r1})"
        elif isinstance(r1, str):
            r2 = f"({r1} | {r2})"
        else:
            r2 |= r1
    elif sig == 15:
        next_sig = signals[i]
        i += 1
        imm = {1:1, 2:5, 3:10, 4:50, 5:100}[next_sig]
        if isinstance(r2, str):
            r2 = f"({r2} + {imm})"
        else:
            r2 = (r2 + imm) & 0xFF
    elif sig == 17:
        print("FINAL CHECK:", r2)
        break
