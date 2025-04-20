import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess
import atexit
from box import Box
import yaml
from gui import ASSETS_DIR, CONFIG_PATH, JS_SCRIPT_PATH, GUI_DIR
import socket 

# Load config.yaml
with open(CONFIG_PATH, "r") as file:
    config = Box(yaml.safe_load(file))

# Global process tracker
web_processes = []


# Cleanup to terminate all web server processes on exit
def cleanup_processes():
    print("🧹 Cleaning up web server processes...")
    for proc in web_processes:
        if proc.poll() is None:  # still running
            try:
                proc.terminate()
                proc.wait(timeout=5)
                print(f"✅ Terminated process PID {proc.pid}")
            except Exception as e:
                print(f"⚠️ Could not terminate process PID {proc.pid}: {e}")
        else:
            print(f"ℹ️ Process PID {proc.pid} already exited")

atexit.register(cleanup_processes)  # always run on exit

def free_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def kill_process_on_port(port):
    import subprocess
    try:
        output = subprocess.check_output(["lsof", "-ti", f":{port}"])
        pids = output.decode().splitlines()
        for pid in pids:
            subprocess.run(["kill", "-9", pid])
            print(f"🔪 Killed process on port {port}, PID {pid}")
    except subprocess.CalledProcessError:
        print(f"✅ Port {port} already free")


def run_web():
    print("🔘 Button pressed: run_web() triggered")

    # === Open QR Code ===
    image_path = os.path.join(ASSETS_DIR, "qr.png")
    if not os.path.exists(image_path):
        print("❌ QR image not found at", image_path)
        return

    img_win = tk.Toplevel()
    img_win.title("📷 Remote QR")
    img_win.configure(bg="#1a1f2c")

    img = Image.open(image_path)
    img = img.resize((500, 400))
    tk_img = ImageTk.PhotoImage(img)
    tk.Label(img_win, image=tk_img, bg="#1a1f2c").pack(padx=10, pady=10)
    img_win.image = tk_img

    # === Launch Node.js server ===
    print(f"🚀 Launching Node.js from: {JS_SCRIPT_PATH}")
    try:

    # Build absolute path to server.js
        server_js = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web-app", "server.js"))
        # Launch Node.js server with correct working directory
        node_proc = subprocess.Popen(["node", server_js], cwd=os.path.dirname(server_js))
        web_processes.append(node_proc)
    except Exception as e:
        print("❌ Failed to start Node.js server:", e)
