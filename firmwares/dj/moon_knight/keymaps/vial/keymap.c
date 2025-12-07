// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
     /*
      * LAYER 0 - BASE (Default typing layer)
      * Home Row Mods: F and J act as Shift when held
      * ┌───┬───┬───┬───┬───┬───┐       ┌───┬───┬───┬───┬───┬───┐
      * │Esc│ Q │ W │ E │ R │ T │       │ Y │ U │ I │ O │ P │Bsp│
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │Ctl│ A │ S │ D │F/Sft│ G │     │ H │J/Sft│ K │ L │ ; │ ' │
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │Sft│ Z │ X │ C │ V │ B │       │ N │ M │ , │ . │ / │Sft│
      * └───┴───┴───┴───┴───┴───┘       └───┴───┴───┴───┴───┴───┘
      *           ┌───┬───┬───┬───┐   ┌───┬───┬───┬───┐
      *           │Tab│GUI│Spc│L1 │   │L2 │Spc│Ent│Alt│
      *           └───┴───┴───┴───┘   └───┴───┴───┴───┘
      */
    [0] = LAYOUT_split_3x6_4(
        KC_ESC,  KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,                               KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    KC_BSPC,
        KC_LCTL, KC_A,    KC_S,    KC_D,    LSFT_T(KC_F), KC_G,                          KC_H,    RSFT_T(KC_J), KC_K, KC_L,   KC_SCLN, KC_QUOT,
        KC_LSFT, KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,                               KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH, KC_RSFT,
                                            KC_TAB,  KC_LGUI, KC_SPC,  MO(1),            MO(2),   KC_SPC,  KC_ENT,  KC_RALT
    ),

     /*
      * LAYER 1 - NUMBERS & NAVIGATION (Hold left MO(1))
      * ┌───┬───┬───┬───┬───┬───┐       ┌───┬───┬───┬───┬───┬───┐
      * │   │ 1 │ 2 │ 3 │ 4 │ 5 │       │ 6 │ 7 │ 8 │ 9 │ 0 │Del│
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │   │   │   │   │   │       │ ← │ ↓ │ ↑ │ → │   │   │
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │   │   │   │   │   │       │Hom│PgD│PgU│End│   │   │
      * └───┴───┴───┴───┴───┴───┘       └───┴───┴───┴───┴───┴───┘
      *           ┌───┬───┬───┬───┐   ┌───┬───┬───┬───┐
      *           │   │   │   │   │   │   │   │   │   │
      *           └───┴───┴───┴───┘   └───┴───┴───┴───┘
      */
    [1] = LAYOUT_split_3x6_4(
        _______, KC_1,    KC_2,    KC_3,    KC_4,    KC_5,                               KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    KC_DEL,
        _______, _______, _______, _______, _______, _______,                            KC_LEFT, KC_DOWN, KC_UP,   KC_RGHT, _______, _______,
        _______, _______, _______, _______, _______, _______,                            KC_HOME, KC_PGDN, KC_PGUP, KC_END,  _______, _______,
                                            _______, _______, _______, _______,          _______, _______, _______, _______
    ),

     /*
      * LAYER 2 - SYMBOLS & BRACKETS (Hold right MO(2))
      * Mirrored brackets: Left hand opens, right hand closes
      * ┌───┬───┬───┬───┬───┬───┐       ┌───┬───┬───┬───┬───┬───┐
      * │   │ ! │ @ │ # │ $ │ % │       │ ~ │ ^ │ & │ * │ + │   │
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │ ( │ [ │ { │ < │ _ │       │ - │ > │ } │ ] │ ) │   │
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │   │   │   │ | │ = │       │ \ │   │   │   │   │   │
      * └───┴───┴───┴───┴───┴───┘       └───┴───┴───┴───┴───┴───┘
      *           ┌───┬───┬───┬───┐   ┌───┬───┬───┬───┐
      *           │   │   │L3 │   │   │   │   │   │   │
      *           └───┴───┴───┴───┘   └───┴───┴───┴───┘
      */
    [2] = LAYOUT_split_3x6_4(
        _______, KC_EXLM, KC_AT,   KC_HASH, KC_DLR,  KC_PERC,                            KC_TILD, KC_CIRC, KC_AMPR, KC_ASTR, KC_PLUS, _______,
        _______, KC_LPRN, KC_LBRC, KC_LCBR, KC_LABK, KC_UNDS,                            KC_MINS, KC_RABK, KC_RCBR, KC_RBRC, KC_RPRN, _______,
        _______, _______, _______, _______, KC_PIPE, KC_EQL,                             KC_BSLS, _______, _______, _______, _______, _______,
                                            _______, _______, MO(3),   _______,          _______, _______, _______, _______
    ),

     /*
      * LAYER 3 - FUNCTION KEYS & MEDIA (Hold MO(2) then press MO(3))
      * ┌───┬───┬───┬───┬───┬───┐       ┌───┬───┬───┬───┬───┬───┐
      * │F1 │F2 │F3 │F4 │F5 │F6 │       │F7 │F8 │F9 │F10│F11│F12│
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │   │   │   │   │   │       │Prv│Vl-│Vl+│Nxt│Mut│Ply│
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │   │   │   │   │   │       │   │   │   │   │   │   │
      * └───┴───┴───┴───┴───┴───┘       └───┴───┴───┴───┴───┴───┘
      *           ┌───┬───┬───┬───┐   ┌───┬───┬───┬───┐
      *           │   │   │   │   │   │   │   │   │   │
      *           └───┴───┴───┴───┘   └───┴───┴───┴───┴───┘
      */
    [3] = LAYOUT_split_3x6_4(
        KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,   KC_F6,                              KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_F11,  KC_F12,
        _______, _______, _______, _______, _______, _______,                            KC_MPRV, KC_VOLD, KC_VOLU, KC_MNXT, KC_MUTE, KC_MPLY,
        _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
                                            _______, _______, _______, _______,          _______, _______, _______, _______
    ),

     /*
      * LAYER 4 - RESERVED (No-op for now)
      * ┌───┬───┬───┬───┬───┬───┐       ┌───┬───┬───┬───┬───┬───┐
      * │   │   │   │   │   │   │       │   │   │   │   │   │   │
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │   │   │   │   │   │       │   │   │   │   │   │   │
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │   │   │   │   │   │       │   │   │   │   │   │   │
      * └───┴───┴───┴───┴───┴───┘       └───┴───┴───┴───┴───┴───┘
      *           ┌───┬───┬───┬───┐   ┌───┬───┬───┬───┐
      *           │   │   │   │   │   │   │   │   │   │
      *           └───┴───┴───┴───┘   └───┴───┴───┴───┘
      */
    [4] = LAYOUT_split_3x6_4(
        _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
                                            _______, _______, _______, _______,          _______, _______, _______, _______
    ),

     /*
      * LAYER 5 - RESERVED (No-op for now)
      * ┌───┬───┬───┬───┬───┬───┐       ┌───┬───┬───┬───┬───┬───┐
      * │   │   │   │   │   │   │       │   │   │   │   │   │   │
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │   │   │   │   │   │       │   │   │   │   │   │   │
      * ├───┼───┼───┼───┼───┼───┤       ├───┼───┼───┼───┼───┼───┤
      * │   │   │   │   │   │   │       │   │   │   │   │   │   │
      * └───┴───┴───┴───┴───┴───┘       └───┴───┴───┴───┴───┴───┘
      *           ┌───┬───┬───┬───┐   ┌───┬───┬───┬───┐
      *           │   │   │   │   │   │   │   │   │   │
      *           └───┴───┴───┴───┘   └───┴───┴───┴───┘
      */
    [5] = LAYOUT_split_3x6_4(
        _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
                                            _______, _______, _______, _______,          _______, _______, _______, _______
    )
};

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

        // Set RGB color based on layer
        switch (current_layer) {
            case 0:  // Base layer - Cyan (closest to #264653)
                rgblight_sethsv_noeeprom(HSV_CYAN);
                break;
            case 1:  // Numbers & Navigation - Teal
                rgblight_sethsv_noeeprom(HSV_TEAL);
                break;
            case 2:  // Symbols & Brackets - Spring green (closest to #8ab17d)
                rgblight_sethsv_noeeprom(HSV_SPRINGGREEN);
                break;
            case 3:  // Function Keys & Media - Gold/Yellow
                rgblight_sethsv_noeeprom(HSV_GOLD);
                break;
            case 4:  // Reserved - Orange
                rgblight_sethsv_noeeprom(HSV_ORANGE);
                break;
            case 5:  // Reserved - Coral
                rgblight_sethsv_noeeprom(HSV_CORAL);
                break;
            default:
                rgblight_sethsv_noeeprom(HSV_CYAN);
                break;
        }
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
    rgblight_mode_noeeprom(RGBLIGHT_MODE_STATIC_LIGHT);  // Solid color mode
    rgblight_sethsv_noeeprom(HSV_CYAN);  // Start with layer 0 color
}

