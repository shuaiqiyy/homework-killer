import os
import json
import requests

with open(os.getcwd() + '\\api\\fangao\\fangao_api.json', 'r', encoding='utf-8') as file:
    data_json = json.load(file)
def homework_informance(token,taskid,sid,user_id):
    hight_grades = []
    homwerk_img = []
    teaid = []
    headers = {
        'token' : token
    }
    homweork_informance_url = data_json['url_homework']
    homwerk_img = []
    data_homework = {
        'request': '{{"mid":{uid},"hid":{hid},"student_mid":{sid}}}'.format(
        uid=user_id,hid=str(taskid),sid=sid)
    }
    r_homework = requests.post(homweork_informance_url,data=data_homework,headers=headers, verify=False)
    da_homework = json.loads(r_homework.text)
    da_homework = da_homework['data']
    for da_home in da_homework['answer_content']:
        if da_home['question_type'] == 1:
            hight_grades.append(da_home['question_score'])
            teaid.append(da_home['said'])
    return hight_grades,homwerk_img,teaid

def homework_work(token,taskid,sid,teaid,hight,grades):
    teaid = str(teaid)

