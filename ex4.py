import requests

respons = requests.get("https://playground.learnqa.ru/api/get_text")
print(respons.text)