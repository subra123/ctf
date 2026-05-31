import time
from pwn import *

def measure_time(hmac_hex):
    r = remote('chals.cyberjousting.com', 1362, level='error')
    r.recvuntil(b'Encrypted data: ')
    c = r.recvline().strip().decode()
    r.recvuntil(b'Poly1305 authentication tag: ')
    t = r.recvline().strip().decode()
    r.recvuntil(b'HMAC tag: ')
    h = r.recvline().strip().decode()
    
    r.sendlineafter(b'>>> Enter a ciphertext to decrypt:', c.encode())
    r.sendlineafter(b'>>> Enter an IV for the message:', b"303132333435363738396162")
    r.sendlineafter(b'>>> Enter a Poly1305 authentication tag for the message:', t.encode())
    
    start = time.time()
    r.sendlineafter(b'>>> Enter an HMAC tag for the message:', hmac_hex.encode())
    r.recvline() # Wait for response
    end = time.time()
    r.close()
    return end - start

def solve():
    # Try different first bytes for HMAC
    for i in range(5):
        h_guess = format(i, '02x') + "0" * 62
        t = measure_time(h_guess)
        print(f"Guess {h_guess[:2]}: {t:.6f}s")

if __name__ == "__main__":
    solve()
