"""
Interactive Command-Line Interface for Text Steganography
---------------------------------------------------------
Allows users to encode and decode secret messages from the terminal,
with support for Robust (Tamper-Resistant) and Standard modes.
"""

import sys
import os
from stego_core import encode_text, decode_text, get_image_capacity


def print_banner():
    print("=" * 65)
    print("        TEXT STEGANOGRAPHY (LSB DATA HIDING)")
    print("   With Robust Majority-Voting Error Correction & Tamper Detection")
    print("=" * 65)


def handle_encode():
    print("\n--- [1] ENCODE: HIDE SECRET MESSAGE IN IMAGE ---")
    image_path = input("Enter path to cover image (e.g. cover.png or photo.jpg): ").strip().strip('"')
    
    if not os.path.exists(image_path):
        print(f"[ERROR] File '{image_path}' not found.")
        return
    
    print("\nSelect Protection Mode:")
    print("  1. Robust Mode (5x Redundancy) [RECOMMENDED]")
    print("     -> Message survives pixel modifications, drawing, and noise via Majority Voting.")
    print("  2. Standard Mode (1x Redundancy)")
    print("     -> Maximizes storage capacity, but fragile to pixel changes.")
    mode_choice = input("Enter choice (1 or 2) [Default: 1]: ").strip()
    redundancy = 1 if mode_choice == '2' else 5
    
    try:
        capacity = get_image_capacity(image_path, redundancy=redundancy)
        mode_str = "Robust (5x)" if redundancy == 5 else "Standard (1x)"
        print(f"[INFO] Mode: {mode_str} | Max capacity: {capacity:,} characters.")
    except Exception as e:
        print(f"[ERROR] Failed to read image: {e}")
        return

    secret_text = input("\nEnter the secret message to hide: ").strip()
    if not secret_text:
        print("[ERROR] Secret message cannot be empty.")
        return

    default_output = os.path.splitext(image_path)[0] + "_stego.png"
    output_prompt = f"Enter output stego image path [Press Enter for '{default_output}']: "
    output_path = input(output_prompt).strip().strip('"')
    if not output_path:
        output_path = default_output

    try:
        result = encode_text(image_path, secret_text, output_path, redundancy=redundancy)
        print("\n[SUCCESS] Message successfully hidden!")
        print(f" -> Output Stego Image: {result['output_path']}")
        print(f" -> Mode:               {result['mode']}")
        print(f" -> Message Length:     {result['message_length']:,} characters")
        print(f" -> Capacity Used:      {result['capacity_used_percent']}%")
        if redundancy > 1:
            print(" -> Note: Protected by Majority Voting. Even if pixels are edited, the message can still be retrieved!")
    except Exception as e:
        print(f"\n[ERROR] Encoding failed: {e}")


def handle_decode():
    print("\n--- [2] DECODE: EXTRACT SECRET MESSAGE FROM IMAGE ---")
    image_path = input("Enter path to stego image (e.g. stego.png): ").strip().strip('"')
    
    if not os.path.exists(image_path):
        print(f"[ERROR] File '{image_path}' not found.")
        return
    
    try:
        result = decode_text(image_path)
        print("\n" + "=" * 65)
        print(f"[SUCCESS] SECRET MESSAGE EXTRACTED (Mode: {result.mode})")
        print("=" * 65)
        print(result)
        print("=" * 65)
        
        # Tamper Report
        if result.tampered:
            print(f"[TAMPER REPORT] ⚠️ Image had pixel alterations!")
            print(f" -> Repaired {result.tampered_bits:,} corrupted pixel bits via Majority Voting.")
            print(f" -> Tamper Rate: {result.tamper_rate}% of sampled bits had to be corrected.")
        else:
            print("[INTEGRITY REPORT] ✅ Image intact! 0 corrupted bits detected.")
            
    except Exception as e:
        print(f"\n[ERROR] Decoding failed: {e}")


def main_menu():
    while True:
        print_banner()
        print("1. Encode Secret Text into Image")
        print("2. Decode Secret Text from Image")
        print("3. Launch Graphical User Interface (GUI)")
        print("4. Exit")
        print("-" * 65)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            handle_encode()
        elif choice == '2':
            handle_decode()
        elif choice == '3':
            print("\nLaunching Graphical Interface...")
            try:
                import gui
                gui.main()
            except Exception as e:
                print(f"[ERROR] Could not start GUI: {e}")
        elif choice == '4':
            print("\nExiting Text Steganography. Goodbye!")
            sys.exit(0)
        else:
            print("\n[INVALID] Please choose 1, 2, 3, or 4.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main_menu()
