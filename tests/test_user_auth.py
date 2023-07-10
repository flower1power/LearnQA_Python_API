import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]
    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_headers(response1, "x-csrf-token")
        self.user_id_from_auth_metod = self.get_json_value(response1, "user_id")

        # assert "auth_sid" in response1.cookies, "There is no auth xookie in the response"
        # assert "x-csrf-token" in response1.headers, "There is not CSRF token header in the response"
        # assert "user_id" in response1.json(), "There is no user id in the response"
        # self.auth_sid = response1.cookies.get("auth_sid")
        # self.token = response1.headers.get("x-csrf-token")
        # self.user_id_from_auth_metod = response1.json()["user_id"]

    @allure.description("This test successfuly authorization user by email and password")
    def test_auth_user(self):


        # response2 = requests.get(
        #     "https://playground.learnqa.ru/api/user/auth",
        #     headers={"x-csrf-token": self.token},
        #     cookies={"auth_sid": self.auth_sid}
        # )

        response2 = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_metod,
            "User id from auth metod is not equal to user id from check metohod"
        )
        # assert "user_id" in response2.json(), "There is no user id in the second response"
        # user_id_from_check_metod = response2.json()["user_id"]
        # assert  self.user_id_from_auth_metod == user_id_from_check_metod, "User id from auth metod is not equal to user id check metod"

    @allure.description("This test checks authorizations status w/o sending auth cookie or token")
    @pytest.mark.parametrize("condition", exclude_params)
    @allure.issue("YOUR_ISSUE_TRACKER_LINK")
    @allure.tag("negative_case")
    def test_nagative_auth_check(self, condition):

        # if condition == "no_cookie":
        #     response2 = requests.get(
        #         "https://playground.learnqa.ru/api/user/auth",
        #         headers={"x-csrf-token": self.token},
        #     )
        # else:
        #     response2 = requests.get(
        #         "https://playground.learnqa.ru/api/user/auth",
        #         cookies={"auth_sid": self.auth_sid}
        #     )

        if condition == "no_cookie":
            response2 = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token},
            )
        else:
            response2 = MyRequests.get(
                "/user/auth",
                cookies={"auth_sid": self.auth_sid}
            )


        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )

        # assert "user_id" in response2.json(), "There is no user id in the second response"
        # user_id_from_check_metod = response2.json()["user_id"]
        # assert user_id_from_check_metod == 0, f"User is authorized with condition {condition}"