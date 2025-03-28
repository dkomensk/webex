from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    message = data["text"]
    response_message = process_message(message)
    send_response(response_message)
    return "", 200

def process_message(message):
    if "hello" in message.lower():
        return "Hello! How can I assist you?"
    else:
        return "Sorry, I didn't understand that."

def send_response(message):
    webex_url = "https://webexapis.com/v1/messages"
    payload = {
        "roomId": "your-room-id",
        "text": message
    }
    headers = {
        "Authorization": "Bearer your-webex-token"
    }
    requests.post(webex_url, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(debug=True)
