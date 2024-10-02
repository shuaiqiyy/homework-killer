import os
import fangao.fangao_api
import xiaoxin.xiaoxin_api

def api_choose():
    path_api = os.getcwd() + "/api"
    api_liat = []
    for name in os.listdir(path_api):
        if os.path.isdir(os.path.join(path_api, name)):
            api_liat.append(name)
    return api_liat

def api_user_infotmance(user_number,user_password,api):
    if api == 'fangao':
        return fangao.fangao_api.user_infotmance(user_number,user_password)
    elif api == 'xiaoxin':
        return xiaoxin.xiaoxin_api.user_infotmance(user_number,user_password)
    else:
        return False

def api_class_infomance(token,uid,api):
    if api == 'fangao':
        return fangao.fangao_api.class_infomance(token,uid)
    elif api == 'xiaoxin':
        return xiaoxin.xiaoxin_api.class_infomace(token)
    else:
        return False

def api_homework_list_infomance(token,uid,class_id,subject_id,api):
    if api == 'fangao':
        return fangao.fangao_api.homework_list_infomance(token,uid,class_id,subject_id)
    elif api == 'xiaoxin':
        return xiaoxin.xiaoxin_api.homework_list_infomance(token,uid,class_id,subject_id)
    else:
        return False

def api_student_list_iformance(token,uid,hid,class_id,api):
    if api == 'fangao':
        return fangao.fangao_api.student_list_iformance(token,uid,hid,class_id)
    elif api == 'xiaoxin':
        return xiaoxin.xiaoxin_api.student_list_iformance(token,uid,hid,class_id)
    else:
        return False
