
import z3

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
flag_len = 100 # Large enough
flag = [z3.BitVec(f"f{i}", 8) for i in range(flag_len)]
memory = [z3.BitVecVal(0, 8) for _ in range(256)]
for i in range(flag_len):
    memory[i] = flag[i]

ip = 0
r1 = z3.BitVecVal(0, 8)
r2 = z3.BitVecVal(0, 8)

i = 0
while i < len(signals):
    sig = signals[i]
    i += 1
    if sig == 1: ip += 1
    elif sig == 2: ip -= 1
    elif sig == 3: r2 = memory[ip]
    elif sig == 4: r1 = memory[ip]
    elif sig == 5: r2 = z3.BitVecVal(0, 8)
    elif sig == 7: memory[ip] = r2
    elif sig == 13: r2 ^= r1
    elif sig == 14: r2 |= r1
    elif sig == 15:
        next_sig = signals[i]
        i += 1
        imm = {1:1, 2:5, 3:10, 4:50, 5:100}[next_sig]
        r2 += imm
    elif sig == 17:
        break

s = z3.Solver()
s.add(r2 == 0)

# Add constraints for printable characters and flag format if known
# byuctf{...}
s.add(flag[0] == ord('b'))
s.add(flag[1] == ord('y'))
s.add(flag[2] == ord('u'))
s.add(flag[3] == ord('c'))
s.add(flag[4] == ord('t'))
s.add(flag[5] == ord('f'))
s.add(flag[6] == ord('{'))

if s.check() == z3.sat:
    m = s.model()
    res = []
    for i in range(flag_len):
        v = m[flag[i]]
        if v is not None:
            res.append(chr(v.as_long()))
        else:
            res.append('?')
    print("".join(res))
else:
    print("UNSAT")
