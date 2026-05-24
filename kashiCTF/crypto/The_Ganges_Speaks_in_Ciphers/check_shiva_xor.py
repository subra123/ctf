import binascii

c0 = "89f4f14325785a1837ba71e463c31fdb24e53448d9e11915fa33ecf3ccb5c9c5dfc6c905acafe674a29383d93fe6a133820edadcd720200caf891a"
c2 = "15656698abe9df82b661f064a7568950af74a9c35a6a8bce6cf7666d476c105f495b07c22f2d34be6d140e0ef054059d45f5637a12dacbe2381e70"

c0_bytes = binascii.unhexlify(c0)
c2_bytes = binascii.unhexlify(c2)

def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

res = xor(c0_bytes, c2_bytes)
print(res.hex())
