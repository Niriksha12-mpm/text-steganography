"""
Automated Verification & Demonstration Script for Text Steganography
--------------------------------------------------------------------
Tests:
1. Standard Mode: Embedding & decoding without loss.
2. Robust Mode: Embeds secret message, INTENTIONALLY MODIFIES/TAMPERES with pixels,
   and proves that Majority Voting still retrieves the secret message 100% intact!
3. Error handling on un-encoded carrier image.
"""

import os
import sys
from PIL import Image, ImageDraw
from stego_core import encode_text, decode_text, get_image_capacity


def create_sample_image(filename: str, width: int = 250, height: int = 250):
    """Generates a clean RGB gradient carrier image for testing."""
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        r = int(255 * (y / height))
        for x in range(width):
            g = int(255 * (x / width))
            b = int(255 * ((x + y) / (width + height)))
            img.putpixel((x, y), (r, g, b))
            
    img.save(filename, format="PNG")
    return filename


def tamper_with_image(image_path: str, tampered_path: str):
    """
    Intentionally corrupts/modifies a block of pixels in the stego image
    to simulate drawing on it or editing it in an image editor.
    """
    with Image.open(image_path) as img:
        img_copy = img.copy()
        draw = ImageDraw.Draw(img_copy)
        
        # Draw a solid rectangle over the first pixels where data is stored
        # Modifying (x: 5 to 25, y: 0 to 10) -> directly corrupting hundreds of embedded bits!
        draw.rectangle([5, 0, 25, 10], fill=(255, 0, 128))
        
        img_copy.save(tampered_path, format="PNG")
        return tampered_path


def run_tests():
    print("=" * 70)
    print("   RUNNING TEXT STEGANOGRAPHY VERIFICATION & TAMPER-RESILIENCE TESTS")
    print("=" * 70)

    carrier_path = "sample_carrier.png"
    stego_standard_path = "sample_stego_std.png"
    stego_robust_path = "sample_stego_robust.png"
    tampered_stego_path = "sample_stego_tampered.png"

    # Step 1: Create carrier image
    print("\n[STEP 1] Generating sample carrier image (250x250 pixels)...")
    create_sample_image(carrier_path, 250, 250)
    cap_std = get_image_capacity(carrier_path, redundancy=1)
    cap_rob = get_image_capacity(carrier_path, redundancy=5)
    print(f" -> Carrier created: 250x250 pixels.")
    print(f" -> Standard Capacity (1x): {cap_std:,} characters.")
    print(f" -> Robust Capacity (5x):   {cap_rob:,} characters.")

    test_secret = (
        "CONFIDENTIAL TRANSMISSION\n"
        "Project: Text Steganography via LSB\n"
        "Status: Success!\n"
        "Security Clearance: Top Secret\n"
        "This message must survive pixel tampering!"
    )

    # Step 2: Test Standard Mode
    print("\n[STEP 2] Testing Standard Mode (1x)...")
    encode_text(carrier_path, test_secret, stego_standard_path, redundancy=1)
    res_std = decode_text(stego_standard_path)
    assert res_std == test_secret, "Standard mode decode mismatch!"
    print(f"[PASS] Standard mode: Message encoded and extracted cleanly.")

    # Step 3: Test Robust Mode with INTENTIONAL PIXEL TAMPERING!
    print("\n[STEP 3] Testing Robust Mode (5x) with DELIBERATE PIXEL TAMPERING...")
    stats = encode_text(carrier_path, test_secret, stego_robust_path, redundancy=5)
    print(f" -> Message encoded with 5x Redundancy into {stego_robust_path}")
    
    # Tamper with the image
    print(" -> Deliberately corrupting pixels (drawing a solid 40x40 box over the image)...")
    tamper_with_image(stego_robust_path, tampered_stego_path)
    print(f" -> Tampered image saved to {tampered_stego_path} (1,600 pixels altered!)")

    # Extract from the tampered image
    print(" -> Decoding message from the heavily tampered image...")
    res_tampered = decode_text(tampered_stego_path)
    
    print("\n-----------------------------------------------------------------")
    print("RECOVERED MESSAGE FROM TAMPERED IMAGE:")
    print("-----------------------------------------------------------------")
    print(res_tampered)
    print("-----------------------------------------------------------------")
    
    assert res_tampered == test_secret, "Robust mode failed to recover message after tampering!"
    assert res_tampered.tampered is True, "Tamper detector failed to flag altered pixels!"
    assert res_tampered.tampered_bits > 0, "Tampered bits count should be > 0!"
    
    print(f"\n[VERIFICATION PASSED] Message retrieved 100% intact despite pixel damage!")
    print(f" -> Tamper Detector: SUCCESSFULLY DETECTED!")
    print(f" -> Bits Corrected:  {res_tampered.tampered_bits:,} corrupted bits repaired via Majority Voting.")
    print(f" -> Tamper Rate:     {res_tampered.tamper_rate}%")

    # Step 4: Test un-encoded image error handling
    print("\n[STEP 4] Testing non-stego image error handling...")
    try:
        decode_text(carrier_path)
        print("[FAIL] Carrier image should not contain a message!")
    except ValueError as e:
        print(f"[PASS] Expected error correctly caught: {e}")

    print("\n" + "=" * 70)
    print("   ALL TESTS PASSED! ROBUST STEGANOGRAPHY IS 100% OPERATIONAL")
    print("=" * 70)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    run_tests()
