import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Získanie Webex Bot Tokenu z environmentálnej premennej
WEBEX_BOT_TOKEN = os.getenv("WEBEX_BOT_TOKEN")

# Webex API URL
WEBEX_API_URL = "https://webexapis.com/v1/messages"

@app.route("/", methods=["GET"])
def home():
    return "Webex Chatbot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "data" in data:
        message_id = data["data"]["id"]
        sender_email = data["data"]["personEmail"]
        
        # Zabráni odpovedaniu botovi samému
        if sender_email.endswith("@webex.bot"):
            return "Ignoring bot messages", 200
        
        # Získanie textu správy
        headers = {"Authorization": f"Bearer {WEBEX_BOT_TOKEN}"}
        response = requests.get(f"{WEBEX_API_URL}/{message_id}", headers=headers)
        message_text = response.json().get("text", "").lower()
        
        # Odpoveď na správu
        reply_text = "Neznáma požiadavka."
        if "hello" in message_text:
            reply_text = "Hello! How can I assist you?"
        elif "help" in message_text:
            reply_text = "Available commands: hello, help."

        # Odoslanie odpovede
        payload = {"roomId": data["data"]["roomId"], "text": reply_text}
        requests.post(WEBEX_API_URL, headers=headers, json=payload)

    return jsonify({"message": "Processed"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
