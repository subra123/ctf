import binascii

c4 = "a2e9f31f295a732933ed75b37aff019d62f9071b97b3132eff75e5e3e2bdcdcbc084a20fbcb4f8258dd983bc3fce8357cf39d0ea8210143082d096"
c4_bytes = binascii.unhexlify(c4)

flag = b"kashiCTF{g4ng4_sh1v4_v4r4n4s1}"

def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

res = xor(c4_bytes, flag)
print(res.hex())
