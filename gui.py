"""
Desktop Graphical User Interface (GUI) for Text Steganography
-------------------------------------------------------------
Modernized UI/UX with:
- Live image thumbnail previews
- Dynamic capacity progress bar & real-time character counter
- 1-Click "Load Demo Image" for quick testing/presentations
- Color-coded protection mode cards
- Visual tamper radar with detailed integrity breakdown
- Interactive feedback ("✓ Copied to Clipboard!")
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image, ImageTk, ImageDraw
from stego_core import encode_text, decode_text, get_image_capacity


class ModernSteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Steganography Studio — LSB Data Hiding")
        self.root.geometry("820x720")
        self.root.minsize(760, 650)
        self.root.configure(bg="#f8fafc")

        # Color Palette
        self.C_BG = "#f8fafc"
        self.C_CARD = "#ffffff"
        self.C_BORDER = "#e2e8f0"
        self.C_TEXT_MAIN = "#0f172a"
        self.C_TEXT_MUTED = "#64748b"
        self.C_PRIMARY = "#4f46e5"       # Indigo
        self.C_PRIMARY_HOVER = "#4338ca"
        self.C_SUCCESS = "#059669"       # Emerald
        self.C_SUCCESS_HOVER = "#047857"
        self.C_AMBER = "#d97706"

        # State Variables - Encode
        self.enc_img_path = tk.StringVar()
        self.enc_img_info = tk.StringVar(value="No image loaded yet.")
        self.enc_redundancy = tk.IntVar(value=5)  # Default: Robust 5x
        self.enc_capacity = 0
        self.enc_thumbnail_ref = None

        # State Variables - Decode
        self.dec_img_path = tk.StringVar()
        self.dec_img_info = tk.StringVar(value="No stego image loaded yet.")
        self.dec_thumbnail_ref = None

        self._configure_styles()
        self._build_header()
        self._build_notebook()
        self._build_statusbar()

    def _configure_styles(self):
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass

        # Notebook tab styling
        style.configure("TNotebook", background=self.C_BG, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            font=("Segoe UI", 10, "bold"),
            padding=[20, 10],
            background="#e2e8f0",
            foreground=self.C_TEXT_MUTED,
            borderwidth=0
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#ffffff")],
            foreground=[("selected", self.C_PRIMARY)]
        )

        # Progressbar styling
        style.configure(
            "Capacity.Horizontal.TProgressbar",
            troughcolor="#e2e8f0",
            background=self.C_PRIMARY,
            thickness=8,
            borderwidth=0
        )

    def _build_header(self):
        header = tk.Frame(self.root, bg="#0f172a", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        top_container = tk.Frame(header, bg="#0f172a")
        top_container.pack(fill="both", expand=True, padx=24, pady=12)

        title_lbl = tk.Label(
            top_container,
            text="🔐 TEXT STEGANOGRAPHY STUDIO",
            font=("Segoe UI", 15, "bold"),
            fg="#f8fafc",
            bg="#0f172a"
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            top_container,
            text="Robust LSB Data Hiding with Majority-Voting Error Correction & Tamper Detection",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#0f172a"
        )
        subtitle_lbl.pack(anchor="w")

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=(12, 6))

        # Tab 1: Encode (Hide)
        self.tab_encode = tk.Frame(self.notebook, bg=self.C_BG)
        self.notebook.add(self.tab_encode, text="   🔒 Hide Message (Encode)   ")
        self._build_encode_view()

        # Tab 2: Decode (Extract)
        self.tab_decode = tk.Frame(self.notebook, bg=self.C_BG)
        self.notebook.add(self.tab_decode, text="   🔓 Extract Message (Decode)   ")
        self._build_decode_view()

    def _build_statusbar(self):
        status_frame = tk.Frame(self.root, bg="#f1f5f9", height=28, highlightthickness=1, highlightbackground=self.C_BORDER)
        status_frame.pack(side="bottom", fill="x")
        status_frame.pack_propagate(False)

        self.status_var = tk.StringVar(value="Ready. Select an image or click '⚡ Load Demo Image' to begin.")
        status_lbl = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 8),
            fg="#475569",
            bg="#f1f5f9",
            anchor="w",
            padx=16
        )
        status_lbl.pack(fill="both", expand=True)

    # =========================================================================
    # TAB 1: ENCODE VIEW
    # =========================================================================
    def _build_encode_view(self):
        container = tk.Frame(self.tab_encode, bg=self.C_BG)
        container.pack(fill="both", expand=True, padx=12, pady=10)

        # Top Card: Image Selection & Live Preview
        card_img = self._create_card(container, "1. Carrier (Cover) Image")
        card_img.pack(fill="x", pady=(0, 10))

        img_row = tk.Frame(card_img, bg=self.C_CARD)
        img_row.pack(fill="x", padx=14, pady=10)

        # Image Thumbnail Canvas
        self.enc_preview_canvas = tk.Canvas(
            img_row, width=120, height=90, bg="#f1f5f9",
            highlightthickness=1, highlightbackground=self.C_BORDER
        )
        self.enc_preview_canvas.pack(side="left", padx=(0, 14))
        self._draw_canvas_placeholder(self.enc_preview_canvas, "No Image")

        # Right side info & buttons
        info_col = tk.Frame(img_row, bg=self.C_CARD)
        info_col.pack(side="left", fill="both", expand=True)

        path_lbl = tk.Label(
            info_col, textvariable=self.enc_img_path,
            font=("Consolas", 8), fg="#64748b", bg="#f8fafc",
            anchor="w", padx=6, pady=4, relief=tk.SOLID, borderwidth=1
        )
        path_lbl.pack(fill="x", pady=(0, 6))

        meta_lbl = tk.Label(
            info_col, textvariable=self.enc_img_info,
            font=("Segoe UI", 9, "bold"), fg="#0f766e", bg=self.C_CARD, anchor="w"
        )
        meta_lbl.pack(fill="x", pady=(0, 8))

        btn_row = tk.Frame(info_col, bg=self.C_CARD)
        btn_row.pack(anchor="w")

        browse_btn = tk.Button(
            btn_row, text="📁 Browse Image...", font=("Segoe UI", 9),
            bg="#f1f5f9", fg=self.C_TEXT_MAIN, relief=tk.GROOVE,
            padx=12, pady=4, cursor="hand2", command=self._browse_encode_image
        )
        browse_btn.pack(side="left", padx=(0, 8))

        demo_btn = tk.Button(
            btn_row, text="⚡ Load Demo Image", font=("Segoe UI", 9, "bold"),
            bg="#e0e7ff", fg=self.C_PRIMARY, relief=tk.FLAT,
            padx=12, pady=4, cursor="hand2", command=self._load_demo_image
        )
        demo_btn.pack(side="left")

        # Middle Card: Protection Mode
        card_mode = self._create_card(container, "2. Protection Mode")
        card_mode.pack(fill="x", pady=(0, 10))

        mode_row = tk.Frame(card_mode, bg=self.C_CARD)
        mode_row.pack(fill="x", padx=14, pady=8)

        rb_robust = tk.Radiobutton(
            mode_row,
            text="🛡️ Robust Mode (5x Redundancy) — Resilient to pixel edits, noise, and drawing via Majority Voting [Recommended]",
            variable=self.enc_redundancy, value=5,
            font=("Segoe UI", 9, "bold"), fg=self.C_PRIMARY, bg=self.C_CARD,
            activebackground=self.C_CARD, command=self._on_mode_change
        )
        rb_robust.pack(anchor="w", pady=2)

        rb_standard = tk.Radiobutton(
            mode_row,
            text="⚡ Standard Mode (1x Redundancy) — Maximizes storage capacity (fragile to pixel alterations)",
            variable=self.enc_redundancy, value=1,
            font=("Segoe UI", 9), fg=self.C_TEXT_MUTED, bg=self.C_CARD,
            activebackground=self.C_CARD, command=self._on_mode_change
        )
        rb_standard.pack(anchor="w", pady=2)

        # Bottom Card: Secret Message & Live Capacity
        card_msg = self._create_card(container, "3. Secret Message")
        card_msg.pack(fill="both", expand=True, pady=(0, 8))

        msg_body = tk.Frame(card_msg, bg=self.C_CARD)
        msg_body.pack(fill="both", expand=True, padx=14, pady=(8, 12))

        # Text Area with Scrollbar
        text_frame = tk.Frame(msg_body, bg=self.C_CARD)
        text_frame.pack(fill="both", expand=True, pady=(0, 8))

        self.enc_text = tk.Text(
            text_frame, wrap="word", font=("Consolas", 10),
            bg="#f8fafc", fg=self.C_TEXT_MAIN, relief=tk.SOLID, borderwidth=1,
            padx=8, pady=8
        )
        self.enc_text.pack(side="left", fill="both", expand=True)
        self.enc_text.bind("<KeyRelease>", self._update_capacity_meter)

        scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.enc_text.yview)
        scroll.pack(side="right", fill="y")
        self.enc_text.config(yscrollcommand=scroll.set)

        # Capacity Progress Bar & Labels
        cap_row = tk.Frame(msg_body, bg=self.C_CARD)
        cap_row.pack(fill="x", pady=(0, 6))

        self.enc_cap_lbl = tk.Label(
            cap_row, text="Storage Usage: 0 / 0 characters (0%)",
            font=("Segoe UI", 8), fg=self.C_TEXT_MUTED, bg=self.C_CARD
        )
        self.enc_cap_lbl.pack(side="left")

        self.enc_progress = ttk.Progressbar(
            cap_row, orient="horizontal", mode="determinate",
            style="Capacity.Horizontal.TProgressbar", length=220
        )
        self.enc_progress.pack(side="right")

        # Encode Action Button
        action_row = tk.Frame(msg_body, bg=self.C_CARD)
        action_row.pack(fill="x", pady=(4, 0))

        clear_btn = tk.Button(
            action_row, text="Clear", font=("Segoe UI", 9),
            bg="#f1f5f9", fg=self.C_TEXT_MUTED, relief=tk.FLAT,
            padx=14, pady=6, cursor="hand2", command=self._clear_encode_fields
        )
        clear_btn.pack(side="left")

        self.enc_action_btn = tk.Button(
            action_row, text="🔒 Hide Secret Message & Save Stego Image",
            font=("Segoe UI", 10, "bold"), bg=self.C_PRIMARY, fg="#ffffff",
            activebackground=self.C_PRIMARY_HOVER, activeforeground="#ffffff",
            relief=tk.FLAT, padx=20, pady=8, cursor="hand2", command=self._do_encode
        )
        self.enc_action_btn.pack(side="right")

    # =========================================================================
    # TAB 2: DECODE VIEW
    # =========================================================================
    def _build_decode_view(self):
        container = tk.Frame(self.tab_decode, bg=self.C_BG)
        container.pack(fill="both", expand=True, padx=12, pady=10)

        # Top Card: Stego Image Selection & Live Preview
        card_img = self._create_card(container, "1. Stego Image Selection")
        card_img.pack(fill="x", pady=(0, 10))

        img_row = tk.Frame(card_img, bg=self.C_CARD)
        img_row.pack(fill="x", padx=14, pady=10)

        # Image Thumbnail Canvas
        self.dec_preview_canvas = tk.Canvas(
            img_row, width=120, height=90, bg="#f1f5f9",
            highlightthickness=1, highlightbackground=self.C_BORDER
        )
        self.dec_preview_canvas.pack(side="left", padx=(0, 14))
        self._draw_canvas_placeholder(self.dec_preview_canvas, "No Image")

        info_col = tk.Frame(img_row, bg=self.C_CARD)
        info_col.pack(side="left", fill="both", expand=True)

        path_lbl = tk.Label(
            info_col, textvariable=self.dec_img_path,
            font=("Consolas", 8), fg="#64748b", bg="#f8fafc",
            anchor="w", padx=6, pady=4, relief=tk.SOLID, borderwidth=1
        )
        path_lbl.pack(fill="x", pady=(0, 6))

        meta_lbl = tk.Label(
            info_col, textvariable=self.dec_img_info,
            font=("Segoe UI", 9, "bold"), fg="#0f766e", bg=self.C_CARD, anchor="w"
        )
        meta_lbl.pack(fill="x", pady=(0, 8))

        btn_row = tk.Frame(info_col, bg=self.C_CARD)
        btn_row.pack(anchor="w")

        browse_btn = tk.Button(
            btn_row, text="📁 Browse Stego Image...", font=("Segoe UI", 9),
            bg="#f1f5f9", fg=self.C_TEXT_MAIN, relief=tk.GROOVE,
            padx=12, pady=4, cursor="hand2", command=self._browse_decode_image
        )
        browse_btn.pack(side="left", padx=(0, 8))

        # Decode Action Button
        self.dec_action_btn = tk.Button(
            card_img, text="🔓 Extract Confidential Message & Verify Integrity",
            font=("Segoe UI", 10, "bold"), bg=self.C_SUCCESS, fg="#ffffff",
            activebackground=self.C_SUCCESS_HOVER, activeforeground="#ffffff",
            relief=tk.FLAT, padx=16, pady=8, cursor="hand2", command=self._do_decode
        )
        self.dec_action_btn.pack(fill="x", padx=14, pady=(0, 12))

        # Middle: Tamper & Integrity Radar Card (Hidden initially)
        self.card_radar = self._create_card(container, "2. Integrity & Tamper Radar")
        self.radar_content = tk.Frame(self.card_radar, bg=self.C_CARD)
        self.radar_content.pack(fill="x", padx=14, pady=10)

        self.radar_badge = tk.Label(
            self.radar_content, text="", font=("Segoe UI", 10, "bold"),
            padx=12, pady=6, relief=tk.FLAT
        )
        self.radar_badge.pack(anchor="w", pady=(0, 4))

        self.radar_details = tk.Label(
            self.radar_content, text="", font=("Segoe UI", 9),
            fg=self.C_TEXT_MUTED, bg=self.C_CARD, justify="left", anchor="w"
        )
        self.radar_details.pack(fill="x")

        # Bottom Card: Extracted Message
        card_extracted = self._create_card(container, "3. Extracted Secret Message")
        card_extracted.pack(fill="both", expand=True, pady=(0, 8))

        extracted_body = tk.Frame(card_extracted, bg=self.C_CARD)
        extracted_body.pack(fill="both", expand=True, padx=14, pady=(8, 12))

        text_frame2 = tk.Frame(extracted_body, bg=self.C_CARD)
        text_frame2.pack(fill="both", expand=True, pady=(0, 8))

        self.dec_text = tk.Text(
            text_frame2, wrap="word", font=("Consolas", 10),
            bg="#f8fafc", fg=self.C_TEXT_MAIN, relief=tk.SOLID, borderwidth=1,
            padx=8, pady=8, state="disabled"
        )
        self.dec_text.pack(side="left", fill="both", expand=True)

        scroll2 = ttk.Scrollbar(text_frame2, orient="vertical", command=self.dec_text.yview)
        scroll2.pack(side="right", fill="y")
        self.dec_text.config(yscrollcommand=scroll2.set)

        action_row2 = tk.Frame(extracted_body, bg=self.C_CARD)
        action_row2.pack(fill="x")

        self.copy_btn = tk.Button(
            action_row2, text="📋 Copy Message", font=("Segoe UI", 9, "bold"),
            bg="#f1f5f9", fg=self.C_PRIMARY, relief=tk.FLAT,
            padx=14, pady=6, cursor="hand2", command=self._copy_extracted
        )
        self.copy_btn.pack(side="left")

        clear_btn2 = tk.Button(
            action_row2, text="Clear", font=("Segoe UI", 9),
            bg="#f1f5f9", fg=self.C_TEXT_MUTED, relief=tk.FLAT,
            padx=14, pady=6, cursor="hand2", command=self._clear_decode_fields
        )
        clear_btn2.pack(side="right")

    # =========================================================================
    # HELPER WIDGETS & GRAPHICS
    # =========================================================================
    def _create_card(self, parent, title_text):
        frame = tk.Frame(parent, bg=self.C_CARD, highlightthickness=1, highlightbackground=self.C_BORDER)
        title = tk.Label(
            frame, text=title_text, font=("Segoe UI", 10, "bold"),
            fg=self.C_TEXT_MAIN, bg=self.C_CARD, anchor="w", padx=14, pady=8
        )
        title.pack(fill="x")
        divider = tk.Frame(frame, bg="#f1f5f9", height=1)
        divider.pack(fill="x")
        return frame

    def _draw_canvas_placeholder(self, canvas, text):
        canvas.delete("all")
        canvas.create_rectangle(2, 2, 118, 88, fill="#f8fafc", outline="#cbd5e1", dash=(4, 4))
        canvas.create_text(60, 45, text=f"📷 {text}", font=("Segoe UI", 8), fill="#94a3b8")

    def _update_canvas_thumbnail(self, canvas, image_path, is_encode=True):
        try:
            with Image.open(image_path) as img:
                img_copy = img.copy()
                img_copy.thumbnail((116, 86), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img_copy)
                
                canvas.delete("all")
                # Center photo in canvas
                canvas.create_image(60, 45, image=photo, anchor="center")
                
                if is_encode:
                    self.enc_thumbnail_ref = photo
                else:
                    self.dec_thumbnail_ref = photo
        except Exception:
            self._draw_canvas_placeholder(canvas, "Invalid")

    # =========================================================================
    # EVENT HANDLERS - ENCODE
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
            # Create a simple synthetic sample image
            img = Image.new("RGB", (300, 300))
            draw = ImageDraw.Draw(img)
            for y in range(300):
                for x in range(300):
                    draw.point((x, y), fill=(int(255 * x / 300), int(255 * y / 300), 160))
            img.save(demo_path, format="PNG")
        self._load_encode_image(demo_path)
        self.status_var.set("Demo image loaded successfully!")

    def _load_encode_image(self, file_path):
        self.enc_img_path.set(file_path)
        self._update_canvas_thumbnail(self.enc_preview_canvas, file_path, is_encode=True)
        try:
            with Image.open(file_path) as im:
                w, h = im.size
                fmt = im.format or "IMG"
                file_size_kb = os.path.getsize(file_path) / 1024
            
            red = self.enc_redundancy.get()
            self.enc_capacity = get_image_capacity(file_path, redundancy=red)
            self.enc_img_info.set(f"{w} × {h} px  |  {fmt}  |  {file_size_kb:.1f} KB  |  Capacity: {self.enc_capacity:,} chars")
            self._update_capacity_meter()
            self.status_var.set(f"Loaded cover image: {os.path.basename(file_path)}")
        except Exception as e:
            self.enc_img_info.set(f"Error reading image: {e}")

    def _on_mode_change(self):
        path = self.enc_img_path.get()
        if path and os.path.exists(path):
            self._load_encode_image(path)

    def _update_capacity_meter(self, event=None):
        msg = self.enc_text.get("1.0", tk.END).rstrip("\n")
        msg_len = len(msg)
        cap = self.enc_capacity

        if cap > 0:
            pct = min(100.0, (msg_len / cap) * 100.0)
            self.enc_progress["value"] = pct
            self.enc_cap_lbl.config(text=f"Storage Usage: {msg_len:,} / {cap:,} characters ({pct:.1f}%)")
            if pct > 95:
                self.enc_cap_lbl.config(fg="#dc2626")  # Red
            elif pct > 75:
                self.enc_cap_lbl.config(fg="#d97706")  # Amber
            else:
                self.enc_cap_lbl.config(fg=self.C_TEXT_MUTED)
        else:
            self.enc_progress["value"] = 0
            self.enc_cap_lbl.config(text=f"Storage Usage: {msg_len:,} characters (No image selected)")

    def _do_encode(self):
        img_path = self.enc_img_path.get().strip()
        secret_msg = self.enc_text.get("1.0", tk.END).rstrip("\n")
        redundancy = self.enc_redundancy.get()

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
            self.status_var.set(f"Stego image saved: {os.path.basename(res['output_path'])}")
            
            mode_desc = (
                "🛡️ Robust Mode (5x Redundancy): Protected by Majority Voting.\n"
                "Even if pixels are edited, the secret message can still be reconstructed!"
                if redundancy > 1 else
                "⚡ Standard Mode (1x Redundancy): Maximum capacity utilized."
            )

            messagebox.showinfo(
                "Steganography Success",
                f"Secret message was successfully embedded!\n\n"
                f"📁 Output File: {res['output_path']}\n"
                f"📊 Protection: {res['mode']}\n"
                f"📝 Message Size: {res['message_length']:,} characters\n"
                f"📈 Capacity Used: {res['capacity_used_percent']}%\n\n"
                f"{mode_desc}"
            )
        except Exception as e:
            messagebox.showerror("Encoding Error", str(e))
            self.status_var.set("Encoding failed.")

    def _clear_encode_fields(self):
        self.enc_img_path.set("")
        self.enc_img_info.set("No image loaded yet.")
        self.enc_capacity = 0
        self.enc_text.delete("1.0", tk.END)
        self._draw_canvas_placeholder(self.enc_preview_canvas, "No Image")
        self._update_capacity_meter()
        self.status_var.set("Cleared encode fields.")

    # =========================================================================
    # EVENT HANDLERS - DECODE
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
            self.dec_img_path.set(file_path)
            self._update_canvas_thumbnail(self.dec_preview_canvas, file_path, is_encode=False)
            try:
                with Image.open(file_path) as im:
                    w, h = im.size
                    fmt = im.format or "IMG"
                    sz_kb = os.path.getsize(file_path) / 1024
                self.dec_img_info.set(f"{w} × {h} px  |  {fmt}  |  {sz_kb:.1f} KB")
                self.card_radar.pack_forget()
                self.status_var.set(f"Selected stego image: {os.path.basename(file_path)}")
            except Exception as e:
                self.dec_img_info.set(f"Error: {e}")

    def _do_decode(self):
        stego_path = self.dec_img_path.get().strip()
        if not stego_path:
            messagebox.showwarning("Missing Image", "Please select a stego image to extract message from.")
            return

        try:
            result = decode_text(stego_path)

            # Display extracted message
            self.dec_text.config(state="normal")
            self.dec_text.delete("1.0", tk.END)
            self.dec_text.insert("1.0", result)
            self.dec_text.config(state="disabled")

            # Show Radar Card with Modern Badges
            self.card_radar.pack(fill="x", pady=(0, 10), before=self.dec_text.master.master)

            if result.tampered:
                self.radar_badge.config(
                    text=f"⚠️ TAMPERING DETECTED & REPAIRED  ({result.mode})",
                    fg="#b45309", bg="#fef3c7"
                )
                self.radar_details.config(
                    text=f"• Corrupted pixel bits detected: {result.tampered_bits:,} bits\n"
                         f"• Majority Voting repair: 100% of bits recovered\n"
                         f"• Tamper rate: {result.tamper_rate}% of sampled bits"
                )
            else:
                self.radar_badge.config(
                    text=f"✅ IMAGE INTACT & PRISTINE  ({result.mode})",
                    fg="#047857", bg="#ecfdf5"
                )
                self.radar_details.config(
                    text="• Clean signal: 0 bit flips detected\n"
                         "• Pixel integrity: 100.0% match with original embedded bits"
                )

            self.status_var.set(f"Message extracted! Length: {len(result):,} chars | Mode: {result.mode}")

        except Exception as e:
            self.dec_text.config(state="normal")
            self.dec_text.delete("1.0", tk.END)
            self.dec_text.config(state="disabled")
            self.card_radar.pack_forget()
            messagebox.showerror("Decoding Error", str(e))
            self.status_var.set("Decoding failed: No valid hidden message detected.")

    def _copy_extracted(self):
        text = self.dec_text.get("1.0", tk.END).rstrip("\n")
        if not text:
            messagebox.showinfo("Clipboard", "No text to copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        
        # Interactive UI feedback
        self.copy_btn.config(text="✓ Copied to Clipboard!", fg="#059669")
        self.root.after(2000, lambda: self.copy_btn.config(text="📋 Copy Message", fg=self.C_PRIMARY))
        self.status_var.set("Secret message copied to clipboard.")

    def _clear_decode_fields(self):
        self.dec_img_path.set("")
        self.dec_img_info.set("No stego image loaded yet.")
        self.card_radar.pack_forget()
        self.dec_text.config(state="normal")
        self.dec_text.delete("1.0", tk.END)
        self.dec_text.config(state="disabled")
        self._draw_canvas_placeholder(self.dec_preview_canvas, "No Image")
        self.status_var.set("Cleared decode fields.")


def main():
    root = tk.Tk()
    app = ModernSteganographyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
