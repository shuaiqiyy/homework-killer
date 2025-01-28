import os
import json
import requests

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)
with open(os.getcwd() + '\\api\\fangao\\fangao_api.json', 'r', encoding='utf-8') as file:
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
            with open(os.getcwd() + '\\api\\fangao\\sumbit\\{said}.json'.format(said=said), "w", encoding="utf-8") as file:
                json.dump(da_home, file, ensure_ascii=False, indent=4)
            hight_grades.append(da_home['question_score'])
            teaid.append(said)
    return hight_grades,homwerk_img,teaid

def homework_work(token, taskid, sid, teaid, hight, grades):
    score = 1
    headers = {
        'token': token
    }
    homweork_informance_url = data_json['url_homework_work']
    sumbit_list = []
    for homwerk_um in range(len(taskid)):
        work_id = taskid[homwerk_um]
        with open(os.getcwd() + '\\api\\fangao\\sumbit\\{work_id}.json'.format(work_id=work_id), 'r', encoding='utf-8') as file:
            sumbit_json = json.load(file)
        grade = grades[homwerk_um]
        sumbit_json['score'] = grade
        sumbit_list.append(sumbit_json)

    answer_content = sumbit_list
    answer = {
        "answer_content": answer_content,
        "teacher_comment": ""
    }
    data_sumbit = {
        'request': {
            "mid": sumbit_list[0]['mid'],
            "hid": taskid,
            "student_mid": sid,
            "score": score,
            "answer": answer,
            "checker_start": "1737965848228",
            "checker_end": "1737966103090"
        }
    }
    r_homework_work = requests.post(url=homweork_informance_url, data=data_sumbit, headers=headers, verify=False)
    directory_path = os.getcwd() + '\\api\\fangao\\sumbit'
    delete_files_in_directory(directory_path)

homework_work("6sCKs9MxeGyu1oJaOJjSC5bSKPMRwXq16q37nDydUzU", ['369796413', '369796414'], "81158582", "81522472", '1', ['25', '15'])