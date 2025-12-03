"""HID communication with QMK keyboard for layer state."""

import hid
import threading
import time
from typing import Callable, Optional


class KeyboardHIDListener:
    """Listen for layer updates from QMK keyboard via Raw HID."""

    # QMK Raw HID usage page and ID
    RAW_HID_USAGE_PAGE = 0xFF60
    RAW_HID_USAGE = 0x61

    # Layer update message ID (you'll define this in firmware)
    MSG_LAYER_UPDATE = 0x01

    def __init__(
        self,
        vendor_id: int,
        product_id: int,
        on_layer_change: Callable[[int], None]
    ):
        """
        Initialize HID listener.

        Args:
            vendor_id: USB vendor ID of your keyboard
            product_id: USB product ID of your keyboard
            on_layer_change: Callback function called with layer number when layer changes
        """
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.on_layer_change = on_layer_change
        self.device: Optional[hid.device] = None
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def connect(self) -> bool:
        """
        Connect to the keyboard.

        Returns:
            True if connected successfully, False otherwise
        """
        try:
            # Find the Raw HID interface
            self.device = hid.device()

            # Try to open by VID/PID and usage page
            # Some keyboards have multiple HID interfaces, we want the Raw HID one
            devices = hid.enumerate(self.vendor_id, self.product_id)

            for dev_info in devices:
                if dev_info['usage_page'] == self.RAW_HID_USAGE_PAGE:
                    self.device.open_path(dev_info['path'])
                    self.device.set_nonblocking(1)
                    print(f"Connected to keyboard: {dev_info['product_string']}")
                    return True

            # Fallback: try to open without usage page filter
            self.device.open(self.vendor_id, self.product_id)
            self.device.set_nonblocking(1)
            print(f"Connected to keyboard (VID: 0x{self.vendor_id:04X}, PID: 0x{self.product_id:04X})")
            return True

        except Exception as e:
            print(f"Failed to connect to keyboard: {e}")
            self.device = None
            return False

    def disconnect(self):
        """Disconnect from the keyboard."""
        self.stop()
        if self.device:
            try:
                self.device.close()
            except:
                pass
            self.device = None

    def start(self):
        """Start listening for layer updates in background thread."""
        if self.running:
            return

        if not self.device and not self.connect():
            raise RuntimeError("Cannot start: keyboard not connected")

        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop listening for layer updates."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
            self.thread = None

    def _listen_loop(self):
        """Background thread that listens for HID messages."""
        while self.running:
            try:
                # Read with timeout (100ms)
                data = self.device.read(32, timeout_ms=100)

                if data and len(data) > 0:
                    self._process_message(data)

            except Exception as e:
                print(f"Error reading from keyboard: {e}")
                time.sleep(0.5)

    def _process_message(self, data: list):
        """
        Process incoming HID message from keyboard.

        Expected message format (you'll implement this in firmware):
        Byte 0: Message ID (MSG_LAYER_UPDATE)
        Byte 1: Current layer number (0-255)
        Bytes 2-31: Reserved
        """
        if len(data) < 2:
            return

        msg_id = data[0]

        if msg_id == self.MSG_LAYER_UPDATE:
            layer = data[1]
            self.on_layer_change(layer)


# Keyboard identification
# From moon_knight/keyboard.json
MOON_KNIGHT_VID = 0x1209  # pid.codes - open source hardware
MOON_KNIGHT_PID = 0x4D4B  # "MK" in hex
