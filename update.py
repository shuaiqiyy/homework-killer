import requests
import json

url = "https://api.github.com/repos///releases/latest"
data = {
    "owner": "shuaiqiyy",
    "repo" : "https://github.com/shuaiqiyy/homework-killer.git"
}
r = requests.get(url,data=data,verify=False)
print(r)