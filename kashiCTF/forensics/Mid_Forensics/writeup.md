# Mid Forensics - Writeup

## Challenge Description
A packet capture was collected from an internal network segment during routine monitoring. No alerts were triggered at the time, and the traffic appears largely normal. Your task is to analyze the capture and determine whether any meaningful information can be recovered. If so, extract it.

## Solution

### 1. Initial Analysis
I started by analyzing the protocol distribution in the `ttl_stego.pcap` file.

```bash
tshark -r ttl_stego.pcap -T fields -e frame.protocols | sort | uniq -c
```

Output:
```
266 ip:icmp
```
The capture contains 266 ICMP packets.

### 2. TTL Steganography Check
The name `ttl_stego.pcap` strongly suggested that information was hidden in the Time-To-Live (TTL) field. I extracted the TTL values using `tshark`.

```bash
tshark -r ttl_stego.pcap -T fields -e ip.ttl | sort | uniq -c
```

Output:
```
145 64
121 65
```
There are only two TTL values: 64 and 65. This indicates a binary encoding scheme where 64 = 0 and 65 = 1.

### 3. Data Extraction and Decoding
I wrote a script to extract all TTL values, convert them to binary (64 to 0, 65 to 1), and then group the binary bits into 8-bit blocks to decode them as ASCII characters.

```python
import sys

# Extract TTLs and convert to binary
lines = open('ttls.txt').read().splitlines()
binary = ''.join(['0' if l.strip()=='64' else '1' for l in lines])

# Decode 8-bit blocks to ASCII
result = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary)-7, 8))
print(result)
```

The decoded string revealed the flag:
`kashiCTF{ttl_stego_is_evil}`

## Flag
`kashiCTF{ttl_stego_is_evil}`
