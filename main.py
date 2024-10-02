import os
import function.log as log
import json
import function.show as show
import function.update as update
import api.api_choose as api

api_list = api.api_choose()
log.examine_log()

def have_user_api():
    with open('user.json', 'r', encoding='utf-8') as file:
        user_json = file.read()
        user_api = json.loads(user_json)['api']
        return user_api

def login():
    with open('user.json', 'r', encoding='utf-8') as file:
        user_json = file.read()
        code = json.loads(user_json)['code']
    if code == 0:
        user_number = json.loads(user_json)['user_number']
        user_password = json.loads(user_json)['user_password']
        user_api = json.loads(user_json)['api']
        code,token,uid,name = api.api_user_infotmance(user_number,user_password,user_api)
        log.user_login_infomance_log(user_number,user_password,uid,name,code,user_api)
        return code,token,uid,name
    else:
        user_number,user_password,user_api = show.login(api_list)
        user_data = {
            'code': 0,
            'user_number': user_number,
            'user_password': user_password,
            'api': user_api,
        }
        with open("user.json", "w", encoding="utf-8") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)
        return login()

def login_clean():
    user_data = {
        'code': '',
        'user_number': '',
        'user_password': '',
        'api': '',
    }
    with open("user.json", "w", encoding="utf-8") as file:
        json.dump(user_data, file, ensure_ascii=False, indent=4)
    return login()

def class_list():
    user_api = have_user_api()
    code,class_name_list,class_id_list,class_subject_list = api.api_class_infomance(token,uid,user_api)
    return code,class_name_list,class_id_list,class_subject_list


code,token,uid,name = login()
if code == 1:
    login_clean()
    show.msg("用户信息错误")
elif code == 5:
    login_clean()
    show.msg("插件错误")