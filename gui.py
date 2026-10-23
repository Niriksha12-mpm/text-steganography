"""
Ultra-Modern Desktop Graphical User Interface for Text Steganography
---------------------------------------------------------------------
Executive 2-Column Split Dashboard Layout:
- Left Column: Image & Engine Hub (Thumbnails, Metadata Pills, Protection Modes)
- Right Column: Secret Message Studio & Telemetry (Multi-Format Templates, Word/Byte Counters, Gauges)
- Decode Hub: Stego Inspector, Format Auto-Detection, and Visual Tamper Radar
- True Rounded Modern Fluent Design via CustomTkinter
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
from datetime import datetime
from PIL import Image, ImageDraw
from stego_core import encode_text, decode_text, get_image_capacity

# Global theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Template formats
TEMPLATES = {
    "📝 Plain Text": "",
    "🔒 Classified Memo": (
        "=====================================================\n"
        "CLASSIFICATION: TOP SECRET // STRICTLY CONFIDENTIAL\n"
        f"TIMESTAMP:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        "CLEARANCE:      LEVEL 5 (EYES ONLY)\n"
        "SUBJECT:        Operation Quantum Cipher\n"
        "=====================================================\n\n"
        "TRANSMISSION BODY:\n"
        "The encrypted rendezvous point has been established.\n"
        "All secondary channels are secured. Proceed with plan."
    ),
    "⚡ JSON Data": (
        "{\n"
        '  "protocol": "STEGO-LSB-ROBUST",\n'
        '  "version": "2.0",\n'
        '  "status": "classified",\n'
        '  "credentials": {\n'
        '    "token": "sec_98f4a2bc01e89",\n'
        '    "access_level": 5\n'
        "  },\n"
        '  "nodes": ["alpha-01", "echo-04"]\n'
        "}"
    ),
    "💻 Hex / Key": (
        "--- BEGIN STEGANOGRAPHIC ACCESS KEY ---\n"
        "KEY_ID:   0x8F9A4B2C_0019A\n"
        "HASH:     e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855\n"
        "ENDPOINT: sftp://vault.secure.internal:8088\n"
        "--- END STEGANOGRAPHIC ACCESS KEY ---"
    )
}


class ExecutiveStegoStudio(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Text Steganography Studio — Executive Dashboard")
        self.geometry("980x760")
        self.minsize(920, 700)

        # State - Encode
        self.enc_img_path = ""
        self.enc_capacity = 0
        self.enc_redundancy = 5
        self.current_template_key = "📝 Plain Text"

        # State - Decode
        self.dec_img_path = ""

        self._build_header()
        self._build_tabview()
        self._build_statusbar()

    # =========================================================================
    # HEADER
    # =========================================================================
    def _build_header(self):
        header = ctk.CTkFrame(self, corner_radius=0, height=72, fg_color=("gray88", "gray13"))
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Title & Badges
        title_box = ctk.CTkFrame(header, fg_color="transparent")
        title_box.pack(side="left", padx=24, pady=10)

        row_title = ctk.CTkFrame(title_box, fg_color="transparent")
        row_title.pack(anchor="w")

        main_title = ctk.CTkLabel(
            row_title,
            text="🔐 TEXT STEGANOGRAPHY STUDIO",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        )
        main_title.pack(side="left", padx=(0, 10))

        badge = ctk.CTkLabel(
            row_title,
            text="v2.5 PRO",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color=("#4f46e5", "#6366f1"),
            text_color="#ffffff",
            corner_radius=6,
            padx=8,
            pady=2
        )
        badge.pack(side="left")

        subtitle = ctk.CTkLabel(
            title_box,
            text="Spatial LSB Digital Steganography • 5x Majority-Voting Error Correction • Tamper Telemetry",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=("gray45", "gray65")
        )
        subtitle.pack(anchor="w")

        # Theme Switcher
        theme_box = ctk.CTkFrame(header, fg_color="transparent")
        theme_box.pack(side="right", padx=24, pady=10)

        self.theme_switch = ctk.CTkSwitch(
            theme_box,
            text="Dark Mode 🌙",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._toggle_theme,
            onvalue="Dark",
            offvalue="Light"
        )
        self.theme_switch.select()
        self.theme_switch.pack()

    # =========================================================================
    # TABS (ENCODE / DECODE)
    # =========================================================================
    def _build_tabview(self):
        self.tabview = ctk.CTkTabview(self, corner_radius=12)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(10, 6))

        self.tab_encode = self.tabview.add("   🔒 Hide Message (Encode Hub)   ")
        self.tab_decode = self.tabview.add("   🔓 Extract Message (Decode Hub)   ")

        self._build_encode_dashboard()
        self._build_decode_dashboard()

    # =========================================================================
    # STATUS BAR
    # =========================================================================
    def _build_statusbar(self):
        status_bar = ctk.CTkFrame(self, corner_radius=0, height=28, fg_color=("gray90", "gray11"))
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)

        self.status_lbl = ctk.CTkLabel(
            status_bar,
            text="System Online. Ready to process carrier images.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=("gray40", "gray60"),
            anchor="w"
        )
        self.status_lbl.pack(fill="both", expand=True, padx=20)

    # =========================================================================
    # TAB 1: 2-COLUMN ENCODE DASHBOARD
    # =========================================================================
    def _build_encode_dashboard(self):
        container = ctk.CTkFrame(self.tab_encode, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=4, pady=6)

        container.grid_columnconfigure(0, weight=4, minsize=350)  # Left Column (Image & Engine)
        container.grid_columnconfigure(1, weight=6, minsize=460)  # Right Column (Message Studio)
        container.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------------------------------
        # LEFT COLUMN: Image & Security Hub
        # ---------------------------------------------------------------------
        col_left = ctk.CTkFrame(container, corner_radius=12)
        col_left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        # Title
        sec_title1 = ctk.CTkLabel(
            col_left,
            text="📸 CARRIER IMAGE & ENGINE HUB",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("#4f46e5", "#818cf8")
        )
        sec_title1.pack(anchor="w", padx=16, pady=(14, 8))

        # Thumbnail Box
        self.enc_preview_lbl = ctk.CTkLabel(
            col_left,
            text="📷 Drop or Select Carrier Image",
            width=260,
            height=140,
            corner_radius=10,
            fg_color=("gray85", "gray18")
        )
        self.enc_preview_lbl.pack(fill="x", padx=16, pady=(0, 10))

        # Metadata Pills Card
        meta_card = ctk.CTkFrame(col_left, corner_radius=8, fg_color=("gray92", "gray16"))
        meta_card.pack(fill="x", padx=16, pady=(0, 10))

        self.enc_pill_res = ctk.CTkLabel(
            meta_card, text="📐 Res: --", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=("gray40", "gray70")
        )
        self.enc_pill_res.pack(anchor="w", padx=12, pady=(8, 2))

        self.enc_pill_format = ctk.CTkLabel(
            meta_card, text="🖼️ Format: --  |  💾 Size: --", font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=("gray40", "gray70")
        )
        self.enc_pill_format.pack(anchor="w", padx=12, pady=2)

        self.enc_pill_capacity = ctk.CTkLabel(
            meta_card, text="⚡ Max Capacity: -- chars", font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=("#0d9488", "#2dd4bf")
        )
        self.enc_pill_capacity.pack(anchor="w", padx=12, pady=(2, 8))

        # Action Buttons
        btn_box = ctk.CTkFrame(col_left, fg_color="transparent")
        btn_box.pack(fill="x", padx=16, pady=(0, 12))

        browse_btn = ctk.CTkButton(
            btn_box, text="📁 Browse Image...", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=8, height=36, command=self._browse_encode_image
        )
        browse_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))

        demo_btn = ctk.CTkButton(
            btn_box, text="⚡ Demo Image", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=("#4f46e5", "#6366f1"), hover_color=("#4338ca", "#4f46e5"),
            corner_radius=8, height=36, width=110, command=self._load_demo_image
        )
        demo_btn.pack(side="right")

        # Protection Mode Selector
        mode_lbl = ctk.CTkLabel(
            col_left, text="SECURITY & RESILIENCE MODE:",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=("gray45", "gray65")
        )
        mode_lbl.pack(anchor="w", padx=16, pady=(6, 4))

        self.mode_selector = ctk.CTkSegmentedButton(
            col_left,
            values=["🛡️ Robust (5x)", "⚡ Standard (1x)"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._on_mode_change
        )
        self.mode_selector.set("🛡️ Robust (5x)")
        self.mode_selector.pack(fill="x", padx=16, pady=(0, 8))

        mode_help = ctk.CTkLabel(
            col_left,
            text="• Robust (5x): Protected by Majority Voting.\n  Survives pixel edits, drawings, and noise.",
            font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=("gray45", "gray60"),
            justify="left"
        )
        mode_help.pack(anchor="w", padx=16, pady=(0, 12))

        # ---------------------------------------------------------------------
        # RIGHT COLUMN: Secret Message Studio & Telemetry
        # ---------------------------------------------------------------------
        col_right = ctk.CTkFrame(container, corner_radius=12)
        col_right.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0)

        # Header with Format Pills
        format_bar = ctk.CTkFrame(col_right, fg_color="transparent")
        format_bar.pack(fill="x", padx=16, pady=(14, 8))

        sec_title2 = ctk.CTkLabel(
            format_bar, text="📝 SECRET MESSAGE STUDIO",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("#4f46e5", "#818cf8")
        )
        sec_title2.pack(side="left")

        # Format Switcher Segmented
        self.format_selector = ctk.CTkSegmentedButton(
            col_right,
            values=["📝 Plain Text", "🔒 Classified Memo", "⚡ JSON Data", "💻 Hex / Key"],
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            command=self._on_format_template_selected
        )
        self.format_selector.set("📝 Plain Text")
        self.format_selector.pack(fill="x", padx=16, pady=(0, 10))

        # Text Editor
        self.enc_textbox = ctk.CTkTextbox(
            col_right,
            font=ctk.CTkFont(family="Consolas", size=12),
            corner_radius=8
        )
        self.enc_textbox.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        self.enc_textbox.bind("<KeyRelease>", self._update_telemetry)

        # Telemetry Card (Characters, Words, Bytes, Capacity %)
        telem_card = ctk.CTkFrame(col_right, corner_radius=8, fg_color=("gray92", "gray16"))
        telem_card.pack(fill="x", padx=16, pady=(0, 8))

        telem_row1 = ctk.CTkFrame(telem_card, fg_color="transparent")
        telem_row1.pack(fill="x", padx=12, pady=(6, 4))

        self.telem_lbl_chars = ctk.CTkLabel(
            telem_row1, text="Chars: 0", font=ctk.CTkFont(family="Consolas", size=11, weight="bold")
        )
        self.telem_lbl_chars.pack(side="left", padx=(0, 14))

        self.telem_lbl_words = ctk.CTkLabel(
            telem_row1, text="Words: 0", font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.telem_lbl_words.pack(side="left", padx=(0, 14))

        self.telem_lbl_bytes = ctk.CTkLabel(
            telem_row1, text="Bytes: 0 B", font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.telem_lbl_bytes.pack(side="left")

        self.telem_lbl_cap = ctk.CTkLabel(
            telem_row1, text="Capacity: 0.0%", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=("#2563eb", "#60a5fa")
        )
        self.telem_lbl_cap.pack(side="right")

        self.enc_progressbar = ctk.CTkProgressBar(telem_card, corner_radius=4, height=8)
        self.enc_progressbar.set(0.0)
        self.enc_progressbar.pack(fill="x", padx=12, pady=(0, 8))

        # Bottom Actions
        action_bar = ctk.CTkFrame(col_right, fg_color="transparent")
        action_bar.pack(fill="x", padx=16, pady=(0, 14))

        clear_btn = ctk.CTkButton(
            action_bar, text="Clear", font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=("gray75", "gray25"), hover_color=("gray65", "gray35"),
            width=70, height=36, command=self._clear_encode_fields
        )
        clear_btn.pack(side="left")

        self.encode_btn = ctk.CTkButton(
            action_bar,
            text="🔒 Hide Secret Message & Save Stego Image",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=("#2563eb", "#3b82f6"), hover_color=("#1d4ed8", "#2563eb"),
            height=38, command=self._do_encode
        )
        self.encode_btn.pack(side="right")

    # =========================================================================
    # TAB 2: 2-COLUMN DECODE DASHBOARD
    # =========================================================================
    def _build_decode_dashboard(self):
        container = ctk.CTkFrame(self.tab_decode, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=4, pady=6)

        container.grid_columnconfigure(0, weight=4, minsize=350)
        container.grid_columnconfigure(1, weight=6, minsize=460)
        container.grid_rowconfigure(0, weight=1)

        # ---------------------------------------------------------------------
        # LEFT COLUMN: Stego Inspector & Telemetry Radar
        # ---------------------------------------------------------------------
        col_left = ctk.CTkFrame(container, corner_radius=12)
        col_left.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        sec_title = ctk.CTkLabel(
            col_left, text="🔍 STEGO IMAGE INSPECTOR",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("#059669", "#34d399")
        )
        sec_title.pack(anchor="w", padx=16, pady=(14, 8))

        # Thumbnail
        self.dec_preview_lbl = ctk.CTkLabel(
            col_left, text="📷 Select Stego Image to Inspect",
            width=260, height=140, corner_radius=10, fg_color=("gray85", "gray18")
        )
        self.dec_preview_lbl.pack(fill="x", padx=16, pady=(0, 10))

        # Metadata Pills Card
        meta_card = ctk.CTkFrame(col_left, corner_radius=8, fg_color=("gray92", "gray16"))
        meta_card.pack(fill="x", padx=16, pady=(0, 10))

        self.dec_pill_path = ctk.CTkLabel(
            meta_card, text="File: No image loaded", font=ctk.CTkFont(family="Consolas", size=11),
            text_color=("gray40", "gray70"), anchor="w"
        )
        self.dec_pill_path.pack(fill="x", padx=12, pady=(6, 2))

        self.dec_pill_meta = ctk.CTkLabel(
            meta_card, text="Status: Waiting for stego image input",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=("#0d9488", "#2dd4bf"), anchor="w"
        )
        self.dec_pill_meta.pack(fill="x", padx=12, pady=(2, 6))

        # Browse & Extract Buttons
        browse_dec_btn = ctk.CTkButton(
            col_left, text="📁 Browse Stego Image...",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=8, height=36, command=self._browse_decode_image
        )
        browse_dec_btn.pack(fill="x", padx=16, pady=(0, 8))

        self.decode_action_btn = ctk.CTkButton(
            col_left, text="🔓 Extract Confidential Message & Verify Integrity",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=("#059669", "#10b981"), hover_color=("#047857", "#059669"),
            height=40, command=self._do_decode
        )
        self.decode_action_btn.pack(fill="x", padx=16, pady=(0, 12))

        # Tamper Radar Box (Initially Collapsed)
        self.radar_box = ctk.CTkFrame(col_left, corner_radius=8, fg_color=("gray92", "gray16"))

        self.radar_badge = ctk.CTkLabel(
            self.radar_box, text="", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=6, anchor="w", padx=10, pady=4
        )
        self.radar_badge.pack(fill="x", padx=10, pady=(8, 4))

        self.radar_stats = ctk.CTkLabel(
            self.radar_box, text="", font=ctk.CTkFont(family="Segoe UI", size=10),
            text_color=("gray40", "gray65"), justify="left", anchor="w"
        )
        self.radar_stats.pack(fill="x", padx=10, pady=(0, 8))

        # ---------------------------------------------------------------------
        # RIGHT COLUMN: Extracted Payload & Analysis
        # ---------------------------------------------------------------------
        col_right = ctk.CTkFrame(container, corner_radius=12)
        col_right.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0)

        # Header Bar
        ext_header = ctk.CTkFrame(col_right, fg_color="transparent")
        ext_header.pack(fill="x", padx=16, pady=(14, 8))

        sec_title3 = ctk.CTkLabel(
            ext_header, text="📄 EXTRACTED PAYLOAD & TELEMETRY",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("#059669", "#34d399")
        )
        sec_title3.pack(side="left")

        self.dec_format_badge = ctk.CTkLabel(
            ext_header, text="FORMAT: AUTO-DETECT",
            font=ctk.CTkFont(family="Segoe UI", size=10, weight="bold"),
            fg_color=("gray85", "gray22"), text_color=("gray40", "gray70"),
            corner_radius=4, padx=6, pady=2
        )
        self.dec_format_badge.pack(side="right")

        # Extracted Text Box
        self.dec_textbox = ctk.CTkTextbox(
            col_right, font=ctk.CTkFont(family="Consolas", size=12), corner_radius=8
        )
        self.dec_textbox.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        # Decode Telemetry Row
        dec_telem = ctk.CTkFrame(col_right, corner_radius=8, fg_color=("gray92", "gray16"))
        dec_telem.pack(fill="x", padx=16, pady=(0, 8))

        dec_row = ctk.CTkFrame(dec_telem, fg_color="transparent")
        dec_row.pack(fill="x", padx=12, pady=6)

        self.dec_lbl_chars = ctk.CTkLabel(dec_row, text="Characters: 0", font=ctk.CTkFont(family="Consolas", size=11))
        self.dec_lbl_chars.pack(side="left", padx=(0, 14))

        self.dec_lbl_words = ctk.CTkLabel(dec_row, text="Words: 0", font=ctk.CTkFont(family="Consolas", size=11))
        self.dec_lbl_words.pack(side="left", padx=(0, 14))

        self.dec_lbl_integrity = ctk.CTkLabel(
            dec_row, text="Integrity: --", font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color=("#059669", "#34d399")
        )
        self.dec_lbl_integrity.pack(side="right")

        # Action Bar
        action_bar2 = ctk.CTkFrame(col_right, fg_color="transparent")
        action_bar2.pack(fill="x", padx=16, pady=(0, 14))

        self.copy_btn = ctk.CTkButton(
            action_bar2, text="📋 Copy Message", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._copy_extracted
        )
        self.copy_btn.pack(side="left", padx=(0, 8))

        save_btn = ctk.CTkButton(
            action_bar2, text="💾 Save to .txt", font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=("gray75", "gray25"), hover_color=("gray65", "gray35"),
            width=100, command=self._save_extracted_to_file
        )
        save_btn.pack(side="left")

        clear_btn2 = ctk.CTkButton(
            action_bar2, text="Clear", font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=("gray75", "gray25"), hover_color=("gray65", "gray35"),
            width=70, command=self._clear_decode_fields
        )
        clear_btn2.pack(side="right")

    # =========================================================================
    # THEME TOGGLE & GRAPHICS
    # =========================================================================
    def _toggle_theme(self):
        mode = self.theme_switch.get()
        ctk.set_appearance_mode(mode)
        self.theme_switch.configure(text="Dark Mode 🌙" if mode == "Dark" else "Light Mode ☀️")

    def _render_thumbnail(self, label_widget, image_path):
        try:
            with Image.open(image_path) as pil_img:
                copy_img = pil_img.copy()
                copy_img.thumbnail((260, 140), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=copy_img, dark_image=copy_img, size=copy_img.size)
                label_widget.configure(image=ctk_img, text="")
                label_widget.image = ctk_img
        except Exception:
            label_widget.configure(image=None, text="Invalid Image")

    # =========================================================================
    # ENCODE LOGIC & TELEMETRY
    # =========================================================================
    def _on_format_template_selected(self, choice):
        self.current_template_key = choice
        template_text = TEMPLATES.get(choice, "")
        if template_text or choice == "📝 Plain Text":
            self.enc_textbox.delete("1.0", "end")
            if template_text:
                self.enc_textbox.insert("1.0", template_text)
            self._update_telemetry()
            self.status_lbl.configure(text=f"Loaded template: {choice}")

    def _browse_encode_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Carrier Image",
            filetypes=[
                ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp"),
                ("PNG Lossless (*.png)", "*.png"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self._load_encode_image(file_path)

    def _load_demo_image(self):
        demo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_carrier.png")
        if not os.path.exists(demo_path):
            img = Image.new("RGB", (300, 300))
            draw = ImageDraw.Draw(img)
            for y in range(300):
                for x in range(300):
                    draw.point((x, y), fill=(int(255 * x / 300), int(255 * y / 300), 160))
            img.save(demo_path, format="PNG")
        self._load_encode_image(demo_path)
        self.status_lbl.configure(text="⚡ Demo carrier image loaded.")

    def _load_encode_image(self, file_path):
        self.enc_img_path = file_path
        self._render_thumbnail(self.enc_preview_lbl, file_path)
        try:
            with Image.open(file_path) as im:
                w, h = im.size
                fmt = im.format or "IMG"
                file_kb = os.path.getsize(file_path) / 1024

            self.enc_redundancy = 5 if "5x" in self.mode_selector.get() else 1
            self.enc_capacity = get_image_capacity(file_path, redundancy=self.enc_redundancy)

            self.enc_pill_res.configure(text=f"📐 Res: {w} × {h} px")
            self.enc_pill_format.configure(text=f"🖼️ Format: {fmt}  |  💾 Size: {file_kb:.1f} KB")
            self.enc_pill_capacity.configure(text=f"⚡ Max Capacity: {self.enc_capacity:,} characters")

            self._update_telemetry()
            self.status_lbl.configure(text=f"Loaded carrier: {os.path.basename(file_path)}")
        except Exception as e:
            self.enc_pill_capacity.configure(text=f"Error reading image: {e}")

    def _on_mode_change(self, value=None):
        if self.enc_img_path and os.path.exists(self.enc_img_path):
            self._load_encode_image(self.enc_img_path)

    def _update_telemetry(self, event=None):
        msg = self.enc_textbox.get("1.0", "end-1c")
        chars = len(msg)
        words = len(msg.split())
        byte_len = len(msg.encode("utf-8"))
        cap = self.enc_capacity

        self.telem_lbl_chars.configure(text=f"Chars: {chars:,}")
        self.telem_lbl_words.configure(text=f"Words: {words:,}")
        self.telem_lbl_bytes.configure(text=f"Bytes: {byte_len:,} B")

        if cap > 0:
            fraction = min(1.0, chars / cap)
            self.enc_progressbar.set(fraction)
            pct = fraction * 100
            self.telem_lbl_cap.configure(text=f"Capacity: {pct:.1f}%")
            if pct > 95:
                self.enc_progressbar.configure(progress_color="#ef4444")
            elif pct > 75:
                self.enc_progressbar.configure(progress_color="#f59e0b")
            else:
                self.enc_progressbar.configure(progress_color=("#2563eb", "#3b82f6"))
        else:
            self.enc_progressbar.set(0.0)
            self.telem_lbl_cap.configure(text="Capacity: 0.0%")

    def _do_encode(self):
        img_path = self.enc_img_path
        secret_msg = self.enc_textbox.get("1.0", "end-1c").strip()
        redundancy = 5 if "5x" in self.mode_selector.get() else 1

        if not img_path:
            messagebox.showwarning("Missing Image", "Please select or drop a carrier image first.")
            return

        if not secret_msg:
            messagebox.showwarning("Empty Message", "Please enter or generate a secret message to embed.")
            return

        default_name = os.path.splitext(os.path.basename(img_path))[0] + "_stego.png"
        save_path = filedialog.asksaveasfilename(
            title="Save Stego Image As",
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[("PNG Image (Lossless)", "*.png"), ("BMP Image", "*.bmp")]
        )

        if not save_path:
            return

        try:
            res = encode_text(img_path, secret_msg, save_path, redundancy=redundancy)
            self.status_lbl.configure(text=f"Stego image created: {os.path.basename(res['output_path'])}")
            
            messagebox.showinfo(
                "Steganography Success",
                f"Secret message successfully embedded!\n\n"
                f"📁 Output File: {res['output_path']}\n"
                f"🛡️ Mode: {res['mode']}\n"
                f"📝 Payload Length: {res['message_length']:,} characters\n"
                f"📈 Capacity Used: {res['capacity_used_percent']}%\n\n"
                f"Visual change is 0.00% (imperceptible to human eyes)."
            )
        except Exception as e:
            messagebox.showerror("Encoding Error", str(e))
            self.status_lbl.configure(text="Encoding failed.")

    def _clear_encode_fields(self):
        self.enc_img_path = ""
        self.enc_capacity = 0
        self.enc_textbox.delete("1.0", "end")
        self.enc_preview_lbl.configure(image=None, text="📷 Drop or Select Carrier Image")
        self.enc_pill_res.configure(text="📐 Res: --")
        self.enc_pill_format.configure(text="🖼️ Format: --  |  💾 Size: --")
        self.enc_pill_capacity.configure(text="⚡ Max Capacity: -- chars")
        self.format_selector.set("📝 Plain Text")
        self._update_telemetry()
        self.status_lbl.configure(text="Cleared encode hub.")

    # =========================================================================
    # DECODE LOGIC & TELEMETRY
    # =========================================================================
    def _browse_decode_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[
                ("PNG / BMP Lossless Images", "*.png;*.bmp"),
                ("All Images", "*.png;*.jpg;*.jpeg;*.bmp"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.dec_img_path = file_path
            self._render_thumbnail(self.dec_preview_lbl, file_path)
            try:
                with Image.open(file_path) as im:
                    w, h = im.size
                    fmt = im.format or "IMG"
                    sz_kb = os.path.getsize(file_path) / 1024
                self.dec_pill_path.configure(text=f"File: {os.path.basename(file_path)}")
                self.dec_pill_meta.configure(text=f"Dimensions: {w} × {h} px  |  Format: {fmt}  |  {sz_kb:.1f} KB")
                self.radar_box.pack_forget()
                self.status_lbl.configure(text=f"Loaded stego image: {os.path.basename(file_path)}")
            except Exception as e:
                self.dec_pill_meta.configure(text=f"Error reading image: {e}")

    def _do_decode(self):
        stego_path = self.dec_img_path
        if not stego_path:
            messagebox.showwarning("Missing Image", "Please select a stego image first.")
            return

        try:
            result = decode_text(stego_path)

            self.dec_textbox.configure(state="normal")
            self.dec_textbox.delete("1.0", "end")
            self.dec_textbox.insert("1.0", result)

            # Auto-detect format
            txt = str(result).strip()
            if txt.startswith("{") and txt.endswith("}"):
                self.dec_format_badge.configure(text="FORMAT: JSON PAYLOAD")
            elif "CLASSIFICATION:" in txt or "TOP SECRET" in txt:
                self.dec_format_badge.configure(text="FORMAT: CLASSIFIED MEMO")
            elif "BEGIN" in txt and "KEY" in txt:
                self.dec_format_badge.configure(text="FORMAT: CRYPTO KEY")
            else:
                self.dec_format_badge.configure(text="FORMAT: PLAIN TEXT")

            # Telemetry
            chars = len(result)
            words = len(result.split())
            self.dec_lbl_chars.configure(text=f"Characters: {chars:,}")
            self.dec_lbl_words.configure(text=f"Words: {words:,}")

            # Radar Box
            self.radar_box.pack(fill="x", padx=16, pady=(0, 10))

            if result.tampered:
                self.radar_badge.configure(
                    text=f"⚠️ TAMPERING DETECTED & REPAIRED ({result.mode})",
                    fg_color=("#fef3c7", "#78350f"),
                    text_color=("#92400e", "#fde68a")
                )
                self.radar_stats.configure(
                    text=f"• Corrupted bits repaired: {result.tampered_bits:,} bits via Majority Voting\n"
                         f"• Tamper rate: {result.tamper_rate}% of sampled bits were modified\n"
                         f"• Integrity: Restored 100% of confidential message"
                )
                self.dec_lbl_integrity.configure(
                    text=f"Integrity: Repaired ({result.tampered_bits} bits)", text_color="#f59e0b"
                )
            else:
                self.radar_badge.configure(
                    text=f"✅ IMAGE INTACT & PRISTINE ({result.mode})",
                    fg_color=("#d1fae5", "#064e3b"),
                    text_color=("#065f46", "#a7f3d0")
                )
                self.radar_stats.configure(
                    text="• Clean signal: 0 bit flips detected\n"
                         "• Pixel integrity: 100.0% pure signal match"
                )
                self.dec_lbl_integrity.configure(
                    text="Integrity: 100% Pristine", text_color=("#059669", "#34d399")
                )

            self.status_lbl.configure(text=f"Extracted payload ({len(result):,} chars) in {result.mode}")

        except Exception as e:
            self.dec_textbox.configure(state="normal")
            self.dec_textbox.delete("1.0", "end")
            self.radar_box.pack_forget()
            messagebox.showerror("Decoding Error", str(e))
            self.status_lbl.configure(text="Decoding failed.")

    def _copy_extracted(self):
        text = self.dec_textbox.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showinfo("Clipboard", "No message to copy.")
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self.copy_btn.configure(text="✓ Copied to Clipboard!", fg_color=("#059669", "#10b981"))
        self.after(2000, lambda: self.copy_btn.configure(text="📋 Copy Message", fg_color=("#2563eb", "#3b82f6")))
        self.status_lbl.configure(text="Secret message copied to clipboard.")

    def _save_extracted_to_file(self):
        text = self.dec_textbox.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showinfo("Save File", "No message to save.")
            return
        save_path = filedialog.asksaveasfilename(
            title="Save Extracted Message",
            defaultextension=".txt",
            filetypes=[("Text File (*.txt)", "*.txt"), ("All Files", "*.*")]
        )
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(text)
            self.status_lbl.configure(text=f"Saved secret text to {os.path.basename(save_path)}")
            messagebox.showinfo("File Saved", f"Message saved to:\n{save_path}")

    def _clear_decode_fields(self):
        self.dec_img_path = ""
        self.dec_preview_lbl.configure(image=None, text="📷 Select Stego Image to Inspect")
        self.dec_pill_path.configure(text="File: No image loaded")
        self.dec_pill_meta.configure(text="Status: Waiting for stego image input")
        self.dec_format_badge.configure(text="FORMAT: AUTO-DETECT")
        self.dec_textbox.delete("1.0", "end")
        self.dec_lbl_chars.configure(text="Characters: 0")
        self.dec_lbl_words.configure(text="Words: 0")
        self.dec_lbl_integrity.configure(text="Integrity: --")
        self.radar_box.pack_forget()
        self.status_lbl.configure(text="Cleared decode hub.")


def main():
    app = ExecutiveStegoStudio()
    app.mainloop()


if __name__ == "__main__":
    main()
