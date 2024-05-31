import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    WHATSAPP_URL = os.getenv('WHATSAPP_URL')
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
