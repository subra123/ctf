
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
memory = [0] * 256
flag_len = 100
for i in range(flag_len):
    memory[i] = f"f{i}"

ip = 0
r1 = 0
r2 = 0

i = 0
while i < len(signals):
    sig = signals[i]
    i += 1
    if sig == 1: # SIGHUP - IP++
        ip += 1
    elif sig == 2: # SIGINT - IP--
        ip -= 1
    elif sig == 3: # SIGQUIT - R2 = memory[IP]
        r2 = memory[ip]
    elif sig == 4: # SIGILL - R1 = memory[IP]
        r1 = memory[ip]
    elif sig == 5: # SIGTRAP - R2 = 0
        r2 = 0
    elif sig == 7: # SIGBUS - memory[IP] = R2
        memory[ip] = r2
    elif sig == 13: # SIGPIPE - R2 ^= R1
        if isinstance(r2, str) or isinstance(r1, str):
            r2 = f"({r2} ^ {r1})"
        else:
            r2 ^= r1
    elif sig == 14: # SIGALRM - R2 |= R1
        if isinstance(r2, str) or isinstance(r1, str):
            r2 = f"({r2} | {r1})"
        else:
            r2 |= r1
    elif sig == 15: # PREFIX1 - R2 += imm
        next_sig = signals[i]
        i += 1
        imm = 0
        if next_sig == 1: imm = 1
        elif next_sig == 2: imm = 5
        elif next_sig == 3: imm = 10
        elif next_sig == 4: imm = 50
        elif next_sig == 5: imm = 100
        
        if isinstance(r2, str):
            r2 = f"({r2} + {imm})"
        else:
            r2 = (r2 + imm) & 0xFF
    elif sig == 17: # EXIT
        print("EXIT CHECK R2:", r2)
        break
    else:
        print("Unknown signal:", sig)

# Final state
# print("Final Memory:", memory[:flag_len])
