
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
# We don't know the flag, so we'll use symbols
flag_len = 50 # Guessing
for i in range(flag_len):
    memory[i] = f"f{i}"

ip = 0
r1 = 0
r2 = 0

i = 0
while i < len(signals):
    sig = signals[i]
    i += 1
    if sig == 1: # SIGHUP
        ip += 1
    elif sig == 2: # SIGINT
        ip -= 1
    elif sig == 3: # SIGQUIT
        r2 = memory[ip]
    elif sig == 4: # SIGILL
        r1 = memory[ip]
    elif sig == 5: # SIGTRAP
        r2 = 0
    elif sig == 7: # SIGBUS
        memory[ip] = r2
    elif sig == 13: # SIGPIPE
        if isinstance(r2, str) or isinstance(r1, str):
            r2 = f"({r2} ^ {r1})"
        else:
            r2 ^= r1
    elif sig == 15: # PREFIX1
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
            r2 += imm
    elif sig == 17: # EXIT
        print("EXIT CHECK:", r2)
        break
    else:
        print("Unknown signal:", sig)

print("Final R2:", r2)
