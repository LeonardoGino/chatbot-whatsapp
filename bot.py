import re
import read_sheet

class WhatsAppBot:
    def __init__(self):
        self.price_patterns = [
            re.compile(r'\bprecio\b.*\b(de|del)\b\s+(\w+)'),  # "precio de/del ..."
            re.compile(r'\bcu[aá]nto\b.*\bcuesta\b\s+(\w+)'),  # "cuánto cuesta ..."
            re.compile(r'\bvalor\b.*\b(de|del)\b\s+(\w+)'),  # "valor de/del ..."
            re.compile(r'\bcosto\b.*\b(de|del)\b\s+(\w+)'),  # "costo de/del ..."
            re.compile(r'\bcu[aá]l es el precio\b.*\b(de|del)\b\s+(\w+)'),  # "cuál es el precio de/del ..."
            re.compile(r'\bcu[aá]l es el valor\b.*\b(de|del)\b\s+(\w+)')  # "cuál es el valor de/del ..."
        ]

    def generate_response_message(self, text):
        try:
            query_info = self.is_price_query(text)
            if query_info:
                return self.handle_price_query(query_info)
            else:
                return self.create_template_response("unknown_query", [])
        except Exception as e:
            print(f"Error in generate_response_message: {e}")
            return self.create_template_response("error_message", [str(e)])

    def is_price_query(self, text):
        text_lower = text.lower()
        for pattern in self.price_patterns:
            match = pattern.search(text_lower)
            if match:
                return match.group(2)  # Devuelve el nombre de la moneda si coincide
        return None

    def handle_price_query(self, currency_name):
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

    @staticmethod
    def create_template_response(template_name, parameters):
        return {
            "template_name": template_name,
            "components": [{"type": "body", "parameters": [{"type": "text", "text": param} for param in parameters]}]
        }
