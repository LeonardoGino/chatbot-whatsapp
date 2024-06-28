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


def get_currency_info(currency_name):
    row = df[df['Moneda'].str.lower() == currency_name.lower()]
    if not row.empty:
        info = {
            'purchase_price': row.iloc[0]['Precio Compra(ARS)'],
            'sale_price': row.iloc[0]['Precio Venta(ARS)'],
            'variable_commission': row.iloc[0]['Comision Variable(%)'],
            'min_amount': row.iloc[0]['Monto minimo (USD)'],
            'fixed_commission': row.iloc[0]['Comision Fija (USD)']
        }
        return info
    else:
        return None


def format_currency_response(currency_name):
    info = get_currency_info(currency_name)
    if info:
        response = (f"El precio del {currency_name} es {info['purchase_price']} para la compra "
                    f"{info['sale_price']} para la venta. Tiene un {info['variable_commission']}% de comisión "
                    f"superando los {info['min_amount']}USD, menos tendría una comisión de {info['fixed_commission']}USD.")
        return response
    else:
        return f"No se encontró información para la moneda {currency_name}."
