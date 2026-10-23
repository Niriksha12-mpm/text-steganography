"""
Modern Web Studio for Text Steganography
----------------------------------------
Built with Streamlit for a fast, responsive, browser-based UI/UX.
Features:
- Drag-and-drop image upload
- Live capacity calculations & dynamic progress gauges
- Side-by-side original vs stego image comparison
- One-click stego image download button
- Interactive tamper radar on extraction
- Educational walkthrough of LSB substitution & majority voting
"""

import streamlit as st
from PIL import Image
import io
import os
import tempfile
from stego_core import encode_text, decode_text, get_image_capacity

# Configure Page
st.set_page_config(
    page_title="Text Steganography Studio",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Theme
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .badge-robust {
        background-color: #e0e7ff;
        color: #4338ca;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
    }
    .badge-intact {
        background-color: #d1fae5;
        color: #065f46;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 600;
    }
    .badge-tampered {
        background-color: #fef3c7;
        color: #92400e;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Top Banner
st.markdown("""
<div class="main-header">
    <h1 style="margin:0; font-size: 28px;">🔐 Text Steganography Studio</h1>
    <p style="margin:4px 0 0 0; color: #94a3b8; font-size: 14px;">
        Robust LSB Digital Image Steganography with Majority-Voting Error Correction & Tamper Detection
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Information
with st.sidebar:
    st.subheader("⚙️ System Status")
    st.info("💡 **Tip**: Always download and transmit images in lossless **PNG** format to preserve hidden LSB data.")
    
    st.markdown("---")
    st.markdown("### 🔬 Core Architecture")
    st.markdown("- **Algorithm**: Spatial LSB substitution")
    st.markdown("- **Fault Tolerance**: 5x Block-Interleaved Majority Voting")
    st.markdown("- **Header**: 64-bit protected binary header")
    st.markdown("- **Format**: Lossless RGB PNG/BMP")
    
    st.markdown("---")
    st.markdown("### ⚡ Quick Demo Image")
    if st.button("Generate Demo Image in Workspace"):
        demo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_carrier.png")
        if not os.path.exists(demo_path):
            img = Image.new("RGB", (300, 300))
            for y in range(300):
                for x in range(300):
                    img.putpixel((x, y), (int(255 * x / 300), int(255 * y / 300), 160))
            img.save(demo_path, format="PNG")
        st.success("✅ Demo image ready at `sample_carrier.png`!")

# Main Tabs
tab_encode, tab_decode, tab_about = st.tabs([
    "🔒 Hide Message (Encode)",
    "🔓 Extract Message (Decode)",
    "📘 How It Works & Theory"
])

# =============================================================================
# TAB 1: ENCODE
# =============================================================================
with tab_encode:
    st.subheader("Step 1: Upload Carrier Image")
    uploaded_file = st.file_uploader(
        "Choose a carrier image (PNG, JPG, BMP)",
        type=["png", "jpg", "jpeg", "bmp"],
        key="uploader_encode"
    )

    if uploaded_file:
        # Load and display image metrics
        col_img, col_settings = st.columns([1, 1.2])

        with col_img:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Carrier Image Preview", use_container_width=True)
            w, h = image.size
            file_kb = uploaded_file.size / 1024

        with col_settings:
            # Mode selection
            mode_choice = st.radio(
                "Protection & Integrity Mode:",
                options=[
                    "🛡️ Robust Mode (5x Redundancy) — Recommended (Survives pixel edits & noise)",
                    "⚡ Standard Mode (1x Redundancy) — Maximum Capacity"
                ],
                index=0
            )
            redundancy = 5 if "5x" in mode_choice else 1

            # Save uploaded image to temp file for capacity calculation
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                image.save(tmp.name, format="PNG")
                tmp_cover_path = tmp.name

            try:
                capacity = get_image_capacity(tmp_cover_path, redundancy=redundancy)
            except Exception:
                capacity = 0

            # Metrics Row
            m1, m2, m3 = st.columns(3)
            m1.metric("Dimensions", f"{w} × {h} px")
            m2.metric("File Size", f"{file_kb:.1f} KB")
            m3.metric("Capacity", f"{capacity:,} chars")

            st.markdown("---")
            st.subheader("Step 2: Enter Secret Message")
            secret_input = st.text_area(
                "Secret Confidential Text:",
                height=130,
                placeholder="Type your sensitive message here..."
            )

            # Capacity Progress
            msg_len = len(secret_input)
            if capacity > 0:
                pct = min(1.0, msg_len / capacity)
                st.progress(pct, text=f"Capacity Used: {msg_len:,} / {capacity:,} characters ({pct*100:.1f}%)")
            else:
                st.warning("Image capacity is too small.")

            # Action button
            if st.button("🔒 Embed Message & Generate Stego Image", type="primary", use_container_width=True):
                if not secret_input.strip():
                    st.error("Please enter a message to hide.")
                else:
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as out_tmp:
                            out_stego_path = out_tmp.name

                        res = encode_text(tmp_cover_path, secret_input, out_stego_path, redundancy=redundancy)
                        st.success(f"✅ Secret message successfully embedded in **{res['mode']}** mode!")

                        # Download button
                        with open(out_stego_path, "rb") as f:
                            stego_bytes = f.read()

                        st.download_button(
                            label="⬇️ Download Stego Image (.png)",
                            data=stego_bytes,
                            file_name="stego_image.png",
                            mime="image/png",
                            type="secondary",
                            use_container_width=True
                        )

                        # Clean up
                        os.unlink(out_stego_path)

                    except Exception as e:
                        st.error(f"Encoding failed: {e}")

            # Clean up cover temp
            if os.path.exists(tmp_cover_path):
                os.unlink(tmp_cover_path)
    else:
        st.info("👆 Upload an image above to start hiding messages.")

# =============================================================================
# TAB 2: DECODE
# =============================================================================
with tab_decode:
    st.subheader("Step 1: Upload Stego Image")
    stego_upload = st.file_uploader(
        "Choose an image containing hidden data (PNG, BMP)",
        type=["png", "bmp"],
        key="uploader_decode"
    )

    if stego_upload:
        col_stego_img, col_extract = st.columns([1, 1.2])

        with col_stego_img:
            stego_img = Image.open(stego_upload).convert("RGB")
            st.image(stego_img, caption="Stego Image Preview", use_container_width=True)

        with col_extract:
            if st.button("🔓 Extract Secret Message & Verify Integrity", type="primary", use_container_width=True):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_s:
                    stego_img.save(tmp_s.name, format="PNG")
                    tmp_stego_path = tmp_s.name

                try:
                    res = decode_text(tmp_stego_path)

                    # Integrity Card
                    if res.tampered:
                        st.markdown(f"""
                        <div class="badge-tampered" style="margin-bottom:12px;">
                            ⚠️ TAMPERING DETECTED & REPAIRED ({res.mode})<br>
                            <small>• Corrupted bits repaired: <b>{res.tampered_bits:,} bits</b> via Majority Voting.<br>
                            • Tamper Rate: <b>{res.tamper_rate}%</b> of sampled bits were modified.</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="badge-intact" style="margin-bottom:12px;">
                            ✅ IMAGE INTACT & PRISTINE ({res.mode})<br>
                            <small>• Clean signal: 0 bit flips detected.<br>
                            • 100.0% pixel bit integrity match.</small>
                        </div>
                        """, unsafe_allow_html=True)

                    # Extracted Text
                    st.text_area(
                        "Extracted Confidential Message:",
                        value=res,
                        height=150
                    )

                    st.download_button(
                        label="📄 Download Secret Message (.txt)",
                        data=res,
                        file_name="secret_message.txt",
                        mime="text/plain"
                    )

                except Exception as e:
                    st.error(f"Extraction failed: {e}")

                finally:
                    if os.path.exists(tmp_stego_path):
                        os.unlink(tmp_stego_path)

# =============================================================================
# TAB 3: HOW IT WORKS & THEORY
# =============================================================================
with tab_about:
    st.markdown("### 🧠 How Spatial LSB Steganography Works")
    st.markdown("""
    Every digital color image is stored as an array of pixels. Each pixel has three 8-bit color channels:
    **Red (R)**, **Green (G)**, and **Blue (B)**, with values between `0` and `255`.
    """)

    st.code("""
    Original Pixel Red:   11001000 (200)
    Secret Bit:                  1
    Stego Pixel Red:      11001001 (201)
    Difference:           +1 unit (completely imperceptible to human eyes)
    """, language="text")

    st.markdown("### 🛡️ Why Standard LSB Breaks and How We Solved It")
    st.markdown("""
    - **The Problem**: Standard LSB is fragile. Modifying pixels flips the bits, and destroys fragile string delimiters (`#####END#####`).
    - **The Solution (Majority Voting)**:
      1. We embed each secret bit across **5 independent pixel channels** distributed across separate blocks.
      2. When reading the image, the decoder samples all 5 copies. If 3 or more copies agree on `1`, the bit is recovered as `1`.
      3. This allows the secret message to survive pixel edits, drawing in Paint, and localized image noise!
    """)
