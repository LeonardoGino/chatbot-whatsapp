import os
import json
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

class Config:
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    WHATSAPP_URL = os.getenv('WHATSAPP_URL')
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
    GOOGLE_SHEETS_CREDENTIALS = json.loads(os.getenv('GOOGLE_SHEETS_CREDENTIALS'))

# Cargar las credenciales desde las variables de entorno
credentials_info = json.loads(os.getenv('GOOGLE_SHEETS_CREDENTIALS'))
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
