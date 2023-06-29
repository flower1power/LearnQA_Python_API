import requests

response = requests.get("https://playground.learnqa.ru/api/homework_header")

assert response.status_code == 200, f"Status code {response.status_code}"
headers_value = response.headers
assert headers_value is not None, "Headers value Nan"
print("Заголовки (headers):")
for header, value in headers_value.items():
    print(f"{header}: {value}")