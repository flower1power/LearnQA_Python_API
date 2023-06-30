import requests

response = requests.get("https://playground.learnqa.ru/api/homework_header")

assert response.status_code == 200, f"Status code {response.status_code}"
headers_value = response.headers
assert headers_value is not None, "Headers value Nan"
keys = ['Date', 'Content-Type', 'Content-Length', 'Connection', 'Keep-Alive', 'Server', 'x-secret-homework-header', 'Cache-Control', 'Expires']
for key in headers_value:
    if key in keys:
        print(f"Ключ {key} присутсвует как в полученных headers, так и в ожидаемых")
    else:
        print(f"Ключ {key} отсутсвует в ожидаемых")

print("Заголовки (headers):")
for header, value in headers_value.items():
    print(f"{header}: {value}")



