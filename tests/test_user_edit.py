import requests
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
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

    def test_edit_user_unauthorized(self):
        # EDIT
        response = MyRequests.put(
            "/user/1",
            data={"firstName": "Changed Name"}
        )

        Assertions.asert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Auth token not supplied"


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






