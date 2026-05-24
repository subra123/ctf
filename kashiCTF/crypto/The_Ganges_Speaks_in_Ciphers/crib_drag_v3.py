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

def is_plausible(b):
    # Allow ASCII and ISCII (top bit set)
    return all(32 <= c <= 126 or c >= 0xA0 or c == 0 for c in b)

cribs = [b"kashiCTF{", b"Hello ", b"Ganga ", b"Varanasi ", b"Kashi "]

for i in range(5):
    for pos in range(len(c_bytes[i]) - 10):
        for crib in cribs:
            if pos + len(crib) > len(c_bytes[i]): continue
            
            # Try key_part = c_i ^ crib
            key_part = xor(c_bytes[i][pos:pos+len(crib)], crib)
            
            matches = []
            for j in range(5):
                p_j = xor(c_bytes[j][pos:pos+len(crib)], key_part)
                # Try also with 0x20 flip
                p_j_flip = bytes(c ^ 0x20 for c in p_j)
                
                if is_plausible(p_j):
                    matches.append((j, p_j, False))
                elif is_plausible(p_j_flip):
                    matches.append((j, p_j_flip, True))
            
            if len(matches) >= 4:
                print(f"Pos {pos}, p{i} starts with {crib}:")
                for j, pj, flip in matches:
                    print(f"  p{j}: {pj} {'(flipped)' if flip else ''}")
