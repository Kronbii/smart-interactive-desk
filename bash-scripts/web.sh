#!/usr/bin/env bash

#######################################################
# CONFIGURATION
#######################################################
PORT=3000
TARGET_DIR="/home/kronbii/github-repos/smart-interactive-desk/koubeisically/web-app" #TODO: make this take ur corrent working directory and cd to the desired
SERVER_SCRIPT="server.js"
#TODO: make the targer dir of the log file a variable

#######################################################
# 1. Kill any existing processes on the port
#######################################################
# Option A: Using fuser (Linux)
echo "Killing any existing processes on port $PORT..."
fuser -k "${PORT}/tcp" 2>/dev/null

# Option B: Using lsof + kill (if fuser is not installed)
# lsof -i :$PORT -t 2>/dev/null | xargs kill -9

#######################################################
# 2. Start the server in the background, capture logs
#######################################################
cd "$TARGET_DIR" || {
  echo "Error: Could not change directory to $TARGET_DIR."
  exit 1
}

echo "Starting Node server..."
node "$SERVER_SCRIPT" > server_output.log 2>&1 &
NODE_PID=$!

# Automatically kill the new Node process when this script exits
trap 'echo "Killing Node process (PID: $NODE_PID)..."; kill $NODE_PID 2>/dev/null' EXIT

# Give server a moment to start
sleep 2

#######################################################
# 3. Check logs for errors (e.g., EADDRINUSE)
#######################################################
if grep -qi "EADDRINUSE" server_output.log; then
  echo "Error: Port $PORT is still in use or another EADDRINUSE error occurred."
  exit 1
fi

if grep -qi "Error:" server_output.log; then
  echo "Error found in server_output.log"
  exit 1
fi

#######################################################
# 4. Parse logs for 'Server started at http://...'
#######################################################
URL=$(grep -oP 'Server running on \K.*' server_output.log)
URL="${URL}/front.html"

if [ -z "$URL" ]; then
  echo "Could not find 'Server running on http://...' in server_output.log"
  exit 1
fi

echo "Server is running! Opening $URL in browser..."

# 5. Open the URL in the default browser (Linux)
xdg-open "$URL" >/dev/null 2>&1

# For macOS, replace with: open "$URL"
# For Windows (Git Bash / Cygwin): cmd.exe /c start "$URL"

#######################################################
# 6. (Optional) Keep script alive until user presses Enter
#    so the server stays up. Once the script exits,
#    trap above kills the Node process automatically.
#######################################################
echo "Press Enter to stop the server..."
read -r
echo "Script ending. Node process will be killed by the 'trap'."
