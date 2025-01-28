import os
import json
import flet as ft
import function.log as log
import api.api_choose as api
import function.update as update
import function.code as api_code
import function.random_addon as random_addon

class_list = []
api_list = api.api_choose()

md_index = """
# Homework  Killer
![](./logo.png)
## Maker : shuaiqiyy
## GitHub : https://github.com/shuaiqiyy/Homework-Killer
###   ⭐⭐⭐希望大家多多支持开发者⭐⭐⭐
### ⭐⭐⭐希望大家可以多多为我点star⭐⭐⭐
``` 此产品为爱发电，所有收费均是骗子！！！ ```
> 版本 v1.0.0
> 检查更新请前往GitHub页
"""

with open('user.json', 'r', encoding='utf-8') as file:
        user_json = file.read()
        code = json.loads(user_json)['code']

def login():
    user_number = json.loads(user_json)['user_number']
    user_password = json.loads(user_json)['user_password']
    user_api = json.loads(user_json)['api']
    code,token,uid,name = api.api_user_infotmance(user_number,user_password,user_api)
    log.user_login_infomance_log(user_number,user_password,uid,name,code,user_api)
    user_data = {
            'code': 0,
            'user_number': user_number,
            'user_password': user_password,
            'api': user_api,
            'user_name': name,
            'user_token': token,
            'user_uid': uid,
        }
    with open("user.json", "w", encoding="utf-8") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)

def woker_main(hid,class_id,grades_less):
    token = json.loads(user_json)['user_token']
    uid = json.loads(user_json)['user_uid']
    user_api = json.loads(user_json)['api']
    grades = []
    code,student_list_name_list,student_list_id_list,student_list_msg_list = api.api_student_list_iformance(token,uid,hid,class_id,user_api)
    if code == 0:
        for stundent_um in range(len(student_list_id_list)):
            if student_list_msg_list[stundent_um] == '待批改':
                sid = student_list_id_list[stundent_um]
                hight_grades,homwerk_img,teacherid = api.api_homework_informance(token,hid,sid,user_api)
                for qu_um in range(len(hight_grades)):
                    grades_h = hight_grades[qu_um]
                    teac_id = teacherid[qu_um]
                    grade = random_addon.main(grades_h,grades_less,homwerk_img)
                    grades.append(grade)
                api.api_homework_work(token,hid,sid,teac_id,hight_grades,grades,user_api)


class Page:
    def __init__(self, ft_page):
        self.ft_page = ft_page
        self.student_list_name_list = []
        self.student_list_msg_list = []

