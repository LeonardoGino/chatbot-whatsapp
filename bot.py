import spacy
from spacy.lang.es.stop_words import STOP_WORDS
from read_sheet import get_crypto_price, get_crypto_commission  # Importar las funciones


class WhatsAppBot:
    def __init__(self, nlp_model):
        self.nlp = nlp_model

    def generate_response_message(self, text):
        try:
            doc = self.nlp(text.lower())
            tokens = [token.text for token in doc if token.text not in STOP_WORDS and not token.is_punct]

            if 'precio' in tokens and 'de' in tokens:
                return self.handle_price_query(tokens)
            else:
                return self.create_template_response("unknown_query", [text])
        except Exception as e:
            print(f"Error in generate_response_message: {e}")
            return self.create_template_response("error_message", [])

    def handle_price_query(self, tokens):
        crypto_name = self.get_crypto_name(tokens)
        if crypto_name:
            price = get_crypto_price(crypto_name)
            commission_info = get_crypto_commission(crypto_name)
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
            return self.create_template_response("price_query_failure", ["no especificada"])

    def get_crypto_name(self, tokens):
        try:
            # Buscar la posición de 'de' y obtener el token siguiente como el nombre de la criptomoneda
            de_index = tokens.index('de')
            if de_index + 1 < len(tokens):
                return tokens[de_index + 1]
            else:
                return None
        except ValueError:
            return None

    def create_template_response(self, template_name, parameters):
        return {
            "template_name": template_name,
            "components": [{"type": "body", "parameters": [{"type": "text", "text": param} for param in parameters]}]
        }
