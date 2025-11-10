# QR Code Communication Portal

A Python-based portal to generate and decode QR codes for sending and receiving messages. Includes a console (text UI) app and an optional Tkinter GUI.

## Features
- Generate a QR code from text (`message_qr.png`)
- Decode the saved QR image back to text
- Console menu and optional GUI with preview

## Requirements
- Python 3.8+
- Libraries:
  - `qrcode`
  - `Pillow`
  - `pyzbar`
  - `tkinter` (bundled with most Python distributions on Windows)

Install dependencies:

```bash
pip install -r requirements.txt
```

On Windows, if `pyzbar` needs ZBar, install from pip first (it bundles binaries for Windows). If you face issues, see: `https://pypi.org/project/pyzbar/`.

## Project Structure
```
qr_portal/
  cli.py          # Console app
  gui.py          # Tkinter GUI (optional)
  qr_utils.py     # Reusable QR helpers (generate/decode)
requirements.txt
README.md
```

## Run - Console
```bash
python -m qr_portal.cli
```

You will see:
```
==============================
    QR CODE COMMUNICATION PORTAL
==============================
1)  Generate QR Code
2)  Decode QR Code
3)  Exit
```

Example:
```
Enter your choice: 1
Enter the message to encode: Hello Surya!
✅ QR Code successfully generated and saved as 'message_qr.png'

Enter your choice: 2
📩 Decoded Message: Hello Surya!
```

## Run - GUI (Optional)
```bash
python -m qr_portal.gui
```
GUI window:
- Enter message
- Click "Generate QR" to save and preview
- Click "Decode QR" to read `message_qr.png` and show the message

## Implementation Notes
- `generate_qr()` uses `qrcode.QRCode` with medium error correction.
- `decode_qr()` uses `pyzbar.decode()` to extract QR content from the saved image.
- Graceful error handling for missing files and invalid inputs.

## Project Report
**Title:** QR Code Communication Portal  
**Abstract:** The QR Code Communication Portal enables users to send and receive messages through QR codes. The project demonstrates QR code generation and decoding using Python libraries.  
**Methodology:**
1. User inputs data.
2. The system encodes data into a QR image.
3. The QR image can be decoded to retrieve the original message.
**Expected Output:** A working portal that encodes and decodes messages via QR.  
**Conclusion:** This project showcases the use of QR codes for secure and offline message sharing using Python.

## Developer
Project by: Surya Abhilash  
Language: Python  
Type: College Mini Project  
Topic: Data Communication and Security using QR


