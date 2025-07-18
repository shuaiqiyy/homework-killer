import os
from pathlib import Path
import api.fangao.fangao_api as fangao
import api.xiaoxin.xiaoxin_api as xiaoxin
import api.fangao.homework_main as homework_fangao
import api.xiaoxin.homework_main as homework_xiaoxin

def student_list(student_list_name_liat,student_list_id_list,student_list_msg_list):
    names = []
    ids = []
    msgs_ = []
    for name, sid,msgs in zip(student_list_name_liat,student_list_id_list,student_list_msg_list):
        if msgs == "待批改":
            names.append(name)
            ids.append(sid)
            msgs_.append(msgs)
    return names,ids,msgs_

def api_choose():
    path_api = Path.cwd() / 'api'
    api_list = []
    for name in os.listdir(path_api):
        if os.path.isdir(os.path.join(path_api, name)):
            api_list.append(name)
    return api_list

def api_user_informance(user_number, user_password, api):
    if api == 'fangao':
        return fangao.user_informance(user_number, user_password)
    elif api == 'xiaoxin':
        return xiaoxin.user_infotmance(user_number, user_password)
    else:
        code = 5
        token = uid = name = None
        return code, token, uid, name

def api_class_informance(token, uid, api):
    if api == 'fangao':
        return fangao.class_infomance(token, uid)
    elif api == 'xiaoxin':
        return xiaoxin.class_infomace(token)
    else:
        code = 5
        class_name_list = class_id_list = class_subject_list = None
        return code, class_name_list, class_id_list, class_subject_list

def api_homework_list_informance(token, uid, class_id, subject_id, api):
    if api == 'fangao':
        return fangao.homework_list_infomance(token, uid, class_id, subject_id)
    elif api == 'xiaoxin':
        return xiaoxin.homework_list_infomance(token, uid, class_id, subject_id)
    else:
        code = 5
        homework_list_name_list = homework_list_hid_list = None
        return code, homework_list_name_list, homework_list_hid_list

def api_student_list_iformance(token, uid, hid, class_id, api):
    if api == 'fangao':
        code,student_list_name_liat,student_list_id_list,student_list_msg_list = fangao.student_list_iformance(token, uid, hid, class_id)
        name_list,id_list,msg_list = student_list(student_list_name_liat,student_list_id_list,student_list_msg_list)
        return code,name_list,id_list,msg_list
    elif api == 'xiaoxin':
        code,student_list_name_liat,student_list_id_list,student_list_msg_list = xiaoxin.student_list_iformance(token, uid, hid, class_id)
        name_list,id_list,msg_list = student_list(student_list_name_liat,student_list_id_list,student_list_msg_list)
        return code,name_list,id_list,msg_list
    else:
        code = 5
        student_list_name_list = student_list_id_list = None
        return code, student_list_name_list, student_list_id_list

def api_homework_informance(token, taskid, sid, uid, api):
    if api == 'fangao':
        return homework_fangao.homework_informance(token, taskid, sid, uid)
    elif api == 'xiaoxin':
        return homework_xiaoxin.homework_informance(token, taskid, sid, uid)
    else:
        code = 5
        hight_grades = homework_img = teaid = None
        return code, hight_grades, homework_img, teaid

def api_homework_work(token, taskid, sid, teaid, hight, grades, api):
    if api == 'fangao':
        return homework_fangao.homework_work(token, taskid, sid, teaid, hight, grades)
    elif api == 'xiaoxin':
        return homework_xiaoxin.homework_work(token, taskid, sid, teaid, hight, grades)
    else:
        code = 5
        return code