import allure
import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
@allure.epic("User Get")
class TestUserGet(BaseCase):
    @allure.title("Test getting user details without authentication")
    @allure.description("This test verifies that user details are not accessible without authentication")
    def test_get_user_details_not_auth(self):
        # response = requests.get("https://playground.learnqa.ru/api/user/2")
        response = MyRequests.get("/user/2")
        # print(response.content)
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.title("Test getting user details while authenticated as the same user")
    @allure.description("This test verifies that user details are accessible when authenticated as the same user")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # reponse1 = requests.post("https://playground.learnqa.ru/api/user/login", data = data)
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")
        user_id_from_auth_metod = self.get_json_value(response1, "user_id")

        # response2 = requests.get(
        #     f"https://playground.learnqa.ru/api/user/{user_id_from_auth_metod}",
        #     headers={"x-csrf-token": token},
        #     cookies={"auth_sid": auth_sid}
        # )
        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_metod}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)
        # Assertions.assert_json_has_key(response2, "username")
        # Assertions.assert_json_has_not_key(response2, "email")
        # Assertions.assert_json_has_not_key(response2, "firstName")
        # Assertions.assert_json_has_not_key(response2, "lastName")

    @allure.title("Test getting user details while authenticated as a different user")
    @allure.description(
        "This test verifies that user details are not accessible when authenticated as a different user")
    def test_get_user_details_auth_as_different_user(self):
        # Авторизуемся одним пользователем
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_headers(response1, "x-csrf-token")

        # Получаем данные о другом пользователе с ID 1
        user_id = 1

        # Запрашиваем данные другого пользователя с использованием его ID
        response2 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        # Проверяем, что ответ содержит только поле "username"
        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")





