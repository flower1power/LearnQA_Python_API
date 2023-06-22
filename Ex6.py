import requests

url = "https://playground.learnqa.ru/api/long_redirect"
response = requests.get(url, allow_redirects=True)
redirects = response.history
last_url = response.url
print(f"Количество редиректов: {len(redirects)}")
print(f"Итоговый URL: {last_url}")