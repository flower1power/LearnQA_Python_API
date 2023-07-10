import json.decoder
from datetime import datetime
from requests import Response


class BaseCase:
    def get_cookie (self, response: Response, coockie_name):
        assert coockie_name in response.cookies, f"Cannot find cookie with name {coockie_name} in the last response"
        return response.cookies[coockie_name]

    def get_headers (self, response: Response, headers_name):
        assert  headers_name in response.headers, f"Cannot find heder with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Respons is not in JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Respons JSON doesn`t have key '{name}'"

        return response_as_dict[name]


    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }