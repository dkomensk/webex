import os
from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
import requests

app = Flask(__name__)

WEBEX_BOT_TOKEN = os.getenv("WEBEX_BOT_TOKEN")
WEBEX_API_URL = "https://webexapis.com/v1/messages"

def send_webex_message(room_id, message):
    headers = {
        "Authorization": f"Bearer {WEBEX_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"roomId": room_id, "text": message}
    response = requests.post(WEBEX_API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/", methods=["GET"])
def home():
    return "Webex Chatbot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "data" in data:
        room_id = data["data"]["roomId"]
        send_webex_message(room_id, "Hello! How can I assist you?")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
