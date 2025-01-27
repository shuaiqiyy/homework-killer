import flet as ft
import os
import function.log as log
import json
import function.code as api_code
import function.update as update
import api.api_choose as api

class_list = []
api_list = ["fangao","xiaoxin"]

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

#if json.loads(user_json)['code'] == 0:
#    login()

def main(page: ft.Page):
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
        def on_work_click(e, homework_name):
            print(f"开始阅卷: {homework_name}")

        tab_content = ft.Container(
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
                                    on_click=lambda e, name=homework_name: on_work_click(e, name), 
                                    disabled=False
                                    )
                            )
                        ],
                    ) for row_index, homework_name in enumerate(homework_name_list)
                ],
            ),
        )
        selected_tab.content = tab_content
        e.control.update()

    def on_rail_change(e):
        global tabs
        tabs = None 
        if e.control.selected_index == 0:
            content_column.controls = [
                ft.Text("Home"),
                ft.Image(
                    src="../logo.png",
                    width=300,
                    height=200,
                    fit=ft.ImageFit.CONTAIN
                )
            ]
        elif e.control.selected_index == 1:
            if code == 1:
                page.open(error_notuser)
            else:
                code_user_login = json.loads(user_json)['code']
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