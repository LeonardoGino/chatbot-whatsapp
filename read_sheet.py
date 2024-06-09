import gspread
import pandas as pd
from config import credentials  # Importar las credenciales desde config.py

# Autenticación y acceso al Google Sheet
gc = gspread.authorize(credentials)
sheet = gc.open_by_key('your_google_sheet_id').sheet1  # Reemplaza 'your_google_sheet_id' con el ID real de tu Google Sheet

# Obtener los datos como un DataFrame de pandas
data = sheet.get_all_records()
df = pd.DataFrame(data)

def get_crypto_price(crypto_name):
    row = df[df['Cryptocurrency'].str.lower() == crypto_name.lower()]
    if not row.empty:
        return row.iloc[0]['Price (USD)']
    else:
        return None
