# Easy Forensics - Writeup

## Challenge Description
A network capture was obtained from an internal monitoring system after suspicious activity was detected. The traffic appears mostly benign, but analysts believe data was covertly exfiltrated during normal communication. No obvious file transfers are present. Your task is to analyze the capture and recover the hidden secret.

**Flag Format:** `kashiCTF{...}`

## Solution

### 1. Protocol Analysis
I started by analyzing the protocol distribution in the provided `capture.pcap` file using `tshark`.

```bash
tshark -r capture.pcap -T fields -e frame.protocols | sort | uniq -c
```

Output:
```
105 ip:udp:dns
```
The capture consists entirely of DNS traffic.

### 2. DNS Query Inspection
Next, I examined the DNS query names to look for suspicious domains or encoded data.

```bash
tshark -r capture.pcap -T fields -e dns.qry.name | sort | uniq -c
```

Output:
```
      1 M63ENZZV6ZLY.exfil.internal
      1 MZUWY5DSMF2G.exfil.internal
      1 NNQXG2DJINKE.exfil.internal
      1 NZSWC23ZPU.exfil.internal
      1 S33OL5UXGX3T.exfil.internal
     66 amazon.com
     34 kashi.com
```

The subdomains of `exfil.internal` look like Base32 encoded data.

### 3. Data Extraction and Decoding
I extracted the subdomains in their chronological order:

1. `NNQXG2DJINKE`
2. `M63ENZZV6ZLY`
3. `MZUWY5DSMF2G`
4. `S33OL5UXGX3T`
5. `NZSWC23ZPU`

Concatenating these gives: `NNQXG2DJINKEM63ENZZV6ZLYMZUWY5DSMF2GS33OL5UXGX3TNZSWC23ZPU`

Decoding this string using Base32:

```bash
echo "NNQXG2DJINKEM63ENZZV6ZLYMZUWY5DSMF2GS33OL5UXGX3TNZSWC23ZPU======" | base32 -d
```

Output:
`kashiCTF{dns_exfiltration_is_sneaky}`

## Flag
`kashiCTF{dns_exfiltration_is_sneaky}`
