# Conquer - KashiCTF Writeup

## Challenge Description
- **Name:** Conquer
- **Points:** 488
- **Category:** Steganography
- **Description:** "I like to save my files as pdfs. Kashi kings hate 184"

## Initial Analysis
We are provided with several files:
- `flag.pdf`
- `flag.png`
- `xored_flag.jpg`
- `xored_flag.png`
- `xored_flag.ppm`

The first step was to identify the actual file types using the `file` command:
```bash
file *
```
Interestingly, `flag.pdf` was identified as **Netpbm image data (PPM)**, not a PDF.

## Investigation
Inspecting the header of `flag.pdf` (which is actually a PPM file):
```bash
head -c 50 flag.pdf
```
Output:
```
P6
284 150
255
...
```
The dimensions were set to `284 x 150`. 

### File Relationships and XOR Analysis
The challenge provided several versions of the same image. By comparing the raw bytes of `flag.pdf` and `xored_flag.ppm`, we found a direct XOR relationship:
- **`flag.pdf` byte 15:** `0xff`
- **`xored_flag.ppm` byte 15:** `0x47` ('G')
- **Calculation:** `0xff ^ 184 = 0x47` (71 in decimal)

The hint **"Kashi kings hate 184"** confirmed that **184** was the XOR key used to transform the original image data into the `xored_flag` versions.

### The Hidden Data (Truncation)
Checking the file size of `flag.pdf`:
- Size: 157,635 bytes.
- Header size: ~15 bytes.
- If dimensions are 284x150, expected pixel data size (3 bytes per pixel for P6): `284 * 150 * 3 = 127,800` bytes.
- Total expected size: `127,800 + header ≈ 127,815` bytes.
- Actual size: `157,635` bytes.
- Extra data: `157,635 - 127,815 = 29,820` bytes.

The extra data `29,820 / (284 * 3) = 35` rows.
This means the actual height of the image was `150 + 35 = 185` pixels, but the header was intentionally truncated to hide the flag.

## Exploitation
To reveal the flag, the height in the PPM headers needed to be corrected.

1. **For the original image (`flag.pdf`):**
```bash
sed -i 's/284 150/284 185/' flag.pdf
convert flag.pdf revealed_flag.png
```

2. **For the XORed image (`xored_flag.ppm`):**
```bash
sed -i 's/284 150/284 185/' xored_flag.ppm
convert xored_flag.ppm revealed_xored_flag.png
```

While `flag.png` was a standard conversion of the truncated source, the full data was always present in the PPM/PDF source files. Fixing the height to 185 revealed the hidden 35 rows at the bottom of the image.

## Flag Extraction
Opening `revealed_flag.png` showed a new section at the bottom containing the flag in clear text.

**Flag:** `kashiCTF{iLOVEkashi}`
