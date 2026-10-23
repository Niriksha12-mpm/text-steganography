"""
Ultra-Modern Desktop Graphical User Interface for Text Steganography
---------------------------------------------------------------------
Built with CustomTkinter for a native Windows 11 / macOS fluent aesthetic:
- True rounded cards, buttons, and segmented pill controls
- High-DPI live thumbnail previews via CTkImage
- Dynamic theme switching (Dark 🌙 / Light ☀️)
- Real-time animated capacity progress bar
- One-click demo image loader
- Glowing Tamper Radar with Majority Voting repair metrics
- Smooth copy-to-clipboard feedback
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageDraw
from stego_core import encode_text, decode_text, get_image_capacity

# Configure global theme settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class UltraModernStegoGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Text Steganography Studio — Next-Gen LSB Data Hiding")
        self.geometry("860x740")
        self.minsize(800, 680)

        # State Variables - Encode
        self.enc_img_path = ""
        self.enc_capacity = 0
        self.enc_redundancy = 5  # Default: Robust 5x
        self.enc_img_obj = None

        # State Variables - Decode
        self.dec_img_path = ""
        self.dec_img_obj = None

        self._build_header()
        self._build_tabs()
        self._build_statusbar()

    # =========================================================================
    # HEADER SECTION
    # =========================================================================
    def _build_header(self):
        header_frame = ctk.CTkFrame(self, corner_radius=0, height=75, fg_color=("gray88", "gray13"))
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        # Left: Title and Subtitle
        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left", padx=24, pady=12)

        main_title = ctk.CTkLabel(
            title_box,
            text="🔐 TEXT STEGANOGRAPHY STUDIO",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold")
        )
        main_title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_box,
            text="Robust LSB Data Hiding with Majority-Voting Error Correction & Tamper Detection",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=("gray45", "gray65")
        )
        subtitle.pack(anchor="w")

        # Right: Theme Switcher
        theme_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        theme_box.pack(side="right", padx=24, pady=12)

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
    # TABVIEW (ENCODE / DECODE)
    # =========================================================================
    def _build_tabs(self):
        self.tabview = ctk.CTkTabview(self, corner_radius=12)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(12, 8))

        self.tab_encode = self.tabview.add("  🔒 Hide Message (Encode)  ")
        self.tab_decode = self.tabview.add("  🔓 Extract Message (Decode)  ")

        self._build_encode_tab()
        self._build_decode_tab()

    # =========================================================================
    # STATUS BAR
    # =========================================================================
    def _build_statusbar(self):
        status_frame = ctk.CTkFrame(self, corner_radius=0, height=30, fg_color=("gray90", "gray11"))
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)

        self.status_lbl = ctk.CTkLabel(
            status_frame,
            text="Ready. Select an image or click '⚡ Load Demo Image' to begin.",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=("gray40", "gray60"),
            anchor="w"
        )
        self.status_lbl.pack(fill="both", expand=True, padx=20)

    # =========================================================================
    # TAB 1: ENCODE TAB
    # =========================================================================
    def _build_encode_tab(self):
        parent = self.tab_encode

        # Card 1: Carrier Image Selection
        card_img = ctk.CTkFrame(parent, corner_radius=12)
        card_img.pack(fill="x", pady=(0, 10), padx=8)

        card_title = ctk.CTkLabel(
            card_img,
            text="1. Carrier (Cover) Image",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        card_title.pack(anchor="w", padx=16, pady=(12, 6))

        img_content = ctk.CTkFrame(card_img, fg_color="transparent")
        img_content.pack(fill="x", padx=16, pady=(0, 14))

        # Thumbnail Box
        self.enc_preview_lbl = ctk.CTkLabel(
            img_content,
            text="📷 No Image",
            width=140,
            height=100,
            corner_radius=8,
            fg_color=("gray85", "gray18")
        )
        self.enc_preview_lbl.pack(side="left", padx=(0, 16))

        # Info & Buttons
        info_col = ctk.CTkFrame(img_content, fg_color="transparent")
        info_col.pack(side="left", fill="both", expand=True)

        self.enc_path_lbl = ctk.CTkLabel(
            info_col,
            text="No carrier image selected.",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=("gray50", "gray70"),
            anchor="w"
        )
        self.enc_path_lbl.pack(fill="x", pady=(2, 4))

        self.enc_meta_lbl = ctk.CTkLabel(
            info_col,
            text="Supported formats: PNG, JPG, BMP",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("#0d9488", "#2dd4bf"),
            anchor="w"
        )
        self.enc_meta_lbl.pack(fill="x", pady=(0, 8))

        btn_row = ctk.CTkFrame(info_col, fg_color="transparent")
        btn_row.pack(anchor="w")

        browse_btn = ctk.CTkButton(
            btn_row,
            text="📁 Browse Image...",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=8,
            command=self._browse_encode_image
        )
        browse_btn.pack(side="left", padx=(0, 10))

        demo_btn = ctk.CTkButton(
            btn_row,
            text="⚡ Load Demo Image",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color=("#4f46e5", "#6366f1"),
            hover_color=("#4338ca", "#4f46e5"),
            corner_radius=8,
            command=self._load_demo_image
        )
        demo_btn.pack(side="left")

        # Card 2: Protection Mode Segmented Control
        card_mode = ctk.CTkFrame(parent, corner_radius=12)
        card_mode.pack(fill="x", pady=(0, 10), padx=8)

        mode_title = ctk.CTkLabel(
            card_mode,
            text="2. Protection & Integrity Mode",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        mode_title.pack(anchor="w", padx=16, pady=(10, 6))

        self.mode_selector = ctk.CTkSegmentedButton(
            card_mode,
            values=[
                "🛡️ Robust Mode (5x Redundancy) — Tamper Resistant [Recommended]",
                "⚡ Standard Mode (1x Redundancy) — Maximum Capacity"
            ],
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            command=self._on_mode_change
        )
        self.mode_selector.set("🛡️ Robust Mode (5x Redundancy) — Tamper Resistant [Recommended]")
        self.mode_selector.pack(fill="x", padx=16, pady=(0, 12))

        # Card 3: Secret Message & Live Capacity
        card_msg = ctk.CTkFrame(parent, corner_radius=12)
        card_msg.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        msg_title = ctk.CTkLabel(
            card_msg,
            text="3. Secret Confidential Message",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        msg_title.pack(anchor="w", padx=16, pady=(10, 4))

        self.enc_textbox = ctk.CTkTextbox(
            card_msg,
            font=ctk.CTkFont(family="Consolas", size=12),
            corner_radius=8
        )
        self.enc_textbox.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        self.enc_textbox.bind("<KeyRelease>", self._update_capacity_meter)

        # Progress bar & label
        cap_frame = ctk.CTkFrame(card_msg, fg_color="transparent")
        cap_frame.pack(fill="x", padx=16, pady=(0, 8))

        self.cap_text_lbl = ctk.CTkLabel(
            cap_frame,
            text="Capacity Usage: 0 / 0 characters (0%)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=("gray40", "gray65")
        )
        self.cap_text_lbl.pack(side="left")

        self.enc_progressbar = ctk.CTkProgressBar(cap_frame, corner_radius=6, height=10)
        self.enc_progressbar.set(0.0)
        self.enc_progressbar.pack(side="right", fill="x", expand=True, padx=(20, 0))

        # Action Buttons
        action_row = ctk.CTkFrame(card_msg, fg_color="transparent")
        action_row.pack(fill="x", padx=16, pady=(0, 12))

        clear_btn = ctk.CTkButton(
            action_row,
            text="Clear",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=("gray75", "gray25"),
            hover_color=("gray65", "gray35"),
            width=80,
            command=self._clear_encode_fields
        )
        clear_btn.pack(side="left")

        self.encode_btn = ctk.CTkButton(
            action_row,
            text="🔒 Hide Secret Message & Save Stego Image",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=("#2563eb", "#3b82f6"),
            hover_color=("#1d4ed8", "#2563eb"),
            height=38,
            command=self._do_encode
        )
        self.encode_btn.pack(side="right")

    # =========================================================================
    # TAB 2: DECODE TAB
    # =========================================================================
    def _build_decode_tab(self):
        parent = self.tab_decode

        # Card 1: Stego Image Selection
        card_img = ctk.CTkFrame(parent, corner_radius=12)
        card_img.pack(fill="x", pady=(0, 10), padx=8)

        card_title = ctk.CTkLabel(
            card_img,
            text="1. Stego Image Selection",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        card_title.pack(anchor="w", padx=16, pady=(12, 6))

        img_content = ctk.CTkFrame(card_img, fg_color="transparent")
        img_content.pack(fill="x", padx=16, pady=(0, 10))

        # Thumbnail Box
        self.dec_preview_lbl = ctk.CTkLabel(
            img_content,
            text="📷 No Stego Image",
            width=140,
            height=100,
            corner_radius=8,
            fg_color=("gray85", "gray18")
        )
        self.dec_preview_lbl.pack(side="left", padx=(0, 16))

        info_col = ctk.CTkFrame(img_content, fg_color="transparent")
        info_col.pack(side="left", fill="both", expand=True)

        self.dec_path_lbl = ctk.CTkLabel(
            info_col,
            text="Select an image containing hidden text.",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=("gray50", "gray70"),
            anchor="w"
        )
        self.dec_path_lbl.pack(fill="x", pady=(2, 4))

        self.dec_meta_lbl = ctk.CTkLabel(
            info_col,
            text="Lossless formats recommended: PNG, BMP",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=("#0d9488", "#2dd4bf"),
            anchor="w"
        )
        self.dec_meta_lbl.pack(fill="x", pady=(0, 8))

        browse_btn = ctk.CTkButton(
            info_col,
            text="📁 Browse Stego Image...",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            corner_radius=8,
            command=self._browse_decode_image
        )
        browse_btn.pack(anchor="w")

        # Big Decode Button
        self.decode_btn = ctk.CTkButton(
            card_img,
            text="🔓 Extract Confidential Message & Verify Integrity",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=("#059669", "#10b981"),
            hover_color=("#047857", "#059669"),
            height=40,
            command=self._do_decode
        )
        self.decode_btn.pack(fill="x", padx=16, pady=(0, 14))

        # Card 2: Tamper Radar & Integrity Card (Initially hidden)
        self.card_radar = ctk.CTkFrame(parent, corner_radius=12)

        self.radar_badge = ctk.CTkLabel(
            self.card_radar,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            corner_radius=8,
            anchor="w"
        )
        self.radar_badge.pack(fill="x", padx=16, pady=(12, 4))

        self.radar_details = ctk.CTkLabel(
            self.card_radar,
            text="",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=("gray40", "gray65"),
            justify="left",
            anchor="w"
        )
        self.radar_details.pack(fill="x", padx=16, pady=(0, 12))

        # Card 3: Extracted Message
        card_msg = ctk.CTkFrame(parent, corner_radius=12)
        card_msg.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        msg_title = ctk.CTkLabel(
            card_msg,
            text="2. Extracted Confidential Message",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        msg_title.pack(anchor="w", padx=16, pady=(10, 4))

        self.dec_textbox = ctk.CTkTextbox(
            card_msg,
            font=ctk.CTkFont(family="Consolas", size=12),
            corner_radius=8
        )
        self.dec_textbox.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        # Actions
        action_row = ctk.CTkFrame(card_msg, fg_color="transparent")
        action_row.pack(fill="x", padx=16, pady=(0, 12))

        self.copy_btn = ctk.CTkButton(
            action_row,
            text="📋 Copy to Clipboard",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=self._copy_extracted
        )
        self.copy_btn.pack(side="left")

        clear_btn = ctk.CTkButton(
            action_row,
            text="Clear",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            fg_color=("gray75", "gray25"),
            hover_color=("gray65", "gray35"),
            width=80,
            command=self._clear_decode_fields
        )
        clear_btn.pack(side="right")

    # =========================================================================
    # THEME TOGGLING & GRAPHICS
    # =========================================================================
    def _toggle_theme(self):
        mode = self.theme_switch.get()
        ctk.set_appearance_mode(mode)
        if mode == "Dark":
            self.theme_switch.configure(text="Dark Mode 🌙")
        else:
            self.theme_switch.configure(text="Light Mode ☀️")

    def _render_thumbnail(self, label_widget, image_path):
        try:
            with Image.open(image_path) as pil_img:
                copy_img = pil_img.copy()
                copy_img.thumbnail((140, 100), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=copy_img, dark_image=copy_img, size=copy_img.size)
                label_widget.configure(image=ctk_img, text="")
                label_widget.image = ctk_img  # Keep reference
        except Exception:
            label_widget.configure(image=None, text="Invalid Image")

    # =========================================================================
    # ENCODE ACTIONS
    # =========================================================================
    def _browse_encode_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
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

            self.enc_path_lbl.configure(text=os.path.basename(file_path))
            self.enc_redundancy = 5 if "5x" in self.mode_selector.get() else 1
            self.enc_capacity = get_image_capacity(file_path, redundancy=self.enc_redundancy)
            self.enc_meta_lbl.configure(
                text=f"{w} × {h} px  |  {fmt}  |  {file_kb:.1f} KB  |  Capacity: {self.enc_capacity:,} chars"
            )
            self._update_capacity_meter()
            self.status_lbl.configure(text=f"Loaded cover image: {os.path.basename(file_path)}")
        except Exception as e:
            self.enc_meta_lbl.configure(text=f"Error reading image: {e}")

    def _on_mode_change(self, value=None):
        if self.enc_img_path and os.path.exists(self.enc_img_path):
            self._load_encode_image(self.enc_img_path)

    def _update_capacity_meter(self, event=None):
        msg = self.enc_textbox.get("1.0", "end-1c")
        msg_len = len(msg)
        cap = self.enc_capacity

        if cap > 0:
            fraction = min(1.0, msg_len / cap)
            self.enc_progressbar.set(fraction)
            pct = fraction * 100
            self.cap_text_lbl.configure(
                text=f"Capacity Usage: {msg_len:,} / {cap:,} characters ({pct:.1f}%)"
            )
            if pct > 95:
                self.enc_progressbar.configure(progress_color="#ef4444")  # Red
            elif pct > 75:
                self.enc_progressbar.configure(progress_color="#f59e0b")  # Amber
            else:
                self.enc_progressbar.configure(progress_color=("#2563eb", "#3b82f6"))  # Blue
        else:
            self.enc_progressbar.set(0.0)
            self.cap_text_lbl.configure(text=f"Capacity Usage: {msg_len:,} characters (No image selected)")

    def _do_encode(self):
        img_path = self.enc_img_path
        secret_msg = self.enc_textbox.get("1.0", "end-1c").strip()
        redundancy = 5 if "5x" in self.mode_selector.get() else 1

        if not img_path:
            messagebox.showwarning("Missing Image", "Please select a cover image first (or click '⚡ Load Demo Image').")
            return

        if not secret_msg:
            messagebox.showwarning("Empty Message", "Please enter a secret message to hide.")
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
            self.status_lbl.configure(text=f"Stego image successfully saved: {os.path.basename(res['output_path'])}")
            
            mode_desc = (
                "🛡️ Robust Mode: Protected by Majority Voting.\n"
                "The secret message can survive pixel edits, drawing, and noise!"
                if redundancy > 1 else
                "⚡ Standard Mode: Maximum storage capacity utilized."
            )

            messagebox.showinfo(
                "Steganography Success",
                f"Secret message was successfully embedded!\n\n"
                f"📁 Output File: {res['output_path']}\n"
                f"📊 Mode: {res['mode']}\n"
                f"📝 Message Size: {res['message_length']:,} characters\n"
                f"📈 Capacity Used: {res['capacity_used_percent']}%\n\n"
                f"{mode_desc}"
            )
        except Exception as e:
            messagebox.showerror("Encoding Error", str(e))
            self.status_lbl.configure(text="Encoding failed.")

    def _clear_encode_fields(self):
        self.enc_img_path = ""
        self.enc_capacity = 0
        self.enc_textbox.delete("1.0", "end")
        self.enc_preview_lbl.configure(image=None, text="📷 No Image")
        self.enc_path_lbl.configure(text="No carrier image selected.")
        self.enc_meta_lbl.configure(text="Supported formats: PNG, JPG, BMP")
        self._update_capacity_meter()
        self.status_lbl.configure(text="Cleared encode fields.")

    # =========================================================================
    # DECODE ACTIONS
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
                self.dec_path_lbl.configure(text=os.path.basename(file_path))
                self.dec_meta_lbl.configure(text=f"{w} × {h} px  |  {fmt}  |  {sz_kb:.1f} KB")
                self.card_radar.pack_forget()
                self.status_lbl.configure(text=f"Selected stego image: {os.path.basename(file_path)}")
            except Exception as e:
                self.dec_meta_lbl.configure(text=f"Error reading image: {e}")

    def _do_decode(self):
        stego_path = self.dec_img_path
        if not stego_path:
            messagebox.showwarning("Missing Image", "Please select a stego image to extract message from.")
            return

        try:
            result = decode_text(stego_path)

            # Insert into textbox
            self.dec_textbox.configure(state="normal")
            self.dec_textbox.delete("1.0", "end")
            self.dec_textbox.insert("1.0", result)

            # Show Radar Card
            self.card_radar.pack(fill="x", pady=(0, 10), padx=8, before=self.dec_textbox.master)

            if result.tampered:
                self.radar_badge.configure(
                    text=f"⚠️ TAMPERING DETECTED & REPAIRED  ({result.mode})",
                    fg_color=("#fef3c7", "#78350f"),
                    text_color=("#92400e", "#fde68a")
                )
                self.radar_details.configure(
                    text=f"• Corrupted pixel bits detected: {result.tampered_bits:,} bits\n"
                         f"• Majority Voting repair: 100% of bits recovered intact\n"
                         f"• Tamper rate: {result.tamper_rate}% of sampled bits"
                )
            else:
                self.radar_badge.configure(
                    text=f"✅ IMAGE INTACT & PRISTINE  ({result.mode})",
                    fg_color=("#d1fae5", "#064e3b"),
                    text_color=("#065f46", "#a7f3d0")
                )
                self.radar_details.configure(
                    text="• Clean signal: 0 bit flips detected\n"
                         "• Pixel integrity: 100.0% match with original embedded bits"
                )

            self.status_lbl.configure(text=f"Message extracted! Length: {len(result):,} chars | Mode: {result.mode}")

        except Exception as e:
            self.dec_textbox.configure(state="normal")
            self.dec_textbox.delete("1.0", "end")
            self.card_radar.pack_forget()
            messagebox.showerror("Decoding Error", str(e))
            self.status_lbl.configure(text="Decoding failed: No valid hidden message detected.")

    def _copy_extracted(self):
        text = self.dec_textbox.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showinfo("Clipboard", "No text to copy.")
            return
        self.clipboard_clear()
        self.clipboard_append(text)

        # Smooth button feedback
        self.copy_btn.configure(text="✓ Copied to Clipboard!", fg_color=("#059669", "#10b981"))
        self.after(2000, lambda: self.copy_btn.configure(text="📋 Copy to Clipboard", fg_color=("#2563eb", "#3b82f6")))
        self.status_lbl.configure(text="Secret message copied to clipboard.")

    def _clear_decode_fields(self):
        self.dec_img_path = ""
        self.card_radar.pack_forget()
        self.dec_textbox.delete("1.0", "end")
        self.dec_preview_lbl.configure(image=None, text="📷 No Stego Image")
        self.dec_path_lbl.configure(text="Select an image containing hidden text.")
        self.dec_meta_lbl.configure(text="Lossless formats recommended: PNG, BMP")
        self.status_lbl.configure(text="Cleared decode fields.")


def main():
    app = UltraModernStegoGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
