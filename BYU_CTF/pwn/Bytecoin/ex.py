from pwn import *
import re

r = remote('chals.cyberjousting.com', 1362)

banner = r.recvuntil(b'>>> Enter a ciphertext to decrypt:\n').decode()
print(banner)

# Fix: escape the brackets so [+] is treated as literal
ct   = re.search(r'\[\+\] Encrypted data: ([0-9a-f]+)', banner).group(1)
poly = re.search(r'\[\+\] Poly1305 authentication tag: ([0-9a-f]+)', banner).group(1)
hmac = re.search(r'\[\+\] HMAC tag: ([0-9a-f]+)', banner).group(1)

print(f"CT:   {ct}")
print(f"Poly: {poly}")
print(f"HMAC: {hmac}")

IV = '303132333435363738396162'

r.sendline(ct.encode())
r.recvuntil(b'>>> Enter an IV for the message:\n')
r.sendline(IV.encode())
r.recvuntil(b'>>> Enter a Poly1305 authentication tag for the message:\n')
r.sendline(poly.encode())
r.recvuntil(b'>>> Enter an HMAC tag for the message:\n')
r.sendline(hmac.encode())

result = r.recvall(timeout=5)
print(result.decode())

flag_hex = re.search(r'message:\s*([0-9a-f]+)', result.decode())
if flag_hex:
    print("FLAG:", bytes.fromhex(flag_hex.group(1)).decode(errors='replace'))
