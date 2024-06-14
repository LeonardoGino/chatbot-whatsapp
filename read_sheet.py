import gspread
import pandas as pd
from config import credentials  # Importar las credenciales desde config.py

# Autenticación y acceso al Google Sheet
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(
    '1TpYk7uNYdfkMK0yDO4QMCi_p05jm4o1h0IFysQ9hgSs').sheet1  # Reemplaza 'your_google_sheet_id' con el ID real de tu Google Sheet

# Obtener los datos como un DataFrame de pandas
data = sheet.get_all_records()
df = pd.DataFrame(data)


def get_crypto_price(crypto_name):
    row = df[df['Cryptocurrency'].str.lower() == crypto_name.lower()]
    if not row.empty:
        return row.iloc[0]['Price (USD)']
    else:
        return None


def get_crypto_commission(crypto_name):
    row = df[df['Cryptocurrency'].str.lower() == crypto_name.lower()]
    if not row.empty:
        return {
            'fixed_commission': row.iloc[0]['Fixed Commission (USDT)'],
            'variable_commission': row.iloc[0]['Variable Commission (%)'],
            'min_amount': row.iloc[0]['Min Amount (USD)']
        }
    else:
        return None
