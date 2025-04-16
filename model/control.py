import json
import fcntl
import os
CONTROL_FILE = os.path.join(os.path.dirname(__file__), 'control.json')
USER_FILE = 'users.json'
HISTORY_FILE = 'history.json'

def read_json(path):
    with open(path, 'r') as f:
        fcntl.flock(f, fcntl.LOCK_SH)  # Shared lock (multiple readers allowed)
        data = json.load(f)
        fcntl.flock(f, fcntl.LOCK_UN)
        return data

def write_json(path, data):
    with open(path, 'w') as f:
        fcntl.flock(f, fcntl.LOCK_EX)  # Exclusive lock (only 1 writer allowed)
        json.dump(data, f, indent=2)
        fcntl.flock(f, fcntl.LOCK_UN)

def get_control():
    return read_json(CONTROL_FILE)

def set_control(data):
    write_json(CONTROL_FILE, data)

def set_command(cmd):
    data = get_control()
    data['command'] = cmd
    set_control(data)

def set_mode(mode):
    data = get_control()
    data['mode'] = mode
    data['command'] = "none"
    set_control(data)

def update_sensor_feedback(height, tilt):
    data = get_control()
    data['sensor_feedback'] = {"height": height, "tilt": tilt}
    set_control(data)
    
def get_sensor_feedback():
    data = get_control()
    feedback = data['sensor_feedback']
    return feedback['height'], feedback['tilt']

def get_users():
    return read_json(USER_FILE)['users']
