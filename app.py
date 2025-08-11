from flask import Flask, request, jsonify
from functools import wraps
from datetime import datetime
from database import save_device_info, save_log, devices_collection, logs_collection
from config import API_KEY

app = Flask(__name__)

# ------------------ AUTH DECORATOR ------------------ #
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-KEY")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

# ------------------ ROUTES ------------------ #

@app.route("/api/device", methods=["POST"])
@require_api_key
def device_data():
    """Receive device info from monitoring app"""
    data = request.json or {}
    data["timestamp"] = datetime.utcnow()
    save_device_info(data)
    save_log({"type": "device_info", "data": data, "timestamp": datetime.utcnow()})
    return jsonify({"status": "success"}), 200

@app.route("/api/log", methods=["POST"])
@require_api_key
def log_data():
    """Receive logs from monitoring app"""
    data = request.json or {}
    data["timestamp"] = datetime.utcnow()
    save_log(data)
    return jsonify({"status": "log saved"}), 200

@app.route("/api/devices", methods=["GET"])
@require_api_key
def list_devices():
    """Return all devices"""
    devices = list(devices_collection.find({}, {"_id": 0}))
    return jsonify(devices), 200

@app.route("/api/logs", methods=["GET"])
@require_api_key
def list_logs():
    """Return all logs"""
    logs = list(logs_collection.find({}, {"_id": 0}))
    return jsonify(logs), 200

# ------------------ START SERVER ------------------ #
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)