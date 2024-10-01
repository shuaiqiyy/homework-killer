import time
import os
def new_log():
    time_log = time.strftime('%Y-%m-%d')
    file_path = (f'log/' + time_log + '_log.txt')
    with open(file_path, 'w') as file:
        file.write("time:"+time.strftime('%Y-%m-%d %H:%M:%S'))
        file.write("\n")
    return (file_path)

def examine_log():
    time_log = time.strftime('%Y-%m-%d')
    file_path = (f'log/' + time_log + '_log.txt')
    if os.path.exists(file_path):
        with open(file_path, 'a') as file:
            file.write("time:"+time.strftime('%Y-%m-%d %H:%M:%S'))
            file.write("\n")
        return (file_path)
    else:
        path = new_log()
        return path

def user_login_infomance_log(user_number,user_password,mid,name,msg):
    path = examine_log()
    with open(path, 'a') as file:
        file.write("user_number:"+user_number)
        file.write("\n")
        file.write("user_password:"+user_password)
        file.write("\n")
        file.write("mid:"+str(mid))
        file.write("\n")
        file.write("name:"+str(name))
        file.write("\n")
        file.write("msg:"+str(msg))
        file.write("\n")
        file.write("****************************************")
        file.write("\n")