from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Cargar variables de entorno
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_API_URL = f"https://graph.facebook.com/v13.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args["hub.challenge"], 200
        return "Verification token mismatch", 403
    return "Hello world", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data.get("object") == "whatsapp_business_account":
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    message = change.get("value").get("messages")[0]
                    phone_number = message.get("from")
                    text = message.get("text", {}).get("body", "")
                    process_incoming_message(phone_number, text)
    return jsonify({"status": "received"}), 200

def process_incoming_message(phone_number, text):
    response_message = f"Received your message: {text}"
    send_whatsapp_message(phone_number, response_message)

def send_whatsapp_message(to, message):
    url = WHATSAPP_API_URL
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