global_custom_page = None
def main(page: ft.Page):
    global global_custom_page
    global_custom_page = Page(page)

    page.title = "Homework Killer"

    def error_notuser_close(e):
        page.close(error_notuser),
    def error_notnet_close(e):
        page.close(error_notnet),
    
    error_notuser = ft.AlertDialog(
        modal=True,
        title=ft.Text("警告"),
        content=ft.Text("请先进行账号认证！！！"),
        actions=[
            ft.TextButton("好的", on_click=error_notuser_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    error_notnet = ft.AlertDialog(
        modal=True,
        title=ft.Text("警告"),
        content=ft.Text("请检查你的网络！！！"),
        actions=[
            ft.TextButton("好的", on_click=error_notnet_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def user_login(e):
        page.close(user_add_page),
        user_number = phone_field.value
        user_password = password_field.value
        user_api = api_dropdown.value
        user_data = {
            'code': 0,
            'user_number': user_number,
            'user_password': user_password,
            'api': user_api,
        }
        with open("user.json", "w", encoding="utf-8") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)
        login()

    def login_clean(e):
        user_data = {
            'code': 1,
        }
        with open("user.json", "w", encoding="utf-8") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)
        page.open(user_add_page)

    def user_add(e):
        page.open(user_add_page)
    phone_field = ft.TextField(label="手机号")
    password_field = ft.TextField(
        label="密码", 
        password=True, 
        can_reveal_password=True
    )
    api_dropdown = ft.Dropdown(
        width=100,
        options=[
            ft.dropdown.Option(text=user_api) for user_api in api_list
        ],
    )
    user_add_page = ft.AlertDialog(
        modal=True,
        title=ft.Text("用户认证"),
        content=ft.Column([
            phone_field,
            password_field,
            api_dropdown,
        ]),
        actions=[
            ft.TextButton("完成",on_click=user_login),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        )

    def on_class_change(e):
        token = json.loads(user_json)['user_token']
        uid = json.loads(user_json)['user_uid']
        user_api = json.loads(user_json)['api']
        code_class, class_list, class_id_list, class_subject_list = api.api_class_infomance(token, uid, user_api)
        selected_index = int(e.data)
        class_um = selected_index
        class_id = class_id_list[class_um]
        subject_id = class_subject_list[class_um]
        code,homework_name_list, homework_id_list = api.api_homework_list_infomance(token, uid, class_id, subject_id, user_api)
        selected_tab_index = e.control.selected_index
        selected_tab = e.control.tabs[selected_tab_index]
        def on_work_click(e, home_um):
            token = json.loads(user_json)['user_token']
            uid = json.loads(user_json)['user_uid']
            user_api = json.loads(user_json)['api']
            code, homework_name_list, homework_id_list = api.api_homework_list_infomance(token, uid, class_id, subject_id, user_api)
            homework_id = homework_id_list[home_um]
            code, student_list_name_list, student_list_id_list, student_list_msg_list = api.api_student_list_iformance(token, uid, homework_id, class_id, user_api)
            global_custom_page.student_list_name_list = student_list_name_list
            global_custom_page.student_list_msg_list = student_list_msg_list
            grades_less_slider = ft.Slider(min=0, max=10, divisions=10, label="{value}")
            work_page = ft.AlertDialog(
                modal=True,
                title=ft.Text("学生列表"),
                content=ft.Column(
                    [
                        ft.Column(
                            [
                                ft.FilledButton("开始", on_click=lambda e: woker_main(homework_id, class_id, grades_less_slider.value)),
                                ft.Text("分差："),
                                grades_less_slider,
                            ]
                        ),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("学生姓名")),
                                ft.DataColumn(ft.Text("状态"))
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text(student_name)),
                                        ft.DataCell(ft.Text(student_msg)),
                                    ],
                                ) for student_name, student_msg in zip(global_custom_page.student_list_name_list,
                                                                        global_custom_page.student_list_msg_list)
                            ]
                        ),
                    ]
                ),
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(work_page)
            page.update()


        tab_content = ft.Container(
            ft.Column(
                [
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("作业标题")),
                            ft.DataColumn(ft.Text("一键阅卷"))
                        ],
                        rows=[
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(homework_name)),
                                    ft.DataCell(
                                        ft.FilledButton(
                                            "一键阅卷", 
                                            on_click=lambda e, home_um=home_um: on_work_click(e, home_um), 
                                            )
                                    )
                                ],
                            ) for home_um, homework_name in enumerate(homework_name_list)
                        ],
                    ),
                ]
            )
        )
        selected_tab.content = tab_content
        e.control.update()

    def on_rail_change(e):
        global tabs
        tabs = None 
        if e.control.selected_index == 0:
            content_column.controls = [
                ft.Markdown(
                    md_index,
                    selectable=True,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    on_tap_link=lambda e: page.launch_url(e.data),
                )
            ]
        elif e.control.selected_index == 1:
            if code == 1:
                page.open(error_notuser)
            else:
                token = json.loads(user_json)['user_token']
                uid = json.loads(user_json)['user_uid']
                name = json.loads(user_json)['user_name']
                user_api = json.loads(user_json)['api']
                code_class,class_list,class_id_list,class_subject_list = api.api_class_infomance(token,uid,user_api)
                tabs = ft.Tabs(
                    selected_index=1,
                    animation_duration=300,
                    tabs=[
                        ft.Tab(
                            text=class_name,
                            content=ft.Container()
                        ) for class_name in class_list
                    ],
                    on_change=on_class_change
                )
                content_column.controls = [tabs] if tabs else []
        elif e.control.selected_index == 2:
            if code == 0:
                code_user_login = json.loads(user_json)['code']
                token = json.loads(user_json)['user_token']
                uid = json.loads(user_json)['user_uid']
                name = json.loads(user_json)['user_name']
                user_api = json.loads(user_json)['api']
                page_login = [
                    ft.Text("账号认证"),
                    ft.Text(name),
                    ft.FilledButton("清除信息",on_click=login_clean)
                ]
            else:
                page_login = [
                    ft.Text("账号认证"),
                    ft.FilledButton("添加用户信息", icon="add",on_click=user_add),
                ]
            content_column.controls = page_login
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        expand=False, 
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.HOME_OUTLINED, selected_icon=ft.icons.HOME_SHARP, label="主页"
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                label="班级",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("设置"),
            ),
        ],
        on_change=on_rail_change,
    )
    content_column = ft.Column(expand=True)
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                content_column
            ],
            expand=True,
        )
    )
ft.app(target=main)