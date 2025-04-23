#!/bin/bash

# === Navigate to base project directory ===
cd /home/bemo/smart-interactive-desk

# === Activate Python virtual environment ===
source bemo/bin/activate

# === Start Python Bridge (background) ===
cd model
python3 -m gui.main &
BRIDGE_PID=$!

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
