import allure
import pytest
import requests
from parameterized import parameterized

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
# from datetime import datetime


@allure.epic("User Registration")
class TestUserRegister(BaseCase):
    # def setup(self):
    #     base_part = "learnqa"
    #     domain = "example.com"
    #     random_part = datetime.now().strftime("%m%d%Y%H%M%S")
    #     self.email = f"{base_part}{random_part}@{domain}"



    @allure.title("Test creating a user successfully")
    @allure.description("This test verifies that a user can be created successfully")
    def test_craete_user_successfully(self):

        data = self.prepare_registration_data()
        # data = {
        #     'password': '123',
        #     'username': 'learnqa',
        #     'firstName': 'learnqa',
        #     'lastName': 'learnqa',
        #     'email': self.email
        # }

        # response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        response = MyRequests.post("/user/", data=data)


        # assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        # print(response.content)
        Assertions.asert_code_status(response, expected_status_code=200)
        Assertions.assert_json_has_key(response, "id")



    @allure.title("Test creating a user with an existing email")
    @allure.description("This test verifies that creating a user with an existing email returns an error message")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        # data = {
        #     'password': '123',
        #     'username': 'learnqa',
        #     'firstName': 'learnqa',
        #     'lastName': 'learnqa',
        #     'email': email
        # }
        # response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        response = MyRequests.post("/user/", data=data)
        
        # print(response.status_code)
        # print(response.content)

        # assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        Assertions.asert_code_status(response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected content {response.content}"



    @allure.title("Test creating a user with an invalid email")
    @allure.description("This test verifies that creating a user with an invalid email returns an error message")
    def test_create_user_with_invalid_email(self):
        email = 'invalid_email'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.asert_code_status(response, expected_status_code=400)
        assert response.content.decode("utf-8") == "Invalid email format"



    @allure.title("Test creating a user without a required field")
    @allure.description("This test verifies that creating a user without a required field returns an error message")
    @pytest.mark.parametrize("field, data", [
        ("password",
         {"username": "learnqa", "firstName": "learnqa", "lastName": "learnqa", "email": "test@example.com"}),
        ("username", {"password": "123", "firstName": "learnqa", "lastName": "learnqa", "email": "test@example.com"}),
        ("firstName", {"password": "123", "username": "learnqa", "lastName": "learnqa", "email": "test@example.com"}),
        ("lastName", {"password": "123", "username": "learnqa", "firstName": "learnqa", "email": "test@example.com"}),
        ("email", {"password": "123", "username": "learnqa", "firstName": "learnqa", "lastName": "learnqa"})
    ])
    def test_create_user_without_field(self, field, data):
        response = MyRequests.post("/user/", data=data)

        Assertions.asert_code_status(response, expected_status_code=400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {field}"



    @allure.title("Test creating a user with a short name")
    @allure.description("This test verifies that creating a user with a short name returns an error message")
    def test_create_user_with_short_name(self):
        name = 'a'
        data = {
            'password': '123',
            'username': name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }


        response = MyRequests.post("/user/", data=data)

        Assertions.asert_code_status(response, expected_status_code=400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short"


    @allure.title("Test creating a user with a long name")
    @allure.description("This test verifies that creating a user with a long name returns an error message")
    def test_create_user_with_long_name(self):
        name = 'a'*251
        data = {
            'password': '123',
            'username': name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        }


        response = MyRequests.post("/user/", data=data)

        Assertions.asert_code_status(response, expected_status_code=400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long"



