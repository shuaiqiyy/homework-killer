import os
import json
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)
with open(os.getcwd() + '/api/xiaoxin/xiaoxin_api.json', 'r', encoding='utf-8') as file:
    data_json = json.load(file)

def homweork_informance(token,taskid,sid):
    homweork_informance_url = data_json['homweork_informance_url']
    homwerk_img = []
    data_homwork = {
        "taskld": f"{taskid}",
        "userId": f"{sid}",
        "token": f"{token}"
    }
    r_homwork = requests.post(homweork_informance_url, data=data_homwork, verify=False)
    da_homwork = json.loads(r_homwork.text)
    msg = da_homwork['state']
    da_homwork = da_homwork['data']
    if msg == 'ok':
        hight_grades = da_homwork['teaScore']
        howork_img_html = da_homwork['teaResolve']
        howork_img_html = BeautifulSoup(howork_img_html, 'html.parser')
        homwerk_img_img = howork_img_html.find_all('img')
        for img in homwerk_img_img:
            homwerk_img.append(img['src'])
        return hight_grades, homwerk_img
    else:
        hight_grades = homwerk_img = None
        return hight_grades, homwerk_img