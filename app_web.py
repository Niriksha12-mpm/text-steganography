"""
Ultra-Modern Web Studio for Text Steganography
----------------------------------------------
Features:
- Executive 2-Column layout with glassmorphic cards
- Clean secret message studio with dynamic capacity gauge
- Side-by-side original vs stego inspection
- One-click downloads for stego PNG and extracted TXT
- Visual Tamper Radar with Majority Voting metrics
"""

import streamlit as st
from PIL import Image
import os
import tempfile
from stego_core import encode_text, decode_text, get_image_capacity

# Configure Page
st.set_page_config(
    page_title="Text Steganography Studio — Executive Web Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .hero-banner {
        background: linear-gradient(135deg, #090d16 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.3);
        border-radius: 16px;
        padding: 24px 32px;
        color: white;
        margin-bottom: 20px;
    }
    
    .hero-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        background: linear-gradient(90deg, #ffffff, #c7d2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 4px;
    }
    
    .badge-intact {
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.15), rgba(5, 150, 105, 0.2));
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #10b981;
        padding: 10px 16px;
        border-radius: 10px;
        font-weight: 600;
        margin-bottom: 14px;
    }
    
    .badge-tampered {
        background: linear-gradient(90deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.2));
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #f59e0b;
        padding: 10px 16px;
        border-radius: 10px;
        font-weight: 600;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Top Banner
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🔐 Text Steganography Studio — Executive Dashboard</div>
    <div class="hero-subtitle">
        Spatial LSB Steganography • 5x Majority-Voting Error Correction • Tamper Telemetry
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Engine Telemetry")
    st.info("💡 **Format Rule**: Steganographic data relies on exact spatial pixel bits. Always preserve images as lossless **PNG** or **BMP**.")
    
    st.markdown("---")
    st.markdown("#### 🔬 Technical Architecture")
    st.markdown("- **Algorithm**: Spatial LSB substitution")
    st.markdown("- **Fault Tolerance**: 5x Block-Interleaved Majority Voting")
    st.markdown("- **Header**: 64-bit protected binary header")
    st.markdown("- **Perceptibility**: $\\Delta E \\approx 0.0$ (Zero visual difference)")
    
    st.markdown("---")
    st.markdown("#### ⚡ Quick Demo Sample")
    if st.button("Generate Demo Image in Workspace", use_container_width=True):
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
    "🔒  Hide Message (Encode Hub)",
    "🔓  Extract Message (Decode Hub)",
    "📘  How It Works & Theory"
])

# =============================================================================
# TAB 1: ENCODE DASHBOARD
# =============================================================================
with tab_encode:
    col_left, col_right = st.columns([4, 6])

    # Left Column: Image & Security Hub
    with col_left:
        st.markdown("##### 📸 Carrier Image & Engine Hub")
        uploaded_file = st.file_uploader(
            "Select or drop carrier image",
            type=["png", "jpg", "jpeg", "bmp"],
            key="uploader_encode"
        )

        image = None
        capacity = 0
        w, h = 0, 0
        file_kb = 0

        if uploaded_file:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, caption="Carrier Thumbnail", use_container_width=True)
            w, h = image.size
            file_kb = uploaded_file.size / 1024

        mode_choice = st.radio(
            "Security & Resilience Mode:",
            options=[
                "🛡️ Robust Mode (5x) — Recommended (Survives pixel edits & noise)",
                "⚡ Standard Mode (1x) — Maximum Capacity"
            ],
            index=0
        )
        redundancy = 5 if "5x" in mode_choice else 1

        if image:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                image.save(tmp.name, format="PNG")
                tmp_cover_path = tmp.name

            try:
                capacity = get_image_capacity(tmp_cover_path, redundancy=redundancy)
            except Exception:
                capacity = 0

            m1, m2, m3 = st.columns(3)
            m1.metric("Dimensions", f"{w}×{h} px")
            m2.metric("Size", f"{file_kb:.1f} KB")
            m3.metric("Capacity", f"{capacity:,} c")
        else:
            st.info("Upload an image to inspect capacity.")

    # Right Column: Secret Message Studio & Telemetry
    with col_right:
        st.markdown("##### 📝 Secret Message Studio")

        secret_input = st.text_area(
            "Confidential Payload:",
            height=260,
            placeholder="Type your sensitive confidential secret message here..."
        )

        # Telemetry
        chars = len(secret_input)
        t_col1, t_col2 = st.columns(2)
        t_col1.markdown(f"**Payload**: `{chars:,} characters`")

        if capacity > 0:
            pct = min(1.0, chars / capacity)
            t_col2.markdown(f"**Capacity**: `{pct*100:.1f}%`")
            st.progress(pct)
        else:
            t_col2.markdown("**Capacity**: `0.0%`")
            st.progress(0.0)

        # Action Button
        if st.button("🔒 Embed Secret Payload & Generate Stego Image", type="primary", use_container_width=True):
            if not image:
                st.error("Please upload a carrier image first.")
            elif not secret_input.strip():
                st.error("Please enter a message to hide.")
            else:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as out_tmp:
                        out_stego_path = out_tmp.name

                    res = encode_text(tmp_cover_path, secret_input, out_stego_path, redundancy=redundancy)
                    st.success(f"✅ Secret message successfully embedded in **{res['mode']}** mode!")

                    with open(out_stego_path, "rb") as f:
                        stego_bytes = f.read()

                    st.download_button(
                        label="⬇️ Download Stego Image (.png)",
                        data=stego_bytes,
                        file_name="stego_image.png",
                        mime="image/png",
                        type="primary",
                        use_container_width=True
                    )
                    os.unlink(out_stego_path)

                except Exception as e:
                    st.error(f"Encoding failed: {e}")

        if image and os.path.exists(tmp_cover_path):
            os.unlink(tmp_cover_path)

