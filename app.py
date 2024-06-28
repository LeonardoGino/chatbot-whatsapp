from flask import Flask, request, jsonify
import requests
from config import Config
from bot import WhatsAppBot
from datetime import datetime

app = Flask(__name__)

WHATSAPP_TOKEN = Config.WHATSAPP_TOKEN
WHATSAPP_PHONE_NUMBER_ID = Config.WHATSAPP_PHONE_NUMBER_ID
VERIFY_TOKEN = Config.VERIFY_TOKEN
WHATSAPP_API_URL = f"https://graph.facebook.com/v13.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

bot = WhatsAppBot()

# Diccionario para rastrear si un usuario ha sido saludado y la última fecha de saludo
greeted_users = {}


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
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    if change.get("field") == "messages":
                        try:
                            message = change.get("value", {}).get("messages", [None])[0]
                            if message is None:
                                continue
                            phone_number = process_telephone_number(message.get("from"))
                            text = message.get("text", {}).get("body", "")

                            if should_greet_user(phone_number):
                                send_whatsapp_message(phone_number, {
                                    "template_name": "greeting_template",
                                    "components": [{"type": "body", "parameters": [{"type": "text", "text": "¡Hola! ¿Cómo estas?"}]}]
                                })
                            greeted_users[phone_number] = datetime.now().date()

                            response = bot.generate_response_message(text)
                            send_whatsapp_message(phone_number, response)
                        except Exception as e:
                            print(f"Error processing message: {e}")
        return jsonify({"status": "received"}), 200
    else:
        return jsonify({"status": "not a json request"}), 400


def should_greet_user(phone_number):
    today = datetime.now().date()
    last_greeted = greeted_users.get(phone_number)
    return last_greeted is None or last_greeted != today


def process_telephone_number(telephone_number):
    if telephone_number.startswith("54") and len(telephone_number) > 2 and telephone_number[2] == "9":
        return telephone_number[:2] + telephone_number[3:]
    return telephone_number


def send_whatsapp_message(phone_number, message):
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": message["template_name"],
            "language": {"code": "es_AR"},
            "components": message["components"]
        }
    }
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    return response.status_code
