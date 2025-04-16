#!/bin/bash

# === Navigate to base project directory ===
cd "$(dirname "$0")/.."

# === Activate Python virtual environment ===
source bemo/bin/activate

# === Start Python Bridge (background) ===
cd model
python3 bridge.py &
BRIDGE_PID=$!

# === Start GUI (foreground) ===
cd gui
python3 gui.py &
GUI_PID=$!

# === Handle KeyboardInterrupt ===
cleanup() {
    echo -e "\n🛑 Stopping all processes..."
    kill $BRIDGE_PID $GUI_PID $SERVER_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT

# === Keep the script running until interrupted ===
echo "🟢 All systems started. Press Ctrl+C to stop."
wait
