import requests
import json

with open('C:\\Users\\25924\\homework-killer\\api\\xiaoxin\\xiaoxin_api.json', 'r', encoding='utf-8') as file:
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
        code = 200
        token = da_login['data']['token']
        uid = da_login['data']['userId']
        name = da_login['data']['realName']
        return code,token,uid,name
    else:
        code = 401
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
        return class_name_list,class_id_list,class_subject_list
    else:
        code = 401
        class_name_list = class_id_list = class_subject_list = None
        return class_name_list,class_id_list,class_subject_list

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
        for homework_umb in da_homework_list['data']:
            code = 200
            homework_list_name_list.append(homework_umb['taskName'])
            homework_list_hid_list.append(homework_umb['taskId'])
        return code,homework_list_name_list,homework_list_hid_list
    else:
        code = 404
        homework_list_name_list = homework_list_hid_list = None
        return code,homework_list_name_list,homework_list_hid_list




