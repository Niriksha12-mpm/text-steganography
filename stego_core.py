"""
Text Steganography Core Module (with Robust Error-Correction & Tamper Detection)
-------------------------------------------------------------------------------
Implements spatial LSB image steganography with:
1. Standard Mode (1x): Direct LSB embedding for maximum storage capacity.
2. Robust Mode (3x / 5x): Redundant block-interleaved embedding with Majority
   Voting. This allows the secret message to survive pixel edits, noise, and
   drawing/tampering, while detecting and repairing corrupted bits.
"""

from PIL import Image
import os
import struct

# Magic signature for robust steganography header (3 bytes)
MAGIC_SIGNATURE = b"STG"

# Legacy delimiter for backward compatibility
DELIMITER = "#####END#####"

HEADER_BITS = 64  # 8 bytes: 3 bytes MAGIC, 1 byte MODE, 4 bytes LENGTH


class StegoResult(str):
    """
    Subclasses str so it can be treated directly as a string, while
    providing tamper detection metrics and encoding statistics.
    """
    def __new__(cls, message: str, stats: dict = None):
        instance = super().__new__(cls, message)
        instance.stats = stats or {}
        instance.message = message
        instance.tampered_bits = instance.stats.get("tampered_bits", 0)
        instance.tampered = instance.tampered_bits > 0
        instance.tamper_rate = instance.stats.get("tamper_rate", 0.0)
        instance.redundancy = instance.stats.get("redundancy", 1)
        instance.mode = instance.stats.get("mode", "Standard")
        return instance


def text_to_binary(text: str) -> str:
    """Converts a string of text into its 8-bit binary representation."""
    byte_data = text.encode('utf-8')
    return ''.join(format(byte, '08b') for byte in byte_data)


def binary_to_text(binary_data: str) -> str:
    """Converts a binary string back into UTF-8 text."""
    bytes_list = []
    for i in range(0, len(binary_data), 8):
        byte_str = binary_data[i:i+8]
        if len(byte_str) == 8:
            bytes_list.append(int(byte_str, 2))
    return bytes(bytes_list).decode('utf-8', errors='replace')


