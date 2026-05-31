
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
    "53a300": 17,
    "53a308": 40,
    "53a310": 31,
    "53a318": 22,
    "53a320": 21,
    "53a328": 20,
    "53a330": 34,
    "53a338": 38,
    "53a340": 10
}

with open("signals_seq.txt") as f:
    addrs = [line.strip() for line in f if line.strip()]

signals = [mapping.get(addr, addr) for addr in addrs]
print(signals[:50])
