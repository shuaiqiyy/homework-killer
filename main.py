import flet as ft
#import homework
import json

class_list = []

with open('user.json', 'r', encoding='utf-8') as file:
        user_json = file.read()
        code = json.loads(user_json)['code']

def main(page: ft.Page):
    def handle_close(e):
        page.close(dlg_modal)
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("警告"),
        content=ft.Text("请先进行账号认证！！！"),
        actions=[
            ft.TextButton("好的", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def on_rail_change(e):
        if e.control.selected_index == 0:
            content_column.controls = [
                ft.Text("Home"),
            ]
        elif e.control.selected_index == 1:
            if class_list == []:
                page.open(dlg_modal)
            tabs = ft.Tabs(
                selected_index=1,
                animation_duration=300,
                tabs=[
                    ft.Tab(
                        text=class_name,
                        content=ft.Container()
                    ) for class_name in class_list
                ],
                on_change=on_tab_change
            )
            content_column.controls = [tabs]
        elif e.control.selected_index == 2:
            if code == 0:
                #name = homework.login()
                page_login = [
                    ft.Text("账号认证"),
                    ft.Text(0),
                ]
            else:
                page_login = [
                    ft.Text("账号认证"),
                    ft.FilledButton("添加用户信息", icon="add"),
                ]
            content_column.controls = page_login
        page.update()
    
    def on_tab_change(e):
        selected_index = int(e.data)
        class_id = selected_index
        print(class_id)

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