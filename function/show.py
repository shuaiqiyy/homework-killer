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
    with open("cui/index.md",encoding='utf-8') as readme:
        markdown = Markdown(readme.read())
    console.print(markdown)

def login(api_list):
    print(api_list)
    user_number = input('请输入学号：')
    user_password = input('请输入密码：')
    user_api = input('请输入api：')
    return user_number,user_password,user_api

def msg(in_msg):
    print(in_msg)
    
index()