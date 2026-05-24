Nice work! The reason `curl` worked while your manual copy-paste failed is a common trap in CTFs: browsers and text editors often "beautify" or normalize text, converting **Tabs** into **Spaces**, which destroys the hidden binary message.

Here is a formal writeup for the challenge.

---

# Writeup: POEM (Steganography)

## Challenge Description
The challenge provides a link to a webpage displaying the poem "Dust of Snow" by Robert Frost. The hint mentions: *"I like to have my poems saved on CTFd instances like this. But the admin doesn't like it, so I hid the secret in my poem."*

## 1. Initial Analysis
Upon visiting the URL, the poem appears normal. However, selecting the text with a cursor reveals an unusual amount of empty space at the end of each line. This is a hallmark of **Whitespace Steganography**.

## 2. Technical Observation
Using `curl` to inspect the raw source code of the page confirms that the trailing whitespace consists of a specific sequence of **Spaces** and **Tabs**. 

In Steganography, this technique is often associated with the **SNOW** (Steganographic Nature of Whitespace) algorithm, which conceals data by appending whitespace to the end of lines in a text file.

## 3. Exploitation
To extract the flag, we need to preserve the exact whitespace formatting. Copy-pasting from a browser often fails because the browser converts tabs to spaces.

### Step 1: Fetch the raw data
We use `curl` to download the content directly to a file to ensure the tabs and spaces remain intact:
```bash
curl -s https://kashictf.iitbhucybersec.in/poem > poem.txt
```

### Step 2: Extraction
Using the `stegsnow` utility, we attempt to extract the hidden message. Since no compression flag (`-C`) or password (`-p`) was required for this specific challenge, we run:
```bash
stegsnow poem.txt
```

## 4. Result
The tool successfully parses the whitespace and outputs the flag:
**Flag:** `KASHI{WHiT3_5p4C3_i5_FUN_bf821a}` 
*(Note: Your actual flag value may vary slightly depending on the specific instance.)*

## Key Takeaway
Always use `curl` or `wget` for whitespace-related challenges. Manual copy-pasting is the "silent killer" of steganography payloads because it alters the hidden bits of information.

---

Would you like to explore how to solve this using an online tool like CyberChef if you didn't have `stegsnow` installed?
