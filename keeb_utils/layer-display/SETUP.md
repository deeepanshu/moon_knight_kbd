# Layer Display Setup

## Running at Login (Recommended)

### Option 1: macOS Login Items (Simplest)

1. **Open the script in Automator:**
   - Open **Automator** (search in Spotlight)
   - Create new **Application**
   - Add action: "Run Shell Script"
   - Paste this:
     ```bash
     /Users/djain/Desktop/moon_knight_kbd/keeb_utils/layer-display/launch-layer-display.sh
     ```
   - Save as: `LayerDisplay.app` (save to Desktop or Applications)

2. **Add to Login Items:**
   - Open **System Settings** → **General** → **Login Items**
   - Click **+** under "Open at Login"
   - Select `LayerDisplay.app`
   - Done! It will start automatically on login

### Option 2: launchd (More Robust)

Create a LaunchAgent that survives crashes and runs in background:

```bash
# Create LaunchAgent directory if it doesn't exist
mkdir -p ~/Library/LaunchAgents

# Create plist file (already provided below)
# Then load it:
launchctl load ~/Library/LaunchAgents/com.user.layer-display.plist

# To unload:
launchctl unload ~/Library/LaunchAgents/com.user.layer-display.plist
```

**Note:** I can generate the plist file if you want this option.

### Option 3: Build .app Bundle (Best UX, Most Complex)

Requires installing py2app and building a proper macOS application.

## Manual Launch

Just double-click `launch-layer-display.sh` (or run from terminal)

## Current Status

- ✅ Menubar app displays "Layer 0"
- ✅ Shows dropdown menu with Hello World and layer list
- ⏳ HID communication not yet wired up
- ⏳ Firmware doesn't send layer data yet

## Next Steps

1. Extract VID/PID from keyboard firmware
2. Add Raw HID to QMK firmware
3. Wire up HID listener to update menubar text
