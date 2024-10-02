import os
import api.fangao.fangao_api as fangao
import api.xiaoxin.xiaoxin_api as xiaoxin

def api_choose():
    path_api = os.getcwd() + "/api"
    api_liat = []
    for name in os.listdir(path_api):
        if os.path.isdir(os.path.join(path_api, name)):
            api_liat.append(name)
    return api_liat

def api_user_infotmance(user_number,user_password,api):
    if api == 'fangao':
        return fangao.user_infotmance(user_number,user_password)
    elif api == 'xiaoxin':
        return xiaoxin.user_infotmance(user_number,user_password)
    else:
        code = 5
        token = uid = name = None
        return code,token,uid,name

def api_class_infomance(token,uid,api):
    if api == 'fangao':
        return fangao.class_infomance(token,uid)
    elif api == 'xiaoxin':
        return xiaoxin.class_infomace(token)
    else:
        code = 5
        class_name_list = class_id_list = class_subject_list = None
        return code,class_name_list,class_id_list,class_subject_list

def api_homework_list_infomance(token,uid,class_id,subject_id,api):
    if api == 'fangao':
        return fangao.homework_list_infomance(token,uid,class_id,subject_id)
    elif api == 'xiaoxin':
        return xiaoxin.homework_list_infomance(token,uid,class_id,subject_id)
    else:
        code = 5
        homework_list_name_list = homework_list_hid_list = None
        return code,homework_list_name_list,homework_list_hid_list
def api_student_list_iformance(token,uid,hid,class_id,api):
    if api == 'fangao':
        return fangao.student_list_iformance(token,uid,hid,class_id)
    elif api == 'xiaoxin':
        return xiaoxin.student_list_iformance(token,uid,hid,class_id)
    else:
        code = 5
        student_list_name_liat = student_list_id_list = None
        return code,student_list_name_liat,student_list_id_list
