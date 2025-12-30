## Moon Knight V4 Keyboard Pinout (Per Side)

### Matrix (4 rows × 6 columns)
**Rows:**
- Row 0: GPIO 4
- Row 1: GPIO 5
- Row 2: GPIO 6
- Row 3: GPIO 7

**Columns:**
- Col 0: GPIO 8
- Col 1: GPIO 9
- Col 2: GPIO 20
- Col 3: GPIO 21
- Col 4: GPIO 22
- Col 5: GPIO 23

### LEDs (27 addressable per side)
- LED Data: GPIO 25 (5V RGB output)

### TRRS Split Communication
- TX: GPIO 0 (UART transmit)
- RX: GPIO 1 (UART receive)

### OLED Display
- SDA: GPIO 2 (I2C data)
- SCL: GPIO 3 (I2C clock)

### Pin Summary
Total pins used: 15
- Matrix: 10 pins (4 rows + 6 cols)
- RGB LEDs: 1 pin
- TRRS: 2 pins
- OLED: 2 pins

### Unusable Pins
- **D+, D-** - USB data (required)
- **RAW, GND, 3V3, nRST** - Power/reset lines
- **GPIO 12-16** - Bottom pads (avoiding per requirements)

### Available GPIO Pins
Total available: 18 pins (0-11, 20-23, 26-29)
Used: 15 pins
Remaining: GPIO 10, 11, 26 (3 pins free for expansion)