def get_image_capacity(image_path: str, redundancy: int = 5) -> int:
    """
    Calculates the maximum characters that can be hidden in an image.
    
    Parameters:
        image_path (str): Path to image.
        redundancy (int): 1 for Standard mode, 3 or 5 for Robust mode.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at: {image_path}")
    
    with Image.open(image_path) as img:
        width, height = img.size
        total_channels = width * height * 3
        
        # Header size in bits
        header_channel_cost = HEADER_BITS * redundancy
        available_channels = total_channels - header_channel_cost
        
        if available_channels <= 0:
            return 0
        
        # Each character is 8 bits, each bit requires `redundancy` channels
        return available_channels // (8 * redundancy)


def encode_text(image_path: str, secret_text: str, output_path: str, redundancy: int = 5) -> dict:
    """
    Encodes secret text into an image.
    
    Parameters:
        image_path (str): Path to cover image.
        secret_text (str): Confidential text to hide.
        output_path (str): Destination path for the stego image (.png).
        redundancy (int): 1 (Standard mode) or 3/5 (Robust Tamper-Resistant mode).
        
    Returns:
        dict: Encoding summary statistics.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Source image not found: {image_path}")
    
    if not secret_text:
        raise ValueError("Secret text cannot be empty.")
    
    if redundancy not in [1, 3, 5]:
        raise ValueError("Redundancy must be 1 (Standard), 3, or 5 (Robust).")

    with Image.open(image_path) as img:
        rgb_img = img.convert('RGB')
        width, height = rgb_img.size
        total_pixels = width * height
        total_channels = total_pixels * 3
        
        # Prepare message bytes
        text_bytes = secret_text.encode('utf-8')
        message_len = len(text_bytes)
        
        # Header: 3 bytes MAGIC ('STG') + 1 byte MODE (ascii '1', '3', or '5') + 4 bytes LENGTH
        mode_byte = str(redundancy).encode('ascii')
        header_bytes = MAGIC_SIGNATURE + mode_byte + struct.pack(">I", message_len)
        header_bits = ''.join(format(b, '08b') for b in header_bytes)  # exactly 64 bits
        
        message_bits = ''.join(format(b, '08b') for b in text_bytes)
        M = len(message_bits)
        
        total_required_channels = (HEADER_BITS * redundancy) + (M * redundancy)
        if total_required_channels > total_channels:
            max_chars = (total_channels - (HEADER_BITS * redundancy)) // (8 * redundancy)
            mode_name = "Robust (5x)" if redundancy == 5 else ("Robust (3x)" if redundancy == 3 else "Standard (1x)")
            raise ValueError(
                f"Message too large for this image in {mode_name} mode! "
                f"Image capacity is {max_chars:,} characters, but message is {len(secret_text):,} characters."
            )
            
        # Extract flat list of color channel values
        raw_pixels = list(rgb_img.getdata())
        channels = []
        for r, g, b in raw_pixels:
            channels.extend([r, g, b])
            
        # 1. Embed Header with Interleaved Redundancy in the first (HEADER_BITS * redundancy) channels
        # Copy k of header bit j is placed at: k * 64 + j
        for k in range(redundancy):
            for j in range(HEADER_BITS):
                bit = int(header_bits[j])
                ch_idx = (k * HEADER_BITS) + j
                channels[ch_idx] = (channels[ch_idx] & ~1) | bit
                
        # 2. Embed Message Bits with Block-Interleaved Redundancy
        # Copy k of message bit i is placed at: (HEADER_BITS * redundancy) + (k * M) + i
        header_offset = HEADER_BITS * redundancy
        for k in range(redundancy):
            for i in range(M):
                bit = int(message_bits[i])
                ch_idx = header_offset + (k * M) + i
                channels[ch_idx] = (channels[ch_idx] & ~1) | bit
                
        # Reconstruct RGB pixels
        new_pixels = []
        for i in range(0, len(channels), 3):
            new_pixels.append((channels[i], channels[i+1], channels[i+2]))
            
        # Save as lossless PNG
        stego_img = Image.new('RGB', (width, height))
        stego_img.putdata(new_pixels)
        
        base_root, ext = os.path.splitext(output_path)
        if ext.lower() not in ['.png', '.bmp']:
            output_path = base_root + '.png'
            
        stego_img.save(output_path, format='PNG')
        
        return {
            "width": width,
            "height": height,
            "total_pixels": total_pixels,
            "message_length": len(secret_text),
            "redundancy": redundancy,
            "mode": f"Robust ({redundancy}x)" if redundancy > 1 else "Standard (1x)",
            "channels_used": total_required_channels,
            "capacity_used_percent": round((total_required_channels / total_channels) * 100, 2),
            "output_path": output_path
        }


