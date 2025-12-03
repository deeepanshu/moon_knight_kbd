# Adding Raw HID Layer Reporting to QMK Firmware

## Overview

This guide shows how to make your keyboard send layer change notifications to the macOS menubar app via Raw HID.

## Changes Needed

### 1. Enable Raw HID in `rules.mk`

Add this line to `/firmwares/dj/moon_knight/keymaps/vial/rules.mk`:

```make
RAW_ENABLE = yes
```

### 2. Add Layer Reporting Code to `keymap.c`

Add this code to `/firmwares/dj/moon_knight/keymaps/vial/keymap.c`:

```c
#ifdef RAW_ENABLE
#include "raw_hid.h"

// Message IDs for HID communication
#define MSG_LAYER_UPDATE 0x01

// Track current layer to only send updates on changes
static uint8_t current_layer = 0;

// Called by QMK whenever the layer changes
layer_state_t layer_state_set_user(layer_state_t state) {
    uint8_t new_layer = get_highest_layer(state);

    // Only send if layer actually changed
    if (new_layer != current_layer) {
        current_layer = new_layer;

        // Send HID message: [MSG_ID, LAYER, 0, 0, ..., 0] (32 bytes total)
        uint8_t data[32] = {0};
        data[0] = MSG_LAYER_UPDATE;
        data[1] = current_layer;

        raw_hid_send(data, sizeof(data));
    }

    return state;
}
#endif
```

### 3. Where to Add the Code

Insert the Raw HID code **after line 88** (after the keymaps definition, before or after `keyboard_post_init_user()`).

Your `keymap.c` structure will be:
```
Line 1-88:   Existing keymaps
Line 89+:    Raw HID code (new)
Line 90+:    keyboard_post_init_user() (existing)
```

## Complete Example

Here's what the end of your `keymap.c` should look like:

```c
    [3] = LAYOUT_split_3x6_4(
        KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,   KC_F6,                              KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_F11,  KC_F12,
        _______, _______, _______, _______, _______, _______,                            KC_MPRV, KC_VOLD, KC_VOLU, KC_MNXT, KC_MUTE, KC_MPLY,
        _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
                                            _______, _______, _______, _______,          _______, _______, _______, _______
    )
};

#ifdef RAW_ENABLE
#include "raw_hid.h"

#define MSG_LAYER_UPDATE 0x01

static uint8_t current_layer = 0;

layer_state_t layer_state_set_user(layer_state_t state) {
    uint8_t new_layer = get_highest_layer(state);

    if (new_layer != current_layer) {
        current_layer = new_layer;

        uint8_t data[32] = {0};
        data[0] = MSG_LAYER_UPDATE;
        data[1] = current_layer;

        raw_hid_send(data, sizeof(data));
    }

    return state;
}
#endif

void keyboard_post_init_kb(void) {
    keyboard_post_init_user();
}

void keyboard_post_init_user(void) {
    // debug_enable=true;
    // debug_matrix=true;
    // debug_keyboard=true;

    rgblight_enable_noeeprom();
    rgblight_mode_noeeprom(RGBLIGHT_MODE_RAINBOW_MOOD + 1);
}
```

## Building and Flashing

After making these changes:

```bash
# Navigate to your QMK firmware directory (where the symlink points)
cd ~/qmk_firmware

# Build the firmware
qmk compile -kb dj/moon_knight -km vial

# Flash to keyboard (hold bootmagic keys and plug in)
qmk flash -kb dj/moon_knight -km vial
```

## Testing

1. Flash the updated firmware
2. Run the menubar app: `./launch-layer-display.sh`
3. Press your layer keys (MO(1), MO(2), MO(3))
4. Watch the menubar text change in real-time!

## How It Works

- **QMK Side:** `layer_state_set_user()` is called whenever layers change
- **Sends:** 32-byte HID packet with [MSG_ID, LAYER_NUMBER, ...]
- **Python Side:** HID listener receives packet and updates menubar text
- **Protocol:** Raw HID (no drivers needed, works out of the box on macOS)
