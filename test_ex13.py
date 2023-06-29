import requests
import pytest

@pytest.mark.parametrize("user_agent, expected_device, expected_browser, expected_platform", [
    # Перечисляйте здесь значения User Agent и ожидаемых результатов
    ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
     "Android", "No", "Mobile"),
    ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
     "iOS", "Chrome", "Mobile"),
    ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
     "Unknown", "Unknown", "Googlebot"),
    ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
     "No", "Chrome", "Web"),
    ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
     "iPhone", "No", "Mobile")
])
def test_user_agent_check(user_agent, expected_device, expected_browser, expected_platform):
    headers = {"User-Agent": user_agent}
    response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check", headers=headers)
    response_data = response.json()

    assert response_data["device"] == expected_device, f"Неправильное значение для device. User Agent: {user_agent}"
    assert response_data["browser"] == expected_browser, f"Неправильное значение для browser. User Agent: {user_agent}"
    assert response_data["platform"] == expected_platform, f"Неправильное значение для platform. User Agent: {user_agent}"