def decode_text(stego_image_path: str) -> StegoResult:
    """
    Extracts the hidden secret text from a stego image.
    Automatically detects whether the image was encoded in Standard or Robust
    mode, performs Majority Voting error correction, and measures pixel tampering.
    
    Returns:
        StegoResult: Extracted text with .tampered, .tampered_bits, and .stats attributes.
    """
    if not os.path.exists(stego_image_path):
        raise FileNotFoundError(f"Stego image not found: {stego_image_path}")
        
    with Image.open(stego_image_path) as img:
        rgb_img = img.convert('RGB')
        raw_pixels = list(rgb_img.getdata())
        
        channels = []
        for r, g, b in raw_pixels:
            channels.extend([r, g, b])
            
        total_channels = len(channels)
        
        # Step 1: Detect Robust Header (try redundancy 5, 3, or 1)
        detected_redundancy = None
        decoded_header_bytes = None
        header_tamper_count = 0
        
        for cand_red in [5, 3, 1]:
            if total_channels < HEADER_BITS * cand_red:
                continue
                
            header_bits = []
            cand_tamper = 0
            
            for j in range(HEADER_BITS):
                # Sample all redundant copies of header bit j
                samples = [channels[(k * HEADER_BITS) + j] & 1 for k in range(cand_red)]
                ones = sum(samples)
                majority_bit = 1 if ones > (cand_red / 2) else 0
                header_bits.append(str(majority_bit))
                cand_tamper += min(ones, cand_red - ones)
                
            # Convert 64 bits to 8 bytes
            h_bytes = bytearray()
            for b_idx in range(0, 64, 8):
                byte_val = int(''.join(header_bits[b_idx:b_idx+8]), 2)
                h_bytes.append(byte_val)
                
            magic = bytes(h_bytes[:3])
            mode = chr(h_bytes[3]) if h_bytes[3] else ''
            
            if magic == MAGIC_SIGNATURE and mode == str(cand_red):
                detected_redundancy = cand_red
                decoded_header_bytes = bytes(h_bytes)
                header_tamper_count = cand_tamper
                break
                
        # If Robust Header Found:
        if detected_redundancy is not None:
            message_len = struct.unpack(">I", decoded_header_bytes[4:8])[0]
            M = message_len * 8
            
            header_offset = HEADER_BITS * detected_redundancy
            required_channels = header_offset + (M * detected_redundancy)
            
            if required_channels > total_channels or message_len < 0:
                raise ValueError("Corrupted image header: message length exceeds image bounds.")
                
            # Decode message bits with Majority Voting across interleaved blocks
            msg_bits = []
            body_tamper_count = 0
            
            for i in range(M):
                samples = []
                for k in range(detected_redundancy):
                    ch_idx = header_offset + (k * M) + i
                    samples.append(channels[ch_idx] & 1)
                    
                ones = sum(samples)
                majority_bit = 1 if ones > (detected_redundancy / 2) else 0
                msg_bits.append(str(majority_bit))
                body_tamper_count += min(ones, detected_redundancy - ones)
                
            # Reconstruct message bytes
            msg_bytes = bytearray()
            for b_idx in range(0, M, 8):
                byte_val = int(''.join(msg_bits[b_idx:b_idx+8]), 2)
                msg_bytes.append(byte_val)
                
            total_tampered_bits = header_tamper_count + body_tamper_count
            total_tested_bits = (HEADER_BITS + M) * detected_redundancy
            tamper_rate = round((total_tampered_bits / total_tested_bits) * 100, 2) if total_tested_bits > 0 else 0.0
            
            decoded_text = msg_bytes.decode('utf-8', errors='replace')
            stats = {
                "mode": f"Robust ({detected_redundancy}x)" if detected_redundancy > 1 else "Standard (1x)",
                "redundancy": detected_redundancy,
                "message_length": len(decoded_text),
                "tampered_bits": total_tampered_bits,
                "tamper_rate": tamper_rate,
                "is_tampered": total_tampered_bits > 0
            }
            return StegoResult(decoded_text, stats)
            
        # Step 2: Fallback for Legacy Delimiter (backward compatibility)
        current_byte_bits = []
        extracted_bytes = bytearray()
        delimiter_bytes = DELIMITER.encode('utf-8')
        delimiter_len = len(delimiter_bytes)
        delimiter_found = False
        
        for ch in channels:
            current_byte_bits.append(str(ch & 1))
            if len(current_byte_bits) == 8:
                byte_val = int(''.join(current_byte_bits), 2)
                extracted_bytes.append(byte_val)
                current_byte_bits = []
                if len(extracted_bytes) >= delimiter_len:
                    if extracted_bytes[-delimiter_len:] == delimiter_bytes:
                        delimiter_found = True
                        break
                        
        if delimiter_found:
            msg_bytes = extracted_bytes[:-delimiter_len]
            decoded_text = msg_bytes.decode('utf-8', errors='replace')
            stats = {
                "mode": "Legacy Delimiter",
                "redundancy": 1,
                "message_length": len(decoded_text),
                "tampered_bits": 0,
                "tamper_rate": 0.0,
                "is_tampered": False
            }
            return StegoResult(decoded_text, stats)
            
        raise ValueError(
            "No hidden message found in this image (or the image suffered excessive alteration/compression)."
        )
