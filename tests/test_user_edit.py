import allure
import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("User Edit")
class TestUserEdit(BaseCase):
    @allure.story("Edit Just Created User")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("user_edit")
    @allure.title("Test Editing Just Created User")
    @allure.description("This test verifies that a just created user can be edited successfully")
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        # response1 = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.asert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #LOGIN

        login_data = {
            'email': email,
            'password': password
        }

        # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")


        #EDIT

        new_name = "Changed Name"

        # response3 = requests.put(
        #     f"https://playground.learnqa.ru/api/user/{user_id}",
        #     headers={"x-csrf-token": token},
        #     cookies={"auth_sid": auth_sid},
        #     data={"firstName": new_name}
        # )

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.asert_code_status(response3, 200)

        #GET

        # response4 = requests.get(
        #     f"https://playground.learnqa.ru/api/user/{user_id}",
        #     headers={"x-csrf-token": token},
        #     cookies={"auth_sid": auth_sid}
        # )
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.asert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.story("Edit User While Unauthorized")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("user_edit")
    @allure.title("Test Editing User While Unauthorized")
    @allure.description("This test verifies that editing a user while unauthorized returns an error message")
    def test_edit_user_unauthorized(self):
        # EDIT
        response = MyRequests.put(
            "/user/1",
            data={"firstName": "Changed Name"}
        )

        Assertions.asert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied"

    @allure.story("Edit User While Authorized as Another User")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("user_edit")
    @allure.title("Test Editing User While Authorized as Another User")
    @allure.description(
        "This test verifies that editing a user while authorized as another user returns an error message")
    def test_edit_user_authorized_as_another_user(self):
        # REGISTER user1
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        user_id1 = self.get_json_value(response1, "id")

        # REGISTER user2
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)
        user_id2 = self.get_json_value(response2, "id")

        # LOGIN as user1
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response3 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_headers(response3, "x-csrf-token")

        # EDIT user2 as user1
        response4 = MyRequests.put(
            f"/user/{user_id2}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "New Name"}
        )

        Assertions.asert_code_status(response4, 400)
        assert response4.content.decode("utf-8") == "Error updating user"

    @allure.story("Edit User with Invalid Email")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("user_edit")
    @allure.title("Test Editing User with Invalid Email")
    @allure.description("This test verifies that editing a user with an invalid email returns an error message")
    def test_edit_user_invalid_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        # EDIT with invalid email
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": "invalid_email"}
        )

        Assertions.asert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == "Invalid email format"

    @allure.story("Edit User with Short firstName")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("user_edit")
    @allure.title("Test Editing User with Short firstName")
    @allure.description("This test verifies that editing a user with a short firstName returns an error message")
    def test_edit_user_short_firstName(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_headers(response2, "x-csrf-token")

        # EDIT with short firstName
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": "A"}
        )

        Assertions.asert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == '{"error":"Too short value for field firstName"}'