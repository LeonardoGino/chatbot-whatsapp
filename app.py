from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Variables de entorno
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
    if request.is_json:
        data = request.get_json()
        print(f"Webhook received data: {data}")  # Debugging
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    if change.get("field") == "messages":
                        message = change.get("value").get("messages")[0]
                        phone_number = message.get("from")
                        phone_number = format_phone_number(phone_number)  # Formatear número de teléfono
                        text = message.get("text", {}).get("body", "")
                        process_incoming_message(phone_number, text)
        return jsonify({"status": "received"}), 200
    else:
        return "Unsupported Media Type", 415

def format_phone_number(phone_number):
    if phone_number.startswith("549"):
        # Cambia "549" a "54" si el número empieza con "549"
        return "54" + phone_number[3:]
    return phone_number

def process_incoming_message(phone_number, text):
    response_message = f"Received your message: {text}"
    print(f"Processing incoming message from {phone_number}: {text}")  # Debugging
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
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Sending message to {to}: {message}")
        print(f"Response: {response.status_code}, {response.text}")
        response.raise_for_status()  # Esto lanzará un error para códigos de estado 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
