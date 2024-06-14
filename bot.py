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
        return re.search(r'\bprecio\b.*\bde\b', text.lower()) is not None

    def handle_price_query(self, text):
        # Extraer el nombre de la criptomoneda usando una expresión regular
        match = re.search(r'\bprecio\b.*\bde\b\s+(\w+)', text.lower())
        crypto_name = match.group(1) if match else None

        if crypto_name:
            price = read_sheet.get_crypto_price(crypto_name)
            commission_info = read_sheet.get_crypto_commission(crypto_name)
            if price is not None and commission_info is not None:
                fixed_commission = commission_info['fixed_commission']
                variable_commission = commission_info['variable_commission']
                min_amount = commission_info['min_amount']
                return self.create_template_response("price_query_success",
                                                     [crypto_name, str(price), str(fixed_commission),
                                                      str(variable_commission), str(min_amount)])
            else:
                return self.create_template_response("price_query_failure", [crypto_name])
        else:
            return self.create_template_response("price_query_failure", [crypto_name])

    @staticmethod
    def create_template_response(template_name, parameters):
        return {
            "template_name": template_name,
            "components": [{"type": "body", "parameters": [{"type": "text", "text": param} for param in parameters]}]
        }
