#!/usr/bin/env python3
"""
Test script to verify GUI launches correctly.
"""
import sys

try:
    print("Importing GUI module...")
    from qr_portal.gui import QRPortalGUI
    print("GUI module imported successfully.")
    
    print("Creating GUI window...")
    app = QRPortalGUI()
    print("GUI window created. Starting mainloop...")
    print("Window should be visible now!")
    app.mainloop()
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)

