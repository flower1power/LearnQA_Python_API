import time
import requests

"""Создаем задачу и получаем токен"""
url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url)
json_response = response.json()
token = json_response["token"]
seconds = json_response["seconds"]
print(f"Created job with token: {token} and delay of {seconds} seconds")

"""Проверяем статус задачи (должен быть "Job is NOT ready")"""
response = requests.get(url, params={"token": token})
json_response = response.json()
status = json_response["status"]
print(f"Job status: {status}")

"""Ждем нужное количество секунд"""
print(f"Job is running, waiting for {seconds} seconds...")
time.sleep(seconds)

"""Проверяем статус и результат задачи"""
response = requests.get(url, params={"token": token})
json_response = response.json()
status = json_response["status"]
print(f"Job status: {status}")

if status == "Job is ready":
    result = json_response.get("result")
    print(f"Job is ready with result: {result}")