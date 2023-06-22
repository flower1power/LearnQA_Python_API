import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

"""Делаем запрос без параметра method"""

response = requests.get(url)
print(response.text)


"""Делаем запрос с нереальным методом, например, HEAD"""

method = "HEAD"
data = {'method': method}

response = requests.get(url, params=data)
print(response.text)


"""Делаем запрос с правильным методом."""

method = "GET"
data = {'method': method}

response = requests.get(url, params=data)
print(response.text)

"""Проверяем все возможные сочетания реальных типов запросов и значений параметра method."""

methods = ["GET", "POST", "PUT", "DELETE"]


for http_method in ["GET", "POST", "PUT", "DELETE"]:
    for method in methods:
        if http_method == "GET":
            response = requests.get(url, params={"method": method})
        else:
            response = requests.request(http_method, url, data={"method": method})

        if response.text == "{\"success\":\"!\"}":
            print(f"{http_method} request with {method} param: OK")
        else:
            print(f"{http_method} request with {method} param: FAIL")

