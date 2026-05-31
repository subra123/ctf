# Writeup: Mixed Signals (BYU CTF - Rev)

## Challenge Description
The challenge consists of two binaries: `program` and `mixed_signals`. The goal is to find the flag by understanding how these two programs interact.

## How the Challenge Works
1.  **Dual-Process Interaction:** `mixed_signals` is the main process that takes the flag as a command-line argument. `program` is a controller process.
2.  **Signal-Based Virtual Machine:** 
    - `mixed_signals` sets up a listener for various Linux signals (SIGHUP, SIGINT, etc.).
    - Each signal acts as an **opcode** for a custom 8-bit Virtual Machine.
    - The VM has two registers (`R1`, `R2`), an Instruction Pointer (`IP`) which indexes into the flag memory, and a 256-byte memory space initialized with the input flag.
3.  **The "Program" Execution:**
    - The `program` binary finds the PID of `mixed_signals`.
    - it sends a hardcoded sequence of ~1,800 signals to `mixed_signals`.
    - This sequence performs complex arithmetic (XORs, Additions) on the flag characters.
    - The final result of all checks is `OR`-ed into `R2`.
    - If `R2` is `0` at the end, the flag is correct.

## Step-by-Step Solution

### 1. Extracting the Signal Sequence
We disassembled `program` to find the sequence of signal calls in `main.run_program`.
```bash
objdump -M intel -d program > program.disasm
sed -n '/<main.run_program>:/,/^$/p' program.disasm | grep "lea    rcx.*# 53a" | sed 's/.*# \(53a[0-9a-f]*\).*/\1/' > signals_seq.txt
```

### 2. Mapping Addresses to Signals
Using `gdb`, we identified which memory addresses in `program` mapped to which signal numbers.
```bash
gdb -batch -ex "x/10gx 0x53a2b8" program
```
Mapping:
- `53a2b8` -> Signal 1 (SIGHUP)
- `53a2c0` -> Signal 4 (SIGILL)
- `53a2c8` -> Signal 5 (SIGTRAP)
- `53a2d0` -> Signal 15 (SIGTERM)
- ... (and so on)

### 3. Reversing VM Opcodes
By disassembling `mixed_signals`, we mapped signal handlers to operations:
- **Signal 1:** `IP++`
- **Signal 2:** `IP--`
- **Signal 3:** `R2 = Memory[IP]`
- **Signal 4:** `R1 = Memory[IP]`
- **Signal 5:** `R2 = 0`
- **Signal 7:** `Memory[IP] = R2`
- **Signal 13:** `R2 ^= R1`
- **Signal 14:** `R2 |= R1`
- **Signal 15:** Prefix for immediate addition (e.g., `15 then 5` -> `R2 += 100`)
- **Signal 17:** Exit and check result.

### 4. Solving with Z3
We used the **Z3 SMT solver** to simulate the 1,800 instructions and solve for the flag bytes that result in `R2 == 0`.

```bash
python3 solve_z3.py
```

**Flag:** `byuctf{l3ft_bl1nk3r_5c9125be}`

## Files in Directory
- `mixed_signals`: Statically linked Go binary (The VM).
- `program`: Dynamically linked Go binary (The Controller).
- `program.disasm`: Disassembly of the controller.
- `mixed_signals.disasm`: Disassembly of the VM.
- `signals_seq.txt`: Extracted sequence of signal addresses.
- `decode_signals.py`: Helper script to map addresses to signal numbers.
- `simulate_vm_v2.py`: Initial symbolic execution script.
- `solve_z3.py`: The final Z3 script that recovered the flag.
- `writeup.md`: This file.
