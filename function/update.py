import requests
import json
import os

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)
with open(os.getcwd() + '\\maker.json', 'r', encoding='utf-8') as file:
    data_json = json.load(file)
version = data_json['version']

def main():
    url = "https://api.github.com/repos/shuaiqiyy/homework-killer/releases/latest"
    r = requests.get(url)
    json_data = json.loads(r.text)
    if json_data['message'] == "Not Found":
        msg = "无法连接github服务器"
        return msg
    elif json_data['tag_name'] == version:
        msg = "当前版本为最新版本"
        return msg
    else:
        msg = "发现新版本" + json_data['tag_name']
        return msg