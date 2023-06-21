import json
import requests

json_text = "https://gist.github.com/KotovVitaliy/83e4eeabdd556431374dfc70d0ba9d37"
new_json_text = f"{json_text}/raw"
response = requests.get(new_json_text)
print(response.text)
text = response.text

def remove_char(s):
    result = s[1 : -1]
    return result
#
text_2 = remove_char(text)
print(text_2)

b = json.loads(text_2)
print(b["messages"][1])