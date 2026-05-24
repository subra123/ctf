# Write-up: Burnt Ashes (Forensics - 500 pts)

## Challenge Overview
The objective was to recover a hidden flag from a Linux disk image (`kashi_ritual_ledger.img`) suspected of containing layered steganography and encryption.

## Step-by-Step Solution

### 1. Initial Image Analysis
First, we identified the file type of the provided image.
```bash
file kashi_ritual_ledger.img
# Output: Linux rev 1.0 ext4 filesystem data, volume name "KASHI_LEDGER"
```
The image is a standard **ext4 filesystem**.

### 2. Exploring the Filesystem
Using `fls` (from The Sleuth Kit), we listed the files within the image to understand the structure.
```bash
fls -r kashi_ritual_ledger.img
```
**Key discoveries in `/home/pandit_ved/`:**
*   `.archive_payloads/`: Contained several `.enc` and `.txt` files (decoy ledgers and `stage2_ledger`).
*   `Notes/`: Contained `restoration_log.txt` and `ritual_index_notes.md`.
*   `chatlogs/`: Contained communications between `ved` and `tara`.
*   `Pictures/ward_scans/`: Four BMP images.

### 3. Information Gathering
We extracted and read the notes and chat logs using `icat`:

*   **`ritual_index_notes.md`**: Mentioned a "passphrase doctrine" where the first part of a key is `ghat manjari` followed by two words from a ritual word list.
*   **Chat Logs**: Revealed an AES-256-CBC encryption scheme, a decoy passphrase (`trishul-lantern-braid`), and specific salt/IV values. It also hinted that the "final capsule" used a different passphrase.
*   **`restoration_log.txt`**: Confirmed that BMP scans were uploaded and might contain hidden data.

### 4. Locating the Flag
While the challenge pointed toward a complex decryption or steganography path (involving the BMPs or `.enc` files), the `stage2_ledger.txt` file found in the `.archive_payloads` directory already contained the final reconstructed note.

By extracting inode **25** (the `stage2_ledger.txt` file):
```bash
icat kashi_ritual_ledger.img 25
```

**File Content:**
```text
Hidden Ledger Capsule
====================

Reconstructed transfer note, sealed for tribunal audit.
Flag: kashiCTF{ledger_ashes_remember_every_ritual}

Custodian phrase seed: ghat manjari
```

## Flag
`kashiCTF{ledger_ashes_remember_every_ritual}`
