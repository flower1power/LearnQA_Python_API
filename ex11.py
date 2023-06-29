import requests

response = requests.get("https://playground.learnqa.ru/api/homework_cookie")

assert response.status_code == 200, f"Status code {response.status_code}"
cookies_value = response.cookies.get("HomeWork")
assert cookies_value is not None, "Cookie value Nan"
print (f"Cookie value: {cookies_value}")

