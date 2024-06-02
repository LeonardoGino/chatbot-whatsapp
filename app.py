import requests
from flask import Flask, render_template, request, Blueprint, json, jsonify

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
main = Blueprint('main', __name__)


@app.route('/')
def index():
    return (render_template('index.html'))


@app.route('/debuglog', methods=['GET'])
def log_properties():
    whatsapp_phone_number = Config.WHATSAPP_PHONE_NUMBER_ID
    whatsapp_token = Config.WHATSAPP_TOKEN
    whatsapp_url = Config.WHATSAPP_URL
    verify_token = Config.VERIFY_TOKEN
    return f"Whatsapp phone number {whatsapp_phone_number} \n Whatsapp token {whatsapp_token} \n Whatsapp URL {whatsapp_url} \n verify token {verify_token}", 200


@app.route('/webhook', methods=['GET'])
def webhook_verification():
    verify_token = Config.VERIFY_TOKEN
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
        if mode == 'subscribe' and token == verify_token:
            return 'Hello world VERIFY TOKEN', challenge, 200
        else:
            return 'Verification token mismatch', 403
    return 'Hello world', 200


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if data.get('object') == 'whatsapp_business_account':
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                value = change.get('value')
                messages = value.get('messages')
                if messages:
                    for message in messages:
                        phone_number = message['from']
                        respuesta = "Hola! Soy un botardo"
                        send_whatsapp_message(phone_number, respuesta)
    return jsonify({'status': 'received'})


def send_whatsapp_message(to, body):
    url = f"https://graph.facebook.com/v14.0/{Config.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {Config.META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": body
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


if __name__ == '__main__':
    app.run(debug=True)
