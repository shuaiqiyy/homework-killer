import os
import json
import requests

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)
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
            said = da_home['said']
            with open(os.getcwd() + '\\api\\fangao\\sumbit\\{said}.json'.format(said=said), "w", encoding="utf-8") as file:
                json.dump(da_home, file, ensure_ascii=False, indent=4)
            hight_grades.append(da_home['question_score'])
            teaid.append(said)
    return hight_grades,homwerk_img,teaid

def homework_work(token,taskid,sid,teaid,hight,grades):
    teaid = str(teaid)
    sumbit_list = []
    headers = {
        'token' : token
    }
    homweork_informance_url = data_json['url_homework_work']
    for homwerk_um in range(len(taskid)):
        work_id = taskid[homwerk_um]
        with open(os.getcwd() + '\\api\\fangao\\sumbit\\{work_id}.json'.format(work_id=work_id), 'r', encoding='utf-8') as file:
            sumbit_json = json.load(file)
        grade = grades[homwerk_um]
        sumbit_json['score'] = grade
        sumbit_list.append(sumbit_json)
        data_sumbit_first = {} 
    for sumbit_um in range(len(sumbit_list)):
        data_sumbit_first = data_sumbit_first + sumbit_list[sumbit_um]
    print(data_sumbit_first)
    data_sumbit_homework ={
        "answer_content":[
            {}
        ]
    }
    data_sumbit = {
        'request': 
            '{{"mid":{uid},"hid":{hid},"student_mid":{sid},"score":{score},"answer":{answer}}}'.format(hid=str(taskid),sid=sid)
    }

##homework_work("6sCKs9MxeGyu1oJaOJjSC5bSKPMRwXq16q37nDydUzU",['369796413','369796414'],"81158582","81522472",'1',['25','15'])
