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

def convert_to_target_format(data):
    converted = data.copy()
    if 'answer' in converted and 'answer_content' in converted['answer']:
        converted['answer'] = converted['answer'].copy()
        converted['answer']['answer_content'] = [
            {**item, 
                'mid': int(item['mid']), 
                'hid': int(item['hid'])}
            for item in converted['answer']['answer_content']
        ]
    if 'checker_end' in converted:
        converted['checker_end'] = int(converted['checker_end'])
    return json.dumps(converted, indent=4)

def convert_to_target_format(data):
    converted = data.copy()
    if 'answer' in converted and 'answer_content' in converted['answer']:
        converted['answer'] = converted['answer'].copy()
        converted['answer']['answer_content'] = [
            {**item, 
                'mid': int(item['mid']), 
                'hid': int(item['hid'])}
            for item in converted['answer']['answer_content']
        ]
    if 'checker_end' in converted:
        converted['checker_end'] = int(converted['checker_end'])
    return converted

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
            with file_path_sub.open('w', encoding='utf-8') as file:
                json.dump(da_home, file, ensure_ascii=False, indent=4)
            hight_grades.append(da_home['question_score'])
            teaid.append(said)
    return hight_grades,homwerk_img,teaid

def homework_work(token, teaid, sid, taskid, hight, grades):
    checker_start = int(time.time() * 1000)
    file_path_uid = Path.cwd() / 'user.json'
    with file_path_uid.open('r', encoding='utf-8') as file:
        data_json_uid = json.load(file)
        uid = data_json_uid['user_uid']
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
    homework_work_change_url = data_json['url_change']
    change_data = {
        'request': '{{"mid": "{uid}","hid":"{hid}","student_mid":{mid},"type":1}}'.format(
            uid=str(uid), hid=str(teaid), mid=int(sid))
    }
    r_change = requests.post(url=homework_work_change_url, data=change_data, headers=headers, verify=False)
    answer = {
        "answer_content": sumbit_list,"teacher_comment": ""
    }
    checker_end = int(time.time() * 1000)
    data_sumbit = {
        'request': '{{"mid": "{mid}","hid":"{teaid}","student_mid": "{sid}","score": {score},"answer": {answer},"checker_start":"{checker_start}","checker_end" :"{checker_end}"}}'.format(
            mid=str(uid), teaid=str(teaid), sid=str(sid), score=0, answer=str(answer),checker_start=checker_start, checker_end=checker_end)
    }
    input_data_r = convert_to_target_format(data_sumbit)
    request_str = input_data_r["request"]
    fixed_request_str = request_str.replace("'", "\"")
    request_data = json.loads(fixed_request_str)
    converted_data = convert_to_target_format(request_data)
    final_output = json.dumps(converted_data, indent=4)
    final_output = str(final_output)
    input_data = {
        'request': final_output
    }
    r_homework_work = requests.post(url=homweork_informance_url, data=input_data, headers=headers, verify=False)
    directory_path = Path.cwd() / 'api' / 'fangao' / 'sumbit' 
    delete_files_in_directory(directory_path)
    da_homework_work = json.loads(r_homework_work.text)
    msg = da_homework_work['msg']
    if msg == "请求成功":
        return True
    else:
        return 0