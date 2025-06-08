import os
from pathlib import Path
import json
import time
import requests

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)
file_path = Path.cwd() / 'api' / 'fangao' / 'fangao_api.json'
with file_path.open('r', encoding='utf-8') as file:
    data_json = json.load(file)

def delete_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

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
            file_path_sub = Path.cwd() / 'api' / 'fangao' / 'sumbit' / '{said}.json'.format(said=said)
            with file_path_sub.open('r', encoding='utf-8') as file:
                json.dump(da_home, file, ensure_ascii=False, indent=4)
            hight_grades.append(da_home['question_score'])
            teaid.append(said)
    return hight_grades,homwerk_img,teaid

def homework_work(token, teaid, sid, taskid, hight, grades):
    checker_start = int(time.time())
    headers = {
        'token': token
    }
    homweork_informance_url = data_json['url_homework_work']
    sumbit_list = []
    for homwerk_um in range(len(taskid)):
        work_id = taskid[homwerk_um]
        file_path_sub = Path.cwd() / 'api' / 'fangao' / 'sumbit' / '{said}.json'.format(said=work_id)
        with file_path_sub.open('r', encoding='utf-8') as file:
            sumbit_json = json.load(file)
        grade = grades[homwerk_um]
        sumbit_json['score'] = str(grade)
        sumbit_list.append(sumbit_json)
    score = max(grades)
    answer = {
        "answer_content": sumbit_list,"teacher_comment": ""
    }
    checker_end = int(time.time())
    data_sumbit = {
        'request': '{{"mid": "{mid}","hid":"{teaid}","student_mid": "{sid}","score": {score},"answer": {answer},"checker_start":"{checker_start}","checker_end" :"{checker_end}"}}'.format(mid=str(sumbit_list[0]['mid']), teaid=str(teaid), sid=str(sid), score=score, answer=answer,checker_start=checker_start, checker_end=checker_end)
    }
    r_homework_work = requests.post(url=homweork_informance_url, data=data_sumbit, headers=headers, verify=False)
    print(r_homework_work.text)
    directory_path = Path.cwd() / 'api' / 'fangao' / 'sumbit' 
    delete_files_in_directory(directory_path)