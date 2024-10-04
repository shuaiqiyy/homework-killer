import os
from rich import print
from rich.console import Console
from rich.markdown import Markdown
console = Console()

import subprocess

def clear_screen():
    if os.name == 'nt':
        subprocess.run(['cls'], shell=True)
    else:
        subprocess.run(['clear'], shell=True)

def index():
    clear_screen()
    with open("./cui/index.md",encoding='utf-8') as readme:
        markdown = Markdown(readme.read())
    console.print(markdown)

def login(api_list):
    for m in range(len(api_list) - 1):
        print(f'{m+1}.{api_list[m]}')
    user_number = input('请输入手机号：')
    user_password = input('请输入密码：')
    user_api = input('请输入api：')
    return user_number,user_password,user_api

def msg(in_msg):
    print(in_msg)

def class_show(class_list):
    clear_screen()
    for i in range(len(class_list)):
        print(f'{i+1}.{class_list[i]}')
    id = input('请输入班级序号：')
    if id.isdigit() and int(id) <= len(class_list):
        return int(id) - 1
    else:
        clear_screen()
        msg('输入有误，请重新输入')
        return class_show(class_list)