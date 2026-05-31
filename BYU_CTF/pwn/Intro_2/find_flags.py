def memfrob(s):
    return "".join(chr(ord(c) ^ 42) for c in s)

import sys

with open("intro", "rb") as f:
    data = f.read()

# Try all sequences of printable characters (after frobbing)
import string
printable = set(string.printable.encode())

for i in range(len(data)):
    for length in range(10, 50):
        if i + length > len(data):
            break
        chunk = data[i:i+length]
        frobbed = bytes(b ^ 42 for b in chunk)
        if all(b in printable for b in frobbed):
            try:
                s = frobbed.decode()
                if "byuctf{" in s:
                    print(f"Found at {hex(i)}: {s}")
            except:
                pass
