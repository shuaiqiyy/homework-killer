import os
import json
import requests

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)
with open(os.getcwd() + '/api/xiaoxin/xiaoxin_api.json', 'r', encoding='utf-8') as file:
    data_json = json.load(file)
def user_infotmance(user_number,user_password):
    user_number = int(user_number)
    url_login = data_json['url_login']
    data_login = {
        "userName": f"{user_number}",
        "userPass": f"{user_password}",
        "platform": "pc",
        "deviceNo": "Pc_Hello"
    }
    r_login = requests.post(url_login,data=data_login, verify=False)
    da_login = json.loads(r_login.text)
    msg = da_login['state']
    if msg == 'ok':
        code = 0
        token = da_login['data']['token']
        uid = da_login['data']['userId']
        name = da_login['data']['realName']
        return code,token,uid,name
    else:
        code = 1
        token = uid = name = None
        return code,token,uid,name

def class_infomace(token):
    url_class = data_json['url_class']
    url_subject = data_json['url_subject']
    class_name_list = []
    class_id_list = []
    class_subject_list = []
    data_class = {
        "token": f"{token}"
    }
    r_class = requests.post(url_class,data=data_class, verify=False)
    da_class = json.loads(r_class.text)
    msg = da_class['state']
    if msg == 'ok':
        code = 0
        class_data = da_class['data']
        for class_umb in class_data:
            class_name_list.append(class_umb['className'])
            class_id_list.append(class_umb['classId'])
            data_subject = {
                "classId": f"{class_umb['classId']}",
                "token": f"{token}"
            }
            r_subject = requests.post(url_subject,data=data_subject, verify=False)
            da_subject = json.loads(r_subject.text)
            subject = da_subject['data']
            subject = subject[0]
            class_subject_list.append(subject['sid'])
        return code,class_name_list,class_id_list,class_subject_list
    else:
        code = 2
        class_name_list = class_id_list = class_subject_list = None
        return code,class_name_list,class_id_list,class_subject_list

def homework_list_infomance(token,uid,class_id,subject_id):
    url = data_json['url_homework_list']
    homework_list_name_list = []
    homework_list_hid_list = []
    data_homework_list = {
        "classId": f"{class_id}",
        "sid": f"{subject_id}",
        "token": f"{token}"
    }
    r_homework_list = requests.post(url,data=data_homework_list, verify=False)
    da_homework_list = json.loads(r_homework_list.text)
    msg = da_homework_list['state']
    if msg == 'ok':
        code = 0
        for homework_umb in da_homework_list['data']:
            homework_list_name_list.append(homework_umb['taskName'])
            homework_list_hid_list.append(homework_umb['taskId'])
        return code,homework_list_name_list,homework_list_hid_list
    else:
        code = 3
        homework_list_name_list = homework_list_hid_list = None
        return code,homework_list_name_list,homework_list_hid_list

def student_list_iformance(token,uid,taskid,classid):
    url = data_json['url_student_list']
    student_list_name_liat = []
    student_list_id_list = []
    student_list_msg_list = []
    data_student_list = {
        "page": 1,
        "limit": 99999999,
        "taskId": f"{taskid}",
        "classId": f"{classid}",
        "token": f"{token}"
    }
    r_student_list = requests.post(url,data=data_student_list, verify=False)
    da_student_list = json.loads(r_student_list.text)
    msg = da_student_list['state']
    da_student_list = da_student_list['data']
    if msg == 'ok':
        code = 0
        for  student_umb in da_student_list['student_list']:
            student_list_name_liat.append(student_umb['realName'])
            student_list_id_list.append(student_umb['userId'])
            student_list_msg_list.append(student_umb['assessRealName'])
        return code,student_list_name_liat,student_list_id_list,student_list_msg_list
    else:
        code = 4
        student_list_name_liat = student_list_id_list = student_list_msg_list = None
        return code,student_list_name_liat,student_list_id_list,student_list_msg_list