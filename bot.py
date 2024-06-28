import re

import read_sheet


class WhatsAppBot:
    def __init__(self):
        pass

    def generate_response_message(self, text):
        try:
            if self.is_price_query(text):
                return self.handle_price_query(text)
            else:
                return self.create_template_response("unknown_query", [])
        except Exception as e:
            print(f"Error in generate_response_message: {e}")
            return self.create_template_response("error_message", [str(e)])

    @staticmethod
    def is_price_query(text):
        # Patrones comunes para detectar consultas sobre precios
        patterns = [
            r'\bprecio\b.*\bde\b',            # "precio de ..."
            r'\bcuánto\b.*\bcuesta\b',        # "cuánto cuesta ..."
            r'\bvalor\b.*\bde\b',             # "valor de ..."
            r'\bcosto\b.*\bde\b',             # "costo de ..."
            r'\bcuál es el precio\b.*\bde\b', # "cuál es el precio de ..."
            r'\bcuál es el valor\b.*\bde\b'   # "cuál es el valor de ..."
        ]
        # Compilar patrones y verificar si alguno coincide con el texto
        for pattern in patterns:
            if re.search(pattern, text.lower()):
                return True
        return False

    def handle_price_query(self, text):
        match = re.search(r'\bprecio\b.*\bde\b\s+(\w+)', text.lower())
        currency_name = match.group(1) if match else None

        if currency_name:
            info = read_sheet.get_currency_info(currency_name)
            if info is not None:
                return self.create_template_response(
                    "price_query_success",
                    [
                        currency_name.capitalize(),
                        str(info['purchase_price']),
                        str(info['sale_price']),
                        str(info['variable_commission']),
                        str(info['min_amount']),
                        str(info['fixed_commission'])
                    ]
                )
            else:
                return self.create_template_response("price_query_failure", [currency_name])
        else:
            return self.create_template_response("price_query_failure", [currency_name])

    @staticmethod
    def create_template_response(template_name, parameters):
        return {
            "template_name": template_name,
            "components": [{"type": "body", "parameters": [{"type": "text", "text": param} for param in parameters]}]
        }
