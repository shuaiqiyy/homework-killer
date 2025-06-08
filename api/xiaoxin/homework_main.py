from pathlib import Path
import json
import requests

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)
file_path = Path.cwd() / 'api' / 'xiaoxin' / 'xiaoxin_api.json'
with file_path.open('r', encoding='utf-8') as file:
    data_json = json.load(file)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "sec-ch-ua": "Microsoft Edge",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}

def homework_informance(token,taskid,sid,user_id):
    homweork_informance_url = data_json['url_homework']
    hight_grades = []
    homwerk_img = []
    teaid = []
    data_homework = (
        'taskId={taskid}&userId={sid}&token={token}'
    ).format(taskid=taskid,sid=sid,token=token)
    r_homwork = requests.post(homweork_informance_url,data=data_homework,headers=headers, verify=False)
    da_homwork = json.loads(r_homwork.text)
    msg = da_homwork['state']
    da_homwork = da_homwork['answers']
    da_homwork = da_homwork[0]
    if msg == 'ok':
        hight_grades.append(da_homwork['teaScore'])
        homwerk_img.append(da_homwork['images'])
        teaid.append(da_homwork['teaId'])
        return hight_grades,homwerk_img,teaid
    else:
        hight_grades = homwerk_img = teaid = None
        return hight_grades,homwerk_img,teaid

def homework_work(token,taskid,sid,teaid,hight,grades):
    teaid = str(teaid[0])
    hight = str(hight[0])
    grades = str(grades[0])
    url_homework_work = data_json['url_homework_submit']
    taskscore = teaid + '-' + grades + '-' + hight
    data_homework_work = (
        'taskId={taskid}&userId={sid}&token={token}&taskScore={taskscore}'
    ).format(taskid=taskid,sid=sid,token=token,taskscore=taskscore)
    r_homework_work = requests.post(url_homework_work,data=data_homework_work,headers=headers, verify=False)
    da_homework_work = json.loads(r_homework_work.text)
    msg = da_homework_work['state']
    if msg == '提交成功':
        return 0
    else:
        return 6