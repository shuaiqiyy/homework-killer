import os
import function.log as log
import json
import function.code as api_code
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

def class_main():
    code,class_name_list,class_id_list,class_subject_list = api.api_class_infomance(token,uid,user_api)
    if code ==0:
        class_um = show.class_show(class_name_list)
        class_id = class_id_list[class_um]
        class_subject = class_subject_list[class_um]
        return class_id,class_subject
    else:
        msg = api_code.main(code)
        show.msg(msg)
        return class_main()

def homework_main(class_id,subject_id):
    code,homework_list_name_list,homework_list_hid_list = api.api_homework_list_infomance(token,uid,class_id,subject_id,user_api)
    if code == 0:
        homework_um = show.class_show(homework_list_name_list)
        hid = homework_list_hid_list[homework_um]
        return hid
    else:
        msg = api_code.main(code)
        show.msg(msg)
        return homework_main(class_id,subject_id)

def homework_persistent(hid,class_id):
    code,student_list_name_liat,student_list_id_list,student_list_msg_list = api.api_student_list_iformance(token,uid,hid,class_id,user_api)
    print(student_list_msg_list)
    low_grades = int(input("请输入最低分："))
    if code == 0:
        for stundent_um in range(len(student_list_id_list)):
            if student_list_msg_list[stundent_um] == '待批改':
                name = student_list_name_liat[stundent_um]
                show.msg(name)
                sid = student_list_id_list[stundent_um]
                hight_grades,homwerk_img,teacherid = api.api_homework_informance(token,hid,sid,user_api)
                grades = random_addon.main(hight_grades,low_grades,homwerk_img)
                show.msg(grades)
                api.api_homework_work(token,hid,sid,teacherid,hight_grades,grades,user_api)


show.index()
code,token,uid,name,user_api = login()
if code == 0:
    show.msg("欢迎使用")
    class_id,class_subject = class_main()
    homework_id = homework_main(class_id,class_subject)
    homework_persistent(homework_id,class_id)
elif code == 1:
    login_clean()
    show.msg("用户信息错误")
elif code == 5:
    login_clean()
    show.msg("插件错误")