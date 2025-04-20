from flask import Flask, request, jsonify
from init_serial import send_command

app = Flask(__name__)

@app.route('/send-command', methods=['POST'])
def handle_command():
    data = request.get_json()
    cmd = data.get("command")
    if not cmd:
        return jsonify({"error": "No command received"}), 400
    try:
        print(f"🛠️ Received from Node.js: {cmd}", flush=True)  # ensures it prints live
        send_command(cmd)
        return jsonify({"status": "success", "echo": cmd})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, host='localhost')