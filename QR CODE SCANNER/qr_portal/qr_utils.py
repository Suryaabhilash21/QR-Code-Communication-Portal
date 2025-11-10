from __future__ import annotations

import os
from typing import Optional

from PIL import Image
import qrcode
try:
    from pyzbar.pyzbar import decode as zbar_decode  # type: ignore
except Exception:  # pragma: no cover - optional on Windows
    zbar_decode = None  # type: ignore
try:
    import cv2  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    cv2 = None  # type: ignore


DEFAULT_QR_FILENAME = "message_qr.png"


def generate_qr(message: str, output_path: str = DEFAULT_QR_FILENAME, show: bool = True) -> str:
    """
    Generate a QR code image from the provided message.

    Args:
        message: Text content to encode into the QR code.
        output_path: File path to save the generated QR image.
        show: If True, attempt to open the image with the default viewer.

    Returns:
        The path where the QR image is saved.
    """
    if not isinstance(message, str) or len(message.strip()) == 0:
        raise ValueError("Message must be a non-empty string.")

    # Create a QR code with reasonable defaults
    qr = qrcode.QRCode(
        version=None,  # automatic
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # medium EC
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img.save(output_path)

    if show:
        # Best-effort show; may be a no-op in some environments
        try:
            img.show(title="Generated QR")
        except Exception:
            pass

    return output_path


def decode_qr(image_path: str = DEFAULT_QR_FILENAME) -> Optional[str]:
    """
    Decode the first QR code found in the given image file.

    Args:
        image_path: Path to the QR image file to decode.

    Returns:
        Decoded text if any QR code is found, otherwise None.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"QR image not found at '{image_path}'. Generate one first.")

    # Try pyzbar first if available
    if zbar_decode is not None:
        try:
            image = Image.open(image_path)
            results = zbar_decode(image)  # may raise if ZBar DLL not found
            if results:
                data_bytes = results[0].data
                try:
                    return data_bytes.decode("utf-8")
                except Exception:
                    return data_bytes.decode(errors="replace")
        except Exception:
            # If pyzbar is installed but ZBar backend missing, fall through to OpenCV
            pass

    # Fallback: OpenCV QRCodeDetector (no external ZBar dependency)
    if cv2 is not None:
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            return None
        detector = cv2.QRCodeDetector()
        data, points, _ = detector.detectAndDecode(img_bgr)
        if points is not None and data:
            return data

    # If we reach here, no backend succeeded
    return None


