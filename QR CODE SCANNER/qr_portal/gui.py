from __future__ import annotations

import os
import tkinter as tk
from tkinter import messagebox
from typing import Optional

from PIL import Image, ImageTk

from .qr_utils import generate_qr, decode_qr, DEFAULT_QR_FILENAME


class QRPortalGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("QR Code Communication Portal")
        self.geometry("560x520")
        self.resizable(False, False)
        
        # Center the window on screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Widgets
        self._build_widgets()

        # Hold reference to PhotoImage to prevent garbage collection
        self._qr_photo: Optional[ImageTk.PhotoImage] = None
        
        # Bring window to front
        self.lift()
        self.attributes("-topmost", True)
        self.after_idle(lambda: self.attributes("-topmost", False))

    def _build_widgets(self) -> None:
        title = tk.Label(self, text="QR Code Communication Portal", font=("Segoe UI", 16, "bold"))
        title.pack(pady=12)

        frame_input = tk.Frame(self)
        frame_input.pack(pady=8, fill="x", padx=16)

        lbl = tk.Label(frame_input, text="Enter message:")
        lbl.pack(anchor="w")

        self.txt_message = tk.Text(frame_input, height=4, wrap="word")
        self.txt_message.pack(fill="x")

        frame_buttons = tk.Frame(self)
        frame_buttons.pack(pady=10)

        btn_generate = tk.Button(frame_buttons, text="Generate QR", width=16, command=self.on_generate)
        btn_generate.grid(row=0, column=0, padx=8)

        btn_decode = tk.Button(frame_buttons, text="Decode QR", width=16, command=self.on_decode)
        btn_decode.grid(row=0, column=1, padx=8)

        frame_preview = tk.LabelFrame(self, text="QR Preview")
        frame_preview.pack(padx=16, pady=10, fill="both", expand=True)

        self.lbl_image = tk.Label(frame_preview, anchor="center")
        self.lbl_image.pack(padx=8, pady=8, fill="both", expand=True)

        self.lbl_status = tk.Label(self, text="", anchor="w", fg="#0a7")
        self.lbl_status.pack(padx=16, pady=6, fill="x")

    def on_generate(self) -> None:
        message = self.txt_message.get("1.0", "end").strip()
        if not message:
            messagebox.showwarning("Input Required", "Please enter a message to encode.")
            return
        try:
            path = generate_qr(message, DEFAULT_QR_FILENAME, show=False)
            self.lbl_status.config(text=f"✅ QR Code saved as '{path}'")
            self._load_preview(path)
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to generate QR: {exc}")

    def on_decode(self) -> None:
        try:
            text = decode_qr(DEFAULT_QR_FILENAME)
            if not os.path.exists(DEFAULT_QR_FILENAME):
                messagebox.showwarning("Not Found", f"QR image not found at '{DEFAULT_QR_FILENAME}'.")
                return
            if text is None:
                messagebox.showinfo("No QR Detected", "No QR code detected in the image.")
            else:
                messagebox.showinfo("Decoded Message", text)
                self.lbl_status.config(text=f"📩 Decoded: {text}")
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to decode QR: {exc}")

    def _load_preview(self, path: str) -> None:
        try:
            img = Image.open(path)
            # Create a thumbnail for display
            img.thumbnail((420, 420))
            self._qr_photo = ImageTk.PhotoImage(img)
            self.lbl_image.config(image=self._qr_photo)
        except Exception:
            # Ignore preview errors; file still saved
            self.lbl_image.config(image="", text="(Preview unavailable)")


def main() -> None:
    app = QRPortalGUI()
    app.mainloop()


if __name__ == "__main__":
    main()


