<div align="center">

# 🔐 TEXT STEGANOGRAPHY STUDIO
### Executive Robust LSB Data Hiding with Majority-Voting Error Correction

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![UI Framework](https://img.shields.io/badge/GUI-CustomTkinter%20%7C%20Streamlit-6366f1)
![Security Protocol](https://img.shields.io/badge/Security-5x%20Majority%20Voting-10b981)
![Image Format](https://img.shields.io/badge/Format-Lossless%20PNG%20%2F%20BMP-f59e0b)
![License](https://img.shields.io/badge/License-MIT-gray)

**A next-generation steganography suite featuring a 2-Column Executive Dashboard, real-time telemetry, and majority-voting error correction to withstand pixel tampering.**

</div>

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

## 🌟 Executive 2-Column Dashboard Layout

```text
+----------------------------------------------------------------------------------------------------+
|  🔐 TEXT STEGANOGRAPHY STUDIO [v2.5 PRO]                                       🌙 Dark / ☀️ Light  |
+----------------------------------------------------------------------------------------------------+
|  [ 🔒 HIDE MESSAGE (ENCODE HUB) ]                    [ 🔓 EXTRACT MESSAGE (DECODE HUB) ]           |
|                                                                                                    |
|  LEFT PANEL: CARRIER IMAGE & ENGINE HUB          RIGHT PANEL: SECRET MESSAGE STUDIO                |
|  +--------------------------------------------+  +-----------------------------------------------+ |
|  | [📷 Live High-DPI Thumbnail Preview]       |  | Monospace Payload Editor (JetBrains Mono)     | |
|  |                                            |  |                                               | |
|  | 📐 Res: 800 x 600 px  | 💾 Size: 142.5 KB   |  | "Type your sensitive confidential payload..." | |
|  | 🖼️ Format: Lossless PNG                     |  |                                               | |
|  | ⚡ Max Capacity: 35,984 characters         |  |                                               | |
|  |                                            |  |                                               | |
|  | [📁 Browse Image...]   [⚡ Demo Image]     |  | --------------------------------------------- | |
|  |                                            |  | Telemetry: Payload: 142 chars | Capacity: 2.6% | |
|  | SECURITY MODE:                             |  | Capacity Progress: [=============>        ]   | |
|  | [ 🛡️ Robust (5x) ]   [ ⚡ Standard (1x) ]   |  |                                               | |
|  +--------------------------------------------+  | [ Clear ]    [ 🔒 Hide Message & Save Stego ] | |
|                                                  +-----------------------------------------------+ |
+----------------------------------------------------------------------------------------------------+
|  Ready. System Online.                                                                             |
+----------------------------------------------------------------------------------------------------+
```

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

## 📁 Project Architecture

```text
text-steganography/
│
├── stego_core.py            # Core algorithms (Standard & Robust 5x LSB with Majority Voting)
├── gui.py                   # Executive 2-Column Dashboard GUI (CustomTkinter, streamlined text studio)
├── app_web.py               # Glassmorphic Web Studio (Streamlit, 2-column layout, download tools)
├── cli.py                   # Interactive Command-Line Interface (terminal menu)
├── main.py                  # Main unified entry point (Desktop GUI, --web, --cli)
├── sample_test.py           # Automated test suite (including deliberate pixel tampering test)
├── sample_carrier.png       # Sample cover image
├── sample_stego_robust.png  # Stego image with 5x redundant embedding
├── sample_stego_tampered.png# Stego image with 1,600 intentionally corrupted pixels
└── README.md                # Project documentation and report
```

---

## ⚙️ Installation & Requirements

The project runs on **Python 3.8+** with the following packages:

```bash
pip install pillow customtkinter streamlit
```

---

## 🚀 How to Run

### 1. Executive Desktop GUI (Default)
```bash
python main.py
```
*(or `python gui.py`)*

### 2. Browser-Based Web Studio
```bash
python main.py --web
```
*(or `streamlit run app_web.py`)*

### 3. Interactive CLI
```bash
python main.py --cli
```

### 4. Automated Tamper-Resilience Verification Test
```bash
python sample_test.py
```
