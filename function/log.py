import time
import os
def new_log():
    time_log = time.strftime('%Y-%m-%d')
    file_path = (os.getcwd() + f'\\log\\' + time_log + '_log.txt')
    with open(file_path, 'w') as file:
        file.write("time:"+time.strftime('%Y-%m-%d %H:%M:%S'))
        file.write("\n")
        file.write("welcome homework_killer")
        file.write("\n")
        file.write("open killler")
        file.write("\n")
        file.write("****************************************")
        file.write("\n")
    return (file_path)

def examine_log():
    time_log = time.strftime('%Y-%m-%d')
    file_path = (f'log/' + time_log + '_log.txt')
    if os.path.exists(file_path):
        with open(file_path, 'a') as file:
            file.write("time:"+time.strftime('%Y-%m-%d %H:%M:%S'))
            file.write("\n")
            file.write("open killler")
            file.write("\n")
            file.write("****************************************")
            file.write("\n")
        return (file_path)
    else:
        path = new_log()
        return path

def user_login_infomance_log(user_number,user_password,mid,name,msg,api):
    path = examine_log()
    with open(path, 'a',encoding='utf-8') as file:
        file.write("user_number:"+user_number)
        file.write("\n")
        file.write("user_password:"+user_password)
        file.write("\n")
        file.write("mid:"+str(mid))
        file.write("\n")
        file.write("name:"+name)
        file.write("\n")
        file.write("msg:"+str(msg))
        file.write("\n")
        file.write("api:"+str(api))
        file.write("\n")
        file.write("****************************************")
        file.write("\n")