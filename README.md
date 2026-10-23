# TEXT STEGANOGRAPHY STUDIO (ROBUST LSB DATA HIDING)

A complete, modern Python application for hiding confidential text messages inside digital images using **Least Significant Bit (LSB) Steganography**, featuring **Majority-Voting Error Correction**, **Tamper Detection**, a **Modern Desktop GUI**, and a **Streamlit Web Studio**.

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

## 🎨 UI/UX Features & Interfaces

### 1. Modern Desktop GUI (`gui.py`)
- **Card-Based Interface**: Clean card containers with subtle borders and clear visual hierarchy.
- **Live Thumbnail Previews**: Real-time canvas preview of selected cover and stego images with aspect ratio preservation.
- **Dynamic Capacity Meter & Progress Bar**: Real-time visual progress bar tracking capacity utilization as you type.
- **1-Click "Load Demo Image"**: Instant sample image loader for fast demonstrations during reviews and viva exams.
- **Interactive Tamper Radar**: Visual health card in the Decode tab displaying:
  - 🟢 **Pristine**: 0 bit flips detected.
  - 🟡 **Tampered & Repaired**: Exact count of corrupted bits repaired by Majority Voting + Tamper Rate percentage.
- **Interactive Copy Feedback**: "✓ Copied to Clipboard!" animated confirmation button.

### 2. Companion Web Studio (`app_web.py`)
- Browser-based interface powered by **Streamlit**.
- Drag-and-drop file uploaders for cover and stego images.
- Side-by-side comparison metrics.
- 1-click **Download Stego Image** button.
- Educational interactive tabs explaining LSB theory.

### 3. Interactive CLI (`cli.py`)
- Terminal menu for lightweight headless environments.

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
├── gui.py                   # Modern Desktop GUI (Card layout, live thumbnails, dynamic capacity)
├── app_web.py               # Modern Streamlit Web Studio (Drag-and-drop, browser interface)
├── cli.py                   # Interactive Command-Line Interface (terminal menu)
├── main.py                  # Main entry point (Desktop GUI, --web, --cli)
├── sample_test.py           # Automated test suite (including deliberate pixel tampering test)
├── sample_carrier.png       # Sample cover image
├── sample_stego_robust.png  # Stego image with 5x redundant embedding
├── sample_stego_tampered.png# Stego image with 1,600 intentionally corrupted pixels
└── README.md                # Project documentation and report
```

---

## ⚙️ Installation & Requirements

The project requires **Python 3.8+**, **Pillow**, and **Streamlit**:

```bash
pip install pillow streamlit
```

---

## 🚀 How to Run the Project

### Option 1: Modern Desktop GUI (Default)
```bash
python main.py
```
*(or `python gui.py`)*

### Option 2: Modern Web Application (Browser)
```bash
python main.py --web
```
*(or `streamlit run app_web.py`)*

### Option 3: Command-Line Interface (CLI)
```bash
python main.py --cli
```

### Option 4: Run the Verification Script (with Tamper Test)
```bash
python sample_test.py
```
