# heap2win - BYU CTF Writeup

## Challenge Description
The challenge provides a C++ binary `heap2win` and its source code `main.cpp`. The goal is to trigger the `WinnerButton::push()` method, which calls `system("/bin/sh")`, but the application prevents you from creating a `WinnerButton` directly.

## Vulnerability Analysis

### 1. The Buffer Overflow
In the `CustomButton` class, the constructor uses `scanf` with a `%s` format string to read the button's name:

```cpp
class CustomButton : public Button {
    public:
        CustomButton() {
            cout << "Enter the name for your custom button!" << endl;
            scanf("%s", name); // <--- VULNERABILITY: No bounds checking
        }
    // ...
    private:
        char name[0x10]; // 16 bytes
};
```

This allows for a heap-based buffer overflow, as `scanf("%s", ...)` will read until it hits whitespace, regardless of the target buffer size.

### 2. C++ Objects and Vtables
C++ classes with virtual functions (like the `Button` hierarchy here) use a **vtable pointer (vptr)**. This pointer is the first 8 bytes of the object on the heap (on 64-bit systems). It points to a table of function pointers (the vtable) used to resolve virtual function calls at runtime.

The goal is to overwrite the `vptr` of an existing button object to point to the `WinnerButton` vtable.

### 3. Binary Protections
Running `checksec` revealed:
- **PIE**: Disabled (Fixed addresses for vtables)
- **NX**: Enabled (Stack/Heap not executable)
- **RELRO**: Full

Since PIE is disabled, we can find the exact address of the `WinnerButton` vtable in the binary:
`0x403630` is the start of the `WinnerButton` vtable entry. Specifically, the pointer to the `push` function is at `0x403640` (vtable + 16 bytes, accounting for the RTTI offset).

## Exploitation Strategy

### Heap Layout Manipulation
The `Application` class stores buttons in a `std::vector<Button*>`.
```cpp
vector<Button*> button_list;
```
When we create buttons, the objects themselves are allocated on the heap, and pointers to them are stored in the vector's internal buffer.

To exploit the overflow:
1. **Allocate HypeButton 1 & 2**: This populates the heap.
2. **Allocate CustomButton**: Due to how `std::vector` and the heap allocator work, a `CustomButton` can be placed such that its `name` buffer is immediately followed by the `vptr` of another button.

In this specific binary, creating two `HypeButton`s and then a `CustomButton` results in the following heap layout:
- `CustomButton` object at `P`
  - `+0x00`: `vptr` (8 bytes)
  - `+0x10`: `name` buffer (16 bytes)
- `HypeButton 2` object at `P + 0x20`
  - `+0x00`: `vptr` (8 bytes)

### The Overflow
By providing a name longer than 16 bytes to the `CustomButton`, we can reach and overwrite the `vptr` of `HypeButton 2`.
- Padding: 16 bytes (name buffer) + 8 bytes (internal alignment/padding) = **24 bytes**.
- Overwrite: **Address of WinnerButton vtable** (`0x403640`).

### Execution
Once `HypeButton 2`'s `vptr` is overwritten, choosing option **2 (Push a button)** and selecting button **2** will call `button_list[1]->push()`. Instead of executing `HypeButton::push()`, the CPU will jump to `WinnerButton::push()`, giving us a shell.

## Exploit Script (Summary)
```python
from pwn import *

vptr_winner = 0x403640
payload = b"A" * 24 + p64(vptr_winner)

# 1. Create Hype Button
# 2. Create Hype Button
# 3. Create Custom Button with payload
# 4. Push Button 2
```

## Flag
`byuctf{y34h,..._you're_a_pro}`
