import binascii

c_files = ["c0.hex", "c1.hex", "c2.hex", "c3.hex", "c4.hex"]
c = [
    "89f4f14325785a1837ba71e463c31fdb24e53448d9e11915fa33ecf3ccb5c9c5dfc6c905acafe674a29383d93fe6a133820edadcd720200caf891a",
    "a1cdcc3b0f18271b07ca46db18f42daa56c91d3df3c825239d4ec491ec86b4f1e6b7ae28978fd24093a6b4e35ce3a62eb605dad8b02d3119f1a197",
    "15656698abe9df82b661f064a7568950af74a9c35a6a8bce6cf7666d476c105f495b07c22f2d34be6d140e0ef054059d45f5637a12dacbe2381e70",
    "82e8f317373c450523e563a77acc168f73e2320c82f01558b86cf7e2dda4d8c7c9dc9619fca8eb31f7949a932ec39e11dd6eabd9a725341dbe5e2e",
    "a2e9f31f295a732933ed75b37aff019d62f9071b97b3132eff75e5e3e2bdcdcbc084a20fbcb4f8258dd983bc3fce8357cf39d0ea8210143082d096"
]
c_bytes = [binascii.unhexlify(x) for x in c]

def xor_key(data, key):
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

for i, cb in enumerate(c_bytes):
    res = xor_key(cb, c_files[i].encode())
    print(f"{c_files[i]} ^ filename: {res.hex()[:20]}...")

# Try XORing pairs after removing filename
for i in range(len(c_bytes)):
    for j in range(i + 1, len(c_bytes)):
        b1 = xor_key(c_bytes[i], c_files[i].encode())
        b2 = xor_key(c_bytes[j], c_files[j].encode())
        diff = bytes(a ^ b for a, b in zip(b1, b2))
        print(f"XOR {c_files[i]} ^ {c_files[j]} (no filename): {diff.hex()[:20]}...")
