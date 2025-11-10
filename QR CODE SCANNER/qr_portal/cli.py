from __future__ import annotations

import sys
import io
from typing import NoReturn

from .qr_utils import generate_qr, decode_qr, DEFAULT_QR_FILENAME

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


BANNER = """
==============================
    QR CODE COMMUNICATION PORTAL
==============================
1)  Generate QR Code
2)  Decode QR Code
3)  Exit
"""


def prompt_choice() -> str:
    try:
        return input("Enter your choice: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()  # newline for clean exit
        return "3"


def handle_generate() -> None:
    try:
        message = input("Enter the message to encode: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")
        return

    if not message:
        print("Message cannot be empty.")
        return

    try:
        path = generate_qr(message, DEFAULT_QR_FILENAME, show=True)
        print(f"✅ QR Code successfully generated and saved as '{path}'")
    except Exception as exc:
        print(f"❌ Failed to generate QR Code: {exc}")


def handle_decode() -> None:
    try:
        decoded = decode_qr(DEFAULT_QR_FILENAME)
        if decoded is None:
            print("⚠️  No QR code detected in the image.")
        else:
            print(f"📩 Decoded Message: {decoded}")
    except FileNotFoundError as exc:
        print(f"❌ {exc}")
    except Exception as exc:
        print(f"❌ Failed to decode QR Code: {exc}")


def main() -> NoReturn:
    while True:
        print(BANNER)
        choice = prompt_choice()
        if choice == "1":
            handle_generate()
        elif choice == "2":
            handle_decode()
        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()


