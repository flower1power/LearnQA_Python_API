import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):
    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # Авторизуемся пользователем с ID 2
        response = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_headers(response, "x-csrf-token")


        # Попытка удаления пользователя с ID 2
        response_delete = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Проверка статуса кода и содержимого ответа
        Assertions.asert_code_status(response_delete, 400)
        assert response_delete.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5."

    def test_delete_user_positive(self):
        # Создаем нового пользователя
        register_data = self.prepare_registration_data()
        response_register = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response_register, "id")

        # Авторизуемся под созданным пользователем
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_headers(response_login, "x-csrf-token")

        # Удаляем пользователя
        response_delete = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Проверка статуса кода
        Assertions.asert_code_status(response_delete, 200)

        # Попытка получения данных удаленного пользователя
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Проверка статуса кода и содержимого ответа
        Assertions.asert_code_status(response_get, 404)
        assert response_get.content.decode("utf-8") == "User not found"

    def test_delete_user_authorized_as_another_user(self):
        # Создаем user1
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        user_id1 = self.get_json_value(response1, "id")

        # Создаем user2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)
        user_id2 = self.get_json_value(response2, "id")

        # Авторизируемся как user1
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_headers(response3, "x-csrf-token")

        # Удаляем user2 как user1
        response4 = MyRequests.delete(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.asert_code_status(response4, 400)
        assert response4.content.decode("utf-8") == "Error deleting user"







