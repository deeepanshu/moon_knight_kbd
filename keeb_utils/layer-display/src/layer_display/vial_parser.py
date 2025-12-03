"""Parser for Vial .vil keymap files."""

import json
from typing import Dict, List, Optional


class VialKeymapParser:
    """Parse and format Vial keymap files."""

    # Common keycode to human-readable mappings
    KEYCODE_MAP = {
        # Modifiers
        "KC_LCTL": "Ctrl",
        "KC_LSFT": "Shift",
        "KC_LALT": "Alt",
        "KC_LGUI": "Cmd",
        "KC_RCTL": "RCtrl",
        "KC_RSFT": "RShift",
        "KC_RALT": "RAlt",
        "KC_RGUI": "RCmd",

        # Special keys
        "KC_ESC": "Esc",
        "KC_ESCAPE": "Esc",
        "KC_TAB": "Tab",
        "KC_SPC": "Space",
        "KC_SPACE": "Space",
        "KC_ENT": "Enter",
        "KC_ENTER": "Enter",
        "KC_BSPC": "Bksp",
        "KC_BSPACE": "Bksp",
        "KC_DEL": "Del",
        "KC_DELETE": "Del",

        # Punctuation
        "KC_MINS": "-",
        "KC_EQL": "=",
        "KC_LBRC": "[",
        "KC_LBRACKET": "[",
        "KC_RBRC": "]",
        "KC_RBRACKET": "]",
        "KC_BSLS": "\\",
        "KC_SCLN": ";",
        "KC_SCOLON": ";",
        "KC_QUOT": "'",
        "KC_QUOTE": "'",
        "KC_GRV": "`",
        "KC_COMM": ",",
        "KC_COMMA": ",",
        "KC_DOT": ".",
        "KC_SLSH": "/",
        "KC_SLASH": "/",

        # Shifted symbols
        "KC_EXLM": "!",
        "KC_AT": "@",
        "KC_HASH": "#",
        "KC_DLR": "$",
        "KC_PERC": "%",
        "KC_CIRC": "^",
        "KC_AMPR": "&",
        "KC_ASTR": "*",
        "KC_LPRN": "(",
        "KC_RPRN": ")",
        "KC_UNDS": "_",
        "KC_PLUS": "+",
        "KC_LCBR": "{",
        "KC_RCBR": "}",
        "KC_PIPE": "|",
        "KC_LABK": "<",
        "KC_RABK": ">",
        "KC_TILD": "~",

        # Navigation
        "KC_LEFT": "←",
        "KC_DOWN": "↓",
        "KC_UP": "↑",
        "KC_RGHT": "→",
        "KC_RIGHT": "→",
        "KC_HOME": "Home",
        "KC_END": "End",
        "KC_PGUP": "PgUp",
        "KC_PGDN": "PgDn",
        "KC_PGDOWN": "PgDn",

        # Function keys
        "KC_F1": "F1", "KC_F2": "F2", "KC_F3": "F3", "KC_F4": "F4",
        "KC_F5": "F5", "KC_F6": "F6", "KC_F7": "F7", "KC_F8": "F8",
        "KC_F9": "F9", "KC_F10": "F10", "KC_F11": "F11", "KC_F12": "F12",

        # Media
        "KC_MUTE": "Mute",
        "KC_VOLU": "Vol+",
        "KC_VOLD": "Vol-",
        "KC_MPLY": "Play",
        "KC_MNXT": "Next",
        "KC_MPRV": "Prev",

        # Mouse
        "KC_BTN1": "M1",
        "KC_BTN2": "M2",
        "KC_MS_L": "M←",
        "KC_MS_D": "M↓",
        "KC_MS_U": "M↑",
        "KC_MS_R": "M→",

        # Transparent
        "KC_TRNS": "---",
        "KC_NO": "",
    }

    def __init__(self, vil_file_path: str):
        """Load and parse Vial keymap file."""
        with open(vil_file_path, 'r') as f:
            self.data = json.load(f)

        self.layout = self.data.get("layout", [])
        self.layer_count = len(self.layout)

    def format_keycode(self, keycode: str) -> str:
        """Convert QMK keycode to human-readable format."""
        if keycode == -1 or keycode == "-1":
            return ""

        # Handle mod-tap keys like LSFT_T(KC_F)
        if "_T(" in keycode:
            # Extract mod and key
            parts = keycode.split("_T(")
            mod = parts[0].replace("KC_", "").replace("L", "").replace("R", "")
            key = parts[1].rstrip(")")
            key_label = self.format_keycode(key)
            return f"{key_label}/{mod[:1]}"  # e.g., "F/S" for Shift-tap

        # Handle layer-tap keys like LT2(KC_BSPACE)
        if keycode.startswith("LT") and "(" in keycode:
            layer = keycode[2]
            key = keycode.split("(")[1].rstrip(")")
            key_label = self.format_keycode(key)
            return f"L{layer}/{key_label}"

        # Handle mod combos like SGUI(KC_SPACE)
        if "(" in keycode and not keycode.startswith("KC_"):
            mod_part = keycode.split("(")[0]
            key_part = keycode.split("(")[1].rstrip(")")
            key_label = self.format_keycode(key_part)
            # S=Shift, GUI=Cmd, etc.
            mod_label = mod_part.replace("SGUI", "⇧⌘").replace("RALT", "⌥")
            return f"{mod_label}{key_label}"

        # Handle MO(n) - momentary layer
        if keycode.startswith("MO("):
            layer = keycode[3]
            return f"L{layer}"

        # Numbers and letters
        if keycode.startswith("KC_") and len(keycode) == 4:
            return keycode[3]  # KC_1 → 1, KC_A → A

        # Look up in map
        if keycode in self.KEYCODE_MAP:
            return self.KEYCODE_MAP[keycode]

        # Fallback: strip KC_ prefix
        return keycode.replace("KC_", "")

    def get_layer_keymap(self, layer: int) -> Dict[str, List[List[str]]]:
        """
        Get formatted keymap for a specific layer.

        Returns:
            Dict with 'left' and 'right' keys, each containing 4 rows of key labels
        """
        if layer >= self.layer_count:
            return {"left": [], "right": []}

        layer_data = self.layout[layer]

        # Split layout: first 4 rows are left side, last 4 are right side
        # Structure: [row0_left, row1_left, row2_left, thumb_left, row0_right, row1_right, row2_right, thumb_right]
        left_rows = layer_data[0:4]
        right_rows = layer_data[4:8]

        # Format keycodes
        left_formatted = [[self.format_keycode(k) for k in row] for row in left_rows]
        right_formatted = [[self.format_keycode(k) for k in row] for row in right_rows]

        return {
            "left": left_formatted,
            "right": right_formatted
        }

    def format_layer_ascii(self, layer: int, max_width: int = 50) -> str:
        """
        Format layer as ASCII art for menubar display.

        Args:
            layer: Layer number (0-3)
            max_width: Maximum width in characters

        Returns:
            Formatted ASCII art string
        """
        keymap = self.get_layer_keymap(layer)
        left = keymap["left"]
        right = keymap["right"]

        lines = []

        # Add header to show split
        lines.append("  ╔═══ LEFT ═══╗     ╔═══ RIGHT ═══╗")

        # Format each row (skip thumb cluster for now, too wide)
        for i in range(3):  # Only show main 3 rows
            left_row = left[i]
            right_row = right[i]

            # Filter out empty keys
            left_keys = [k for k in left_row if k]
            right_keys = [k for k in right_row if k]

            # Format with padding
            left_str = " ".join(f"{k:>4}" for k in left_keys)
            right_str = " ".join(f"{k:>4}" for k in right_keys)

            lines.append(f"  {left_str}  │  {right_str}")

        # Add thumb cluster on separate line
        left_thumb = [k for k in left[3] if k]
        right_thumb = [k for k in right[3] if k]

        thumb_left_str = " ".join(f"{k:>4}" for k in left_thumb[-2:])  # Last 2 keys
        thumb_right_str = " ".join(f"{k:>4}" for k in right_thumb[:2])  # First 2 keys

        lines.append(f"         {thumb_left_str}  │  {thumb_right_str}")

        return "\n".join(lines)
