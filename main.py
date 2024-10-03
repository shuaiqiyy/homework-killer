import os
import function.log as log
import json
import function.code as code
import function.show as show
import function.random_addon as random_addon
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
        return code,token,uid,name,user_api
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

def homework_persistent(hid,class_id):
    code,student_list_name_liat,student_list_id_list,student_list_msg_list = api.api_student_list_iformance(token,uid,hid,class_id,user_api)
    if code == 0:
        for stundent_um in student_list_id_list:
            if student_list_msg_list(stundent_um) == '':
                name = student_list_name_liat(stundent_um)
                sid = student_list_id_list(stundent_um)
                hight_grades,homwerk_img,teacherid = api.api_homework_informance(token,hid,sid,user_api)
                grades = random_addon.main(hight_grades,homwerk_img)
                api.api_homework_work(token,hid,sid,teacherid,grades,user_api)
    else:
        msg = code.main(code)
        show.msg(msg)

code,token,uid,name,user_api = login()
if code == 1:
    login_clean()
    show.msg("用户信息错误")
elif code == 5:
    login_clean()
    show.msg("插件错误")