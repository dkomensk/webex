import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Načítanie API tokenu z environmentálnych premenných
WEBEX_BOT_TOKEN = os.getenv("WEBEX_BOT_TOKEN")
WEBEX_API_URL = "https://webexapis.com/v1"

# Hlavičky pre Webex API
HEADERS = {
    "Authorization": f"Bearer {WEBEX_BOT_TOKEN}",
    "Content-Type": "application/json"
}

# Slovník s odpoveďami na príkazy
COMMANDS = {
    "hello": "Hello! How can I assist you today?",
    "help": "You can ask me questions like:\n- 'hello' to greet me\n- 'help' to see this message\n- 'info' to learn about me",
    "info": "I am a Webex chatbot designed to assist with common queries."
}

def send_webex_message(room_id, message):
    """Odosiela správu do Webex miestnosti"""
    payload = {"roomId": room_id, "text": message}
    response = requests.post(f"{WEBEX_API_URL}/messages", headers=HEADERS, json=payload)
    return response.json()

@app.route("/", methods=["GET"])
def home():
    """Základná stránka pre kontrolu stavu servera"""
    return "Webex Chatbot is running!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    """Spracovanie prichádzajúcich správ z Webexu"""
    data = request.json

    # Overenie, či správa obsahuje údaje
    if "data" in data:
        message_id = data["data"]["id"]
        room_id = data["data"]["roomId"]
        
        # Získanie obsahu správy
        message = get_message_text(message_id)

        # Kontrola, či správa obsahuje známy príkaz
        response_text = COMMANDS.get(message.lower(), "Sorry, I didn't understand that. Type 'help' for a list of commands.")
        
        # Odpovedanie na správu
        send_webex_message(room_id, response_text)

    return jsonify({"status": "ok"}), 200

def get_message_text(message_id):
    """Získanie textu správy na základe jej ID"""
    response = requests.get(f"{WEBEX_API_URL}/messages/{message_id}", headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("text", "")
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
