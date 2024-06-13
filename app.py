from flask import Flask, request, jsonify
import requests
from config import Config  # Importar la configuración
from bot import WhatsAppBot  # Importar la clase WhatsAppBot
import spacy
import subprocess

app = Flask(__name__)

# Variables de entorno
WHATSAPP_TOKEN = Config.WHATSAPP_TOKEN
WHATSAPP_PHONE_NUMBER_ID = Config.WHATSAPP_PHONE_NUMBER_ID
VERIFY_TOKEN = Config.VERIFY_TOKEN
WHATSAPP_API_URL = f"https://graph.facebook.com/v13.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

# Verificar y descargar el modelo de spaCy si no está disponible
def ensure_spacy_model():
    try:
        nlp = spacy.load('es_core_news_sm')
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])
        nlp = spacy.load('es_core_news_sm')
    return nlp

# Cargar el modelo de spaCy
nlp = spacy.load('es_core_news_sm')
bot = WhatsAppBot(nlp)

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
                            phone_number = message.get("from")
                            text = message.get("text", {}).get("body", "")
                            process_incoming_message(phone_number, text)
                        except Exception as e:
                            print(f"Error processing message: {e}")
        return jsonify({"status": "received"}), 200
    else:
        return jsonify({"status": "not a json request"}), 400

def process_incoming_message(phone_number, text):
    try:
        response_template = bot.generate_response_message(text)
        send_whatsapp_message(phone_number, response_template)
    except Exception as e:
        print(f"Error in process_incoming_message: {e}")

def send_whatsapp_message(to, template):
    url = WHATSAPP_API_URL
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template["template_name"],
            "language": {"code": "es"},
            "components": template["components"]
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Esto lanzará un error para códigos de estado 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
