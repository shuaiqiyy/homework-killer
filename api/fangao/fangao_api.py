import json
import requests

with open('C:\\Users\\25924\\homework-killer\\api\\fangao\\fangao_api.json', 'r', encoding='utf-8') as file:
    data_json = json.load(file)

def token_hear(token):
    hear = {
            'token': token
        }
    return hear

def user_infotmance(user_number,user_password):
    user_number = int(user_number)
    user_password = int(user_password)
    url_login = data_json['url_login']
    data_login = {
        'request': '{{"mobile":"{user_number}","password":"{user_password}"}}'.format(
            user_number=user_number,
            user_password=user_password
        )
    }
    r_login = requests.post(url_login,data=data_login, verify=False)
    da_lodin = json.loads(r_login.text)
    code = da_lodin['code']
    if code == 0:
        code = 200
        token = da_lodin['data']['token']
        uid = da_lodin['data']['mid']
        name = da_lodin['data']['username']
        return code,token,uid,name
    else:
        code = 401
        token = mid = name = None
        return code,token,mid,name

def class_infomance(token,uid):
    hear = token_hear(token)
    url_class = data_json['url_class']
    class_name_list = []
    class_id_list = []
    class_subject_list = []
    data_class = {
        'request': '{{"mid":"{mid}"}}'.format(
            mid=uid
        )
    }
    r_class = requests.post(url_class,data=data_class, headers=hear, verify=False)
    da_class = json.loads(r_class.text)
    code = da_class['code']
    if code == 0:
        class_data = da_class['data']
        for class_umb in class_data:
            class_name_list.append(f"{class_umb['class_name']},{class_umb['subject_name']}")
            class_id_list.append(class_umb['class_id'])
            class_subject_list.append(class_umb['subject_id'])
        return code,class_name_list,class_id_list,class_subject_list
    else:
        code = 401
        class_name_list = class_id_list = class_subject_list = None
        return code,class_name_list,class_id_list

def homework_list_infomance(token,uid,class_id,subject_id):
    hear = token_hear(token)
    url_homework_list = data_json['url_homework_list']
    homework_list_name_list = []
    homework_list_hid_list = []
    data_homework_list = {
        'request': '{{"mid":{mid},"subject_id":{subjectid},"class_id":{classid},"page":1,"pageSize":10}}'.format(
            mid=uid,classid=class_id,subjectid=subject_id
            )
    }
    r_homework_list = requests.post(url_homework_list,data=data_homework_list, headers=hear, verify=False)
    da_homework_list = json.loads(r_homework_list.text)
    code = da_homework_list['code']
    if code == 0:
        for homework_umb in da_homework_list['data']:
            homework_list_name_list.append(homework_umb['homework_title'])
            homework_list_hid_list.append(homework_umb['hid'])
        return code,homework_list_name_list,homework_list_hid_list
    else:
        code = 404
        homework_list_name_list = homework_list_hid_list = None
        return code,homework_list_name_list,homework_list_hid_list
