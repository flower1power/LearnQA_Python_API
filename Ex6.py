import requests

url = "https://playground.learnqa.ru/api/long_redirect"
response = requests.get(url, allow_redirects=True)
first_response = response.history[0]
second_response = response.history[1]
hz_response = response
print(first_response.url)
print(second_response.url)
print(hz_response.url)