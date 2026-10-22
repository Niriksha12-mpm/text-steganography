# TEXT STEGANOGRAPHY (ROBUST LSB DATA HIDING)

A complete, practical Python project for hiding confidential text messages inside digital images using **Least Significant Bit (LSB) Steganography**, featuring **Majority-Voting Error Correction** and **Tamper Detection** to survive pixel edits and image modifications.

---

## 📄 Abstract

**Text Steganography** is a technique of hiding confidential information within a digital medium without making the presence of the hidden information noticeable. This project focuses on developing a program that hides a text message inside an image and retrieves the hidden message when required. The main objective is to provide a simple and effective method for protecting sensitive information during digital communication while maintaining the visual quality of the image.

The proposed system uses image steganography, particularly the **Least Significant Bit (LSB)** technique, to embed secret text into image pixels. In this method, the text message is converted into binary form, and the least significant bits of selected pixels are modified according to the binary data. Since the changes made to the pixel values are minimal, the resulting stego image appears almost identical to the original image, making the hidden information difficult to detect through normal observation.

The system consists of two main operations: **encoding** and **decoding**. 
- During **encoding**, the user selects an image and enters the text message to be hidden. The program converts the message into binary data and embeds it into the image pixels, producing a stego image.
- During **decoding**, the program reads the modified pixel values, extracts the embedded binary data, and converts it back into the original text message.

This project demonstrates the practical application of steganography in information security and secure communication. It can be used for confidential data sharing, protecting sensitive messages, and understanding digital data-hiding techniques. Overall, the project provides practical knowledge of image processing, binary data representation, encoding, decoding, and secure information exchange through digital images.

**Keywords**: *Image Steganography, Data Hiding, Least Significant Bit, Secure Communication, Cryptography, Image Processing, Data Encryption, Secret Message, Encoding, Decoding, Error Correction, Majority Voting, Tamper Detection.*

---

## 🛡️ Robust Mode: Surviving Pixel Alterations via Majority Voting

### Why Standard LSB Steganography Breaks When Pixels are Changed
In basic LSB steganography, secret bits are stored directly in the spatial pixel domain. If someone edits, crops, draws on, or modifies pixels:
1. The least significant bits flip (`0` becomes `1` or vice versa).
2. The end-of-message delimiter is destroyed, causing decoding to fail completely.

### The Solution: Majority Voting & Block Interleaving
To make the secret message resilient to pixel changes:
1. **$5\times$ Redundancy**: Every single bit of the secret message is embedded across **5 independent pixel channels** distributed across separate blocks in the image.
2. **Majority Voting**: When extracting the bits:
   $$\text{Decoded Bit} = \begin{cases} 1 & \text{if } \sum \text{samples} \ge 3 \\ 0 & \text{if } \sum \text{samples} < 3 \end{cases}$$
   Even if a user draws or edits a portion of the image, the corrupted bits are outvoted by the untouched copies!
3. **Protected Length Header**: Replaces fragile string delimiters with a 64-bit protected binary header (`MAGIC + MODE + LENGTH`).
4. **Tamper Detection**: The decoder tracks whenever bits disagree with the majority vote and displays the exact count and percentage of repaired pixel bits.

---

## 📁 Project Structure

```text
text-steganography/
│
├── stego_core.py            # Core algorithms (Standard & Robust 5x LSB with Majority Voting)
├── gui.py                   # Desktop GUI with Robust Mode toggle & Tamper Badge
├── cli.py                   # Interactive Command-Line Interface (terminal menu)
├── main.py                  # Main entry point (defaults to GUI, accepts --cli)
├── sample_test.py           # Automated test suite (including deliberate pixel tampering test)
├── sample_carrier.png       # Sample cover image
├── sample_stego_robust.png  # Stego image with 5x redundant embedding
├── sample_stego_tampered.png# Stego image with 1,600 intentionally corrupted pixels
└── README.md                # Project documentation and report
```

---

## ⚙️ Installation & Requirements

The project requires **Python 3.8+** and **Pillow**:

```bash
pip install pillow
```

---

## 🚀 How to Run the Project

### Option 1: Desktop Graphical User Interface (GUI) - Recommended
```bash
python main.py
```

#### GUI Features:
- **Hide Message (Encode) Tab**:
  - Browse cover image (`.png`, `.jpg`, `.bmp`).
  - Choose between **Robust Mode (5x Redundancy)** [Recommended] and **Standard Mode (1x)**.
  - Live capacity and character counters.
  - 1-click **Hide Secret Message & Save Stego Image**.
- **Extract Message (Decode) Tab**:
  - Select stego image.
  - Click **Extract Hidden Secret Message & Check Integrity**.
  - **Integrity Badge**:
    - 🟢 *Image Intact: Clean signal (0 corrupted bits).*
    - 🟡 *Tampering Detected & Repaired: X corrupted bits corrected via Majority Voting!*
  - **Copy Message to Clipboard** button.

---

### Option 2: Command-Line Interface (CLI)
```bash
python main.py --cli
```

Prompts you to select between **Robust Mode** and **Standard Mode**, encodes/decodes, and displays tamper statistics.

---

### Option 3: Run the Verification Script (with Tamper Test)
```bash
python sample_test.py
```

Sample output:
```text
======================================================================
   RUNNING TEXT STEGANOGRAPHY VERIFICATION & TAMPER-RESILIENCE TESTS
======================================================================
[STEP 1] Generating sample carrier image (250x250 pixels)...
[STEP 2] Testing Standard Mode (1x)... [PASS]
[STEP 3] Testing Robust Mode (5x) with DELIBERATE PIXEL TAMPERING...
 -> Deliberately corrupting pixels (drawing a solid box over embedded bits)...
 -> Tampered image saved to sample_stego_tampered.png
 -> Decoding message from the heavily tampered image...

-----------------------------------------------------------------
RECOVERED MESSAGE FROM TAMPERED IMAGE:
-----------------------------------------------------------------
CONFIDENTIAL TRANSMISSION
Project: Text Steganography via LSB
Status: Success!
Security Clearance: Top Secret
This message must survive pixel tampering!
-----------------------------------------------------------------

[VERIFICATION PASSED] Message retrieved 100% intact despite pixel damage!
 -> Tamper Detector: SUCCESSFULLY DETECTED!
 -> Bits Corrected:  272 corrupted bits repaired via Majority Voting.
 -> Tamper Rate:     4.25%
======================================================================
```

---

## ⚠️ Important Note on Image Formats (PNG vs JPEG)

- **Always save stego images as PNG (`.png`) or BMP (`.bmp`)**:
  - PNG uses **lossless compression**, preserving every pixel bit.
  - JPEG (`.jpg`) applies lossy compression (Discrete Cosine Transform) which rounds all pixel values, destroying the fine LSB values.
