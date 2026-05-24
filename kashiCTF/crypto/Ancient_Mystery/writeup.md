## Writeup: Ancient Mystery (Cryptography)

This challenge blends historical flavor with a classic "Onion" encoding puzzle. Here is the breakdown of how the mystery was solved.

### 1. Challenge Analysis
The challenge description provides a historical narrative:
* **Timeline:** From 3136 BCE to 0 CE.
* **Duration:** 3136 years.
* **Encoding Frequency:** The message was re-encoded every **64 years**.

By doing a simple calculation:
$$\frac{3136 \text{ years}}{64 \text{ years/cycle}} = 49 \text{ cycles}$$

This suggests that the flag has been nested inside **49 layers** of encoding. Looking at the challenge title "Ancient Mystery" and the common patterns in CTF crypto challenges, "64" is a clear hint toward **Base64** encoding.

---

### 2. The Solution Strategy
Since the message is wrapped in 49 layers of Base64, manual decoding is out of the question. The solution involves writing a script to recursively decode the data until it no longer resembles Base64 or hits an error.

**The Script Logic (`decoder.py`):**
* **Read** the input from `secret_message.txt`.
* **Loop** the `base64.b64decode()` function.
* **Check** for valid characters and padding to ensure the loop breaks only when the actual flag is revealed.
* **Final Output:** Print the decoded string and the number of iterations performed.

---

### 3. Execution and Results
Running the script confirmed the mathematical hint:

```bash
subramanian@popos:~/ctf/kashiCTF/crypto/Ancient_Mystery$ python3 decoder.py
Decoded 49 times.
Length of final data: 45
Final data (repr):
b'flag{th3_s3cr3t_0f_mah4bh4r4t4_fr0m_3136_BCE}'
```

The script successfully peeled back exactly **49 layers** to reveal the flag.

---

### 4. Flag Adjustment
The challenge description included a specific instruction regarding the flag format:
> *Try changing the flag format to kashiCTF {...} before submitting*

The raw output from the script was `flag{th3_s3cr3t_0f_mah4bh4r4t4_fr0m_3136_BCE}`. Applying the required transformation gives us the final submission.

**Final Flag:**
`kashiCTF{th3_s3cr3t_0f_mah4bh4r4t4_fr0m_3136_BCE}`