# =============================================================================
# TAB 2: DECODE DASHBOARD
# =============================================================================
with tab_decode:
    d_col1, d_col2 = st.columns([4, 6])

    with d_col1:
        st.markdown("##### 🔍 Stego Image Inspector")
        stego_upload = st.file_uploader(
            "Select stego image containing hidden text",
            type=["png", "bmp"],
            key="uploader_decode"
        )

        stego_img = None
        if stego_upload:
            stego_img = Image.open(stego_upload).convert("RGB")
            st.image(stego_img, caption="Stego Thumbnail", use_container_width=True)
            sw, sh = stego_img.size
            s_kb = stego_upload.size / 1024
            st.caption(f"📐 {sw}×{sh} px  |  🖼️ Lossless PNG  |  💾 {s_kb:.1f} KB")

    with d_col2:
        st.markdown("##### 📄 Extracted Confidential Message")

        if stego_img:
            if st.button("🔓 Extract Secret Message & Verify Integrity", type="primary", use_container_width=True):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_s:
                    stego_img.save(tmp_s.name, format="PNG")
                    tmp_stego_path = tmp_s.name

                try:
                    res = decode_text(tmp_stego_path)

                    # Tamper Radar Card
                    if res.tampered:
                        st.markdown(f"""
                        <div class="badge-tampered">
                            <b>⚠️ TAMPERING DETECTED & REPAIRED ({res.mode})</b><br>
                            <small>• Corrupted bits repaired: <b>{res.tampered_bits:,} bits</b> via Majority Voting.<br>
                            • Tamper Rate: <b>{res.tamper_rate}%</b> of sampled bits were modified.<br>
                            • Status: 100% of secret text successfully restored.</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="badge-intact">
                            <b>✅ IMAGE INTACT & PRISTINE ({res.mode})</b><br>
                            <small>• Clean signal: 0 bit flips detected.<br>
                            • 100.0% pixel bit integrity match.</small>
                        </div>
                        """, unsafe_allow_html=True)

                    st.text_area(
                        "Extracted Confidential Message:",
                        value=res,
                        height=240
                    )

                    c1, c2 = st.columns(2)
                    c1.markdown(f"**Payload**: `{len(res):,} characters`")
                    c2.download_button(
                        label="📄 Download Extracted Message (.txt)",
                        data=res,
                        file_name="secret_message.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                except Exception as e:
                    st.error(f"Extraction failed: {e}")

                finally:
                    if os.path.exists(tmp_stego_path):
                        os.unlink(tmp_stego_path)
        else:
            st.info("Upload a stego image on the left to extract hidden payloads.")

# =============================================================================
# TAB 3: HOW IT WORKS
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

    st.markdown("### 🛡️ Why Standard LSB Breaks & How Majority Voting Solves It")
    st.markdown("""
    - **The Problem**: Standard LSB is fragile. Modifying pixels flips the bits, and destroys fragile string delimiters (`#####END#####`).
    - **The Solution (Majority Voting)**:
      1. We embed each secret bit across **5 independent pixel channels** distributed across separate blocks.
      2. When reading the image, the decoder samples all 5 copies. If 3 or more copies agree on `1`, the bit is recovered as `1`.
      3. This allows the secret message to survive pixel edits, drawing in Paint, and localized image noise!
    """)
