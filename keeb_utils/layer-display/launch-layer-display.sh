#!/bin/bash
# Launch script for Layer Display menubar app

# Get the directory where this script lives
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to project directory
cd "$SCRIPT_DIR"

# Find the latest uv binary (version-agnostic)
UV_BIN=$(find ~/.asdf/installs/uv/*/bin/uv -type f 2>/dev/null | sort -V | tail -1)

if [ -z "$UV_BIN" ]; then
    echo "Error: uv not found in ~/.asdf/installs/uv/"
    exit 1
fi

# Run with uv
"$UV_BIN" run layer-display
