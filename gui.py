"""
Desktop Graphical User Interface (GUI) for Text Steganography
-------------------------------------------------------------
Built with Python's standard Tkinter & ttk libraries.
Provides two easy-to-use tabs:
1. Hide Message (Encode) with Robust Tamper-Resistant toggle
2. Extract Message (Decode) with Tamper Detection & Error Correction Badge
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image
from stego_core import encode_text, decode_text, get_image_capacity


class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Steganography - Robust LSB Data Hiding")
        self.root.geometry("740x660")
        self.root.minsize(680, 580)

        # Style configuration
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass

        # Variables for Encode Tab
        self.encode_img_path = tk.StringVar()
        self.encode_img_info = tk.StringVar(value="No image selected.")
        self.redundancy_var = tk.IntVar(value=5)  # Default to Robust 5x
        
        # Variables for Decode Tab
        self.decode_img_path = tk.StringVar()
        self.decode_img_info = tk.StringVar(value="No stego image selected.")
        self.integrity_status = tk.StringVar(value="")

        self._build_ui()

    def _build_ui(self):
        # Header banner
        header_frame = tk.Frame(self.root, bg="#1e293b", height=75)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        title_lbl = tk.Label(
            header_frame,
            text="TEXT STEGANOGRAPHY",
            font=("Segoe UI", 16, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        )
        title_lbl.pack(pady=(8, 2))

        subtitle_lbl = tk.Label(
            header_frame,
            text="LSB Image Data Hiding with Majority-Voting Error Correction & Tamper Detection",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#1e293b"
        )
        subtitle_lbl.pack()

        # Notebook for Tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=12, pady=10)

        # Tab 1: Encode
        encode_tab = ttk.Frame(notebook)
        notebook.add(encode_tab, text="  Hide Message (Encode)  ")
        self._build_encode_tab(encode_tab)

        # Tab 2: Decode
        decode_tab = ttk.Frame(notebook)
        notebook.add(decode_tab, text="  Extract Message (Decode)  ")
        self._build_decode_tab(decode_tab)

        # Status bar
        self.status_var = tk.StringVar(value="Ready.")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor="w",
            font=("Segoe UI", 8),
            fg="#475569",
            bg="#f1f5f9"
        )
        status_bar.pack(side="bottom", fill="x")

    def _build_encode_tab(self, parent):
        frame = ttk.Frame(parent, padding=12)
        frame.pack(fill="both", expand=True)

        # 1. Carrier Image Selection
        img_select_box = ttk.LabelFrame(frame, text="1. Select Carrier (Cover) Image", padding=10)
        img_select_box.pack(fill="x", pady=(0, 8))

        top_row = ttk.Frame(img_select_box)
        top_row.pack(fill="x")

        path_entry = ttk.Entry(top_row, textvariable=self.encode_img_path, state="readonly")
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        browse_btn = ttk.Button(top_row, text="Browse Image...", command=self._browse_encode_image)
        browse_btn.pack(side="right")

        info_lbl = tk.Label(img_select_box, textvariable=self.encode_img_info, fg="#0f766e", font=("Segoe UI", 9, "italic"))
        info_lbl.pack(anchor="w", pady=(6, 0))

        # 2. Protection Mode Selection
        mode_box = ttk.LabelFrame(frame, text="2. Protection & Integrity Mode", padding=10)
        mode_box.pack(fill="x", pady=(0, 8))

        r_robust = ttk.Radiobutton(
            mode_box,
            text="🛡️ Robust Mode (5x Redundancy) — Survived pixel edits, drawing, and tampering via Majority Voting [Recommended]",
            variable=self.redundancy_var,
            value=5,
            command=self._refresh_capacity_label
        )
        r_robust.pack(anchor="w", pady=2)

        r_standard = ttk.Radiobutton(
            mode_box,
            text="⚡ Standard Mode (1x Redundancy) — Maximum capacity, but fragile to pixel alterations",
            variable=self.redundancy_var,
            value=1,
            command=self._refresh_capacity_label
        )
        r_standard.pack(anchor="w", pady=2)

        # 3. Secret Message Input
        msg_box = ttk.LabelFrame(frame, text="3. Enter Secret Message", padding=10)
        msg_box.pack(fill="both", expand=True, pady=(0, 8))

        self.msg_text = tk.Text(msg_box, height=7, wrap="word", font=("Consolas", 10))
        self.msg_text.pack(fill="both", expand=True, side="left")
        self.msg_text.bind("<KeyRelease>", self._update_encode_char_count)

        scrollbar = ttk.Scrollbar(msg_box, orient="vertical", command=self.msg_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.msg_text.config(yscrollcommand=scrollbar.set)

        self.char_count_var = tk.StringVar(value="0 characters")
        count_lbl = tk.Label(frame, textvariable=self.char_count_var, anchor="e", font=("Segoe UI", 8), fg="#64748b")
        count_lbl.pack(fill="x", pady=(0, 4))

        # Action Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=4)

        encode_btn = tk.Button(
            btn_frame,
            text="🔒 Hide Secret Message & Save Stego Image",
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=16,
            pady=8,
            command=self._do_encode
        )
        encode_btn.pack(side="right")

        clear_btn = ttk.Button(btn_frame, text="Clear", command=self._clear_encode)
        clear_btn.pack(side="left")

    def _build_decode_tab(self, parent):
        frame = ttk.Frame(parent, padding=12)
        frame.pack(fill="both", expand=True)

        # 1. Stego Image Selection
        img_select_box = ttk.LabelFrame(frame, text="1. Select Stego Image (containing hidden text)", padding=10)
        img_select_box.pack(fill="x", pady=(0, 10))

        top_row = ttk.Frame(img_select_box)
        top_row.pack(fill="x")

        path_entry = ttk.Entry(top_row, textvariable=self.decode_img_path, state="readonly")
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        browse_btn = ttk.Button(top_row, text="Browse Stego Image...", command=self._browse_decode_image)
        browse_btn.pack(side="right")

        info_lbl = tk.Label(img_select_box, textvariable=self.decode_img_info, fg="#0f766e", font=("Segoe UI", 9, "italic"))
        info_lbl.pack(anchor="w", pady=(6, 0))

        # Decode Action Button
        decode_action_btn = tk.Button(
            frame,
            text="🔓 Extract Hidden Secret Message & Check Integrity",
            bg="#059669",
            fg="white",
            activebackground="#047857",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=16,
            pady=8,
            command=self._do_decode
        )
        decode_action_btn.pack(fill="x", pady=(0, 8))

        # Integrity Badge Label
        self.integrity_lbl = tk.Label(
            frame,
            textvariable=self.integrity_status,
            font=("Segoe UI", 9, "bold"),
            fg="#047857",
            bg="#ecfdf5",
            padx=10,
            pady=6,
            relief=tk.GROOVE
        )
        # Initially not packed until extraction

        # Extracted Message Output Box
        output_box = ttk.LabelFrame(frame, text="2. Extracted Confidential Message", padding=10)
        output_box.pack(fill="both", expand=True, pady=(0, 10))

        self.extracted_text = tk.Text(output_box, height=8, wrap="word", font=("Consolas", 10), state="disabled", bg="#f8fafc")
        self.extracted_text.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(output_box, orient="vertical", command=self.extracted_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.extracted_text.config(yscrollcommand=scrollbar.set)

        # Bottom Buttons
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill="x")

        copy_btn = ttk.Button(bottom_frame, text="📋 Copy Message to Clipboard", command=self._copy_extracted)
        copy_btn.pack(side="left")

        clear_btn = ttk.Button(bottom_frame, text="Clear", command=self._clear_decode)
        clear_btn.pack(side="right")

    # --- Event Handlers for Encode ---
    def _browse_encode_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[
                ("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp"),
                ("PNG Files (*.png)", "*.png"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.encode_img_path.set(file_path)
            self._refresh_capacity_label()
            self.status_var.set(f"Loaded cover image: {os.path.basename(file_path)}")

    def _refresh_capacity_label(self):
        img_path = self.encode_img_path.get().strip()
        if not img_path or not os.path.exists(img_path):
            return
        try:
            red = self.redundancy_var.get()
            cap = get_image_capacity(img_path, redundancy=red)
            with Image.open(img_path) as im:
                w, h = im.size
            mode_desc = f"Robust ({red}x)" if red > 1 else "Standard (1x)"
            self.encode_img_info.set(
                f"Dimensions: {w} × {h} px | Mode: {mode_desc} | Max Capacity: {cap:,} characters"
            )
        except Exception as e:
            self.encode_img_info.set(f"Error reading image: {e}")

    def _update_encode_char_count(self, event=None):
        msg = self.msg_text.get("1.0", tk.END).rstrip("\n")
        self.char_count_var.set(f"{len(msg):,} characters")

    def _do_encode(self):
        img_path = self.encode_img_path.get().strip()
        secret_msg = self.msg_text.get("1.0", tk.END).rstrip("\n")
        redundancy = self.redundancy_var.get()

        if not img_path:
            messagebox.showwarning("Missing Image", "Please select a cover image first.")
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
            self.status_var.set(f"Saved stego image to: {res['output_path']}")
            
            mode_note = (
                "🛡️ Robust Mode: Protected with Majority Voting. Even if pixels are edited, "
                "the secret message can still be reconstructed!"
                if redundancy > 1 else
                "⚡ Standard Mode: Maximum storage capacity used."
            )
            
            messagebox.showinfo(
                "Steganography Success",
                f"Secret message successfully embedded!\n\n"
                f"File Saved: {res['output_path']}\n"
                f"Mode: {res['mode']}\n"
                f"Message Length: {res['message_length']:,} characters\n"
                f"Capacity Used: {res['capacity_used_percent']}%\n\n"
                f"{mode_note}"
            )
        except Exception as e:
            messagebox.showerror("Encoding Error", str(e))
            self.status_var.set("Encoding failed.")

    def _clear_encode(self):
        self.encode_img_path.set("")
        self.encode_img_info.set("No image selected.")
        self.msg_text.delete("1.0", tk.END)
        self.char_count_var.set("0 characters")
        self.status_var.set("Cleared encode fields.")

    # --- Event Handlers for Decode ---
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
            self.decode_img_path.set(file_path)
            try:
                with Image.open(file_path) as im:
                    w, h = im.size
                self.decode_img_info.set(f"Loaded: {os.path.basename(file_path)} ({w} × {h} px)")
                self.status_var.set(f"Selected stego image: {os.path.basename(file_path)}")
                self.integrity_lbl.pack_forget()
            except Exception as e:
                self.decode_img_info.set(f"Error: {e}")

    def _do_decode(self):
        stego_path = self.decode_img_path.get().strip()
        if not stego_path:
            messagebox.showwarning("Missing Image", "Please select a stego image to extract message from.")
            return

        try:
            result = decode_text(stego_path)
            
            self.extracted_text.config(state="normal")
            self.extracted_text.delete("1.0", tk.END)
            self.extracted_text.insert("1.0", result)
            self.extracted_text.config(state="disabled")

            # Update Integrity Badge
            self.integrity_lbl.pack(fill="x", pady=(0, 8), before=self.extracted_text.master)
            if result.tampered:
                self.integrity_status.set(
                    f"⚠️ TAMPERING DETECTED & REPAIRED: {result.tampered_bits:,} corrupted pixel bits "
                    f"were corrected via Majority Voting! (Tamper rate: {result.tamper_rate}%)"
                )
                self.integrity_lbl.config(fg="#b45309", bg="#fef3c7")  # Amber badge
            else:
                self.integrity_status.set(
                    f"✅ IMAGE INTACT: Clean signal detected ({result.mode}). 0 pixel bit flips detected."
                )
                self.integrity_lbl.config(fg="#047857", bg="#ecfdf5")  # Green badge

            self.status_var.set(f"Message extracted! Length: {len(result):,} chars | Mode: {result.mode}")
            
            detail = (
                f"Secret message retrieved successfully!\n\n"
                f"Mode: {result.mode}\n"
                f"Length: {len(result):,} characters\n"
            )
            if result.tampered:
                detail += f"\nNotice: The image was modified, but {result.tampered_bits} corrupted bits were repaired by Majority Voting."
            messagebox.showinfo("Extraction Success", detail)

        except Exception as e:
            self.extracted_text.config(state="normal")
            self.extracted_text.delete("1.0", tk.END)
            self.extracted_text.config(state="disabled")
            self.integrity_lbl.pack_forget()
            messagebox.showerror("Decoding Error", str(e))
            self.status_var.set("Decoding failed.")

    def _copy_extracted(self):
        text = self.extracted_text.get("1.0", tk.END).rstrip("\n")
        if not text:
            messagebox.showinfo("Clipboard", "No text to copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Secret message copied to clipboard.")
        messagebox.showinfo("Copied", "Secret message copied to clipboard!")

    def _clear_decode(self):
        self.decode_img_path.set("")
        self.decode_img_info.set("No stego image selected.")
        self.integrity_lbl.pack_forget()
        self.extracted_text.config(state="normal")
        self.extracted_text.delete("1.0", tk.END)
        self.extracted_text.config(state="disabled")
        self.status_var.set("Cleared decode fields.")


def main():
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
