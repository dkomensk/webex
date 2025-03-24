import requests
import os

WEBEX_BOT_TOKEN = os.getenv("WEBEX_BOT_TOKEN")  # Získa token z env. premenných
WEBHOOK_URL = "https://webexbotapp-b6efh2bxb7dsbphz.germanywestcentral-01.azurewebsites.net/webhook"  # Verejná URL tvojho chatbota

headers = {
    "Authorization": f"Bearer {WEBEX_BOT_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "name": "WebexChatbotWebhook",
    "targetUrl": WEBHOOK_URL,
    "resource": "messages",
    "event": "created"
}

response = requests.post("https://webexapis.com/v1/webhooks", headers=headers, json=payload)

if response.status_code == 200:
    print("Webhook successfully created!")
else:
    print("Error:", response.json())
