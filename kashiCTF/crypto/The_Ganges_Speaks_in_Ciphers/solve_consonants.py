import binascii

c = [
    "89f4f14325785a1837ba71e463c31fdb24e53448d9e11915fa33ecf3ccb5c9c5dfc6c905acafe674a29383d93fe6a133820edadcd720200caf891a",
    "a1cdcc3b0f18271b07ca46db18f42daa56c91d3df3c825239d4ec491ec86b4f1e6b7ae28978fd24093a6b4e35ce3a62eb605dad8b02d3119f1a197",
    "15656698abe9df82b661f064a7568950af74a9c35a6a8bce6cf7666d476c105f495b07c22f2d34be6d140e0ef054059d45f5637a12dacbe2381e70",
    "82e8f317373c450523e563a77acc168f73e2320c82f01558b86cf7e2dda4d8c7c9dc9619fca8eb31f7949a932ec39e11dd6eabd9a725341dbe5e2e",
    "a2e9f31f295a732933ed75b37aff019d62f9071b97b3132eff75e5e3e2bdcdcbc084a20fbcb4f8258dd983bc3fce8357cf39d0ea8210143082d096"
]
c_bytes = [binascii.unhexlify(x.strip()) for x in c]

def xor(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

# Consonants only: H Y V R L Ñ M NG NN N JH BH GH DDH DH J B G DD D KH PH CH TTH TH C TT T V K P Y SH SS S R H L
# ISCII: EF DF DC E2 EB E0 E1 E4 E3 D8 C8 CD E0 C9 CE CF E7 D1 D5 D2 DB DD B4 D5 B6 CE CF B7 D2 B3 DC B3 D4 DF E6 E7 ED E2 EF EB
consonants = bytes([0xEF, 0xDF, 0xDC, 0xE2, 0xEB, 0xE0, 0xE1, 0xE4, 0xE3, 0xD8, 0xC8, 0xCD, 0xE0, 0xC9, 0xCE, 0xCF, 0xE7, 0xD1, 0xD5, 0xD2, 0xDB, 0xDD, 0xB4, 0xD5, 0xB6, 0xCE, 0xCF, 0xB7, 0xD2, 0xB3, 0xDC, 0xB3, 0xD4, 0xDF, 0xE6, 0xE7, 0xED, 0xE2, 0xEF, 0xEB])

# Try all alignments
for start in range(len(consonants) - 30):
    length = 30
    K = xor(c_bytes[2][:length], consonants[start:start+length])
    p4 = xor(c_bytes[4][:length], K)
    if b"kashi" in p4.lower():
        print(f"Match at start {start}: {p4}")
