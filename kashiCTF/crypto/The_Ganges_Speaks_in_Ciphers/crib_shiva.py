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

# Shiva Sutras ISCII (partial)
# 1. a i u nn (A4 A2 D2 B1) - Wait, I need a better mapping
# Let's use the ones I found:
# KA: B3, PA: D4, YA: DF, SHA: E6, SSA: E7, SA: ED, RA: E2, HA: EF, LA: EB, VA: DC
# Verse 12: KA PA YA -> B3 D4 DF
# Verse 13: SHA SSA SA RA -> E6 E7 ED E2
# Verse 14: HA LA -> EF EB

shiva_iscII = bytes([0xB3, 0xD4, 0xDF, 0xE6, 0xE7, 0xED, 0xE2, 0xEF, 0xEB])

for i in range(5):
    for pos in range(len(c_bytes[i]) - len(shiva_iscII) + 1):
        key_part = xor(c_bytes[i][pos:pos+len(shiva_iscII)], shiva_iscII)
        
        matches = 0
        for j in range(5):
            if i == j: continue
            p_j = xor(c_bytes[j][pos:pos+len(shiva_iscII)], key_part)
            if all(32 <= c <= 126 for c in p_j):
                matches += 1
        
        if matches >= 2:
            print(f"Pos {pos}, p{i} matches Shiva Sutras:")
            for j in range(5):
                p_j = xor(c_bytes[j][pos:pos+len(shiva_iscII)], key_part)
                print(f"  p{j}: {p_j}")
