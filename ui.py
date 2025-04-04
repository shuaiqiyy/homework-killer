import flet as ft
from core import UserManager, HomeworkManager
from api.api_choose import api_choose
api_list = api_choose()

class HomeworkKillerUI:
    def __init__(self, page: ft.Page, user_manager: UserManager, homework_manager: HomeworkManager):
        self.page = page
        self.user = user_manager
        self.homework = homework_manager
        self.current_class_id = None
        self.current_subject_id = None
        self.current_homework_id = None
        self._setup_ui()

    def _setup_ui(self):
        """初始化主界面布局"""
        self.page.title = "Homework Killer"
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # 导航栏配置
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            expand=False,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME_SHARP,
                    label="主页"
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="班级"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label="设置"
                ),
            ],
            on_change=self._on_rail_change
        )

        # 主内容区域
        self.content_column = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)
        
        # 页面布局
        self.page.add(
            ft.Row(
                [
                    self.rail,
                    ft.VerticalDivider(width=1),
                    self.content_column
                ],
                expand=True,
            )
        )

    def _on_rail_change(self, e):
        """导航栏切换事件"""
        self.content_column.controls.clear()
        
        if self.rail.selected_index == 0:
            self._show_home_page()
        elif self.rail.selected_index == 1:
            self._show_classes_page()
        elif self.rail.selected_index == 2:
            self._show_settings_page()
        
        self.page.update()

    def _show_home_page(self):
        """显示主页"""
        md_content = ft.Markdown(
            """
            # Homework Killer
            ![](./logo.png)
            ## Maker : shuaiqiyy
            ## GitHub : https://github.com/shuaiqiyy/Homework-Killer
            ### ⭐⭐⭐希望大家多多支持开发者⭐⭐⭐
            ```此产品为爱发电，所有收费均是骗子！！！```
            > 版本 v1.0.0
            > 检查更新请前往GitHub页
            """,
            selectable=True,
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            on_tap_link=lambda e: self.page.launch_url(e.data),
        )
        self.content_column.controls.append(md_content)

    def _show_classes_page(self):
        """显示班级页面"""
        if self.user.user_data['code'] == 1:
            self._show_error_dialog("请先登录！")
            return

        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            on_change=self._on_tab_change
        )
        self.content_column.controls.append(self.tabs)
        self._load_classes()

    def _load_classes(self):
        """加载班级数据"""
        code, classes, ids, subjects = self.homework.get_classes()
        if code != 0:
            self._show_error_dialog("获取班级失败！")
            return

        self.tabs.tabs = [
            ft.Tab(
                text=class_name,
                content=ft.Container(padding=10)
            ) for class_name in classes
        ]
        self.page.update()

    def _on_tab_change(self, e):
        """班级标签切换事件"""
        code, classes, class_ids, subjects = self.homework.get_classes()
        if not class_ids or e.control.selected_index >= len(class_ids):
            return

        self.current_class_id = class_ids[e.control.selected_index]
        self.current_subject_id = subjects[e.control.selected_index]
        self._load_homeworks()

    def _load_homeworks(self):
        """加载作业列表"""
        if not self.current_class_id or not self.current_subject_id:
            return

        code, hw_names, hw_ids = self.homework.get_homeworks(
            self.current_class_id, 
            self.current_subject_id
        )

        if code != 0:
            self._show_error_dialog("获取作业失败！")
            return

        # 修复lambda作用域问题
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(name)),
                    ft.DataCell(
                        ft.FilledButton(
                            "一键批改",
                            on_click=lambda e, hwid=hwid: self._show_grading_dialog(
                                homework_id=hwid, 
                                class_id=self.current_class_id
                            )
                        )
                    )
                ]
            ) for name, hwid in zip(hw_names, hw_ids)
        ]

        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("作业名称")),
                ft.DataColumn(ft.Text("操作"))
            ],
            rows=rows
        )

        self.tabs.tabs[self.tabs.selected_index].content = ft.Container(
            content=data_table,
            padding=10
        )
        self.page.update()

    def _show_grading_dialog(self, homework_id, class_id):
        """显示批改对话框"""
        self.current_homework_id = homework_id
        self.current_class_id = class_id

        self.grades_less_slider = ft.Slider(
            min=0, 
            max=10, 
            divisions=10, 
            label="{value}",
            value=3
        )

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("自动批改设置"),
            content=ft.Column([
                ft.Text("最大分差设置："),
                self.grades_less_slider,
                ft.FilledButton(
                    "开始批改",
                    on_click=self._start_grading
                )
            ]),
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _start_grading(self, e):
        """开始批改作业"""
        try:
            if not self.current_homework_id or not self.current_class_id:
                raise ValueError("缺少必要的作业或班级信息")

            success = self.homework.grade_homework(
                self.current_homework_id,
                self.current_class_id,
                int(self.grades_less_slider.value)
            )

            if success:
                self._show_info_dialog("批改完成！")
                self._close_dialog()
                self._load_homeworks()  # 刷新作业列表
            else:
                self._show_error_dialog("批改过程中出现错误！")
        except Exception as err:
            self._show_error_dialog(f"批改失败：{str(err)}")

    def _show_settings_page(self):
        """显示设置页面"""
        content = []
        if self.user.user_data['code'] == 0:
            content.extend([
                ft.Text(f"当前用户：{self.user.user_data['user_name']}", size=18),
                ft.FilledButton("退出登录", on_click=self._logout),
                ft.FilledButton("重新登录", on_click=self._show_login_dialog)
            ])
        else:
            content.append(ft.FilledButton("登录账号", on_click=self._show_login_dialog))
        
        self.content_column.controls.extend(content)

    def _show_login_dialog(self, e):
        """显示登录对话框"""
        self.phone_field = ft.TextField(label="手机号")
        self.password_field = ft.TextField(label="密码", password=True)
        self.api_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(api) for api in api_list],
            label="选择接口"
        )

        dialog = ft.AlertDialog(
            title=ft.Text("用户登录"),
            content=ft.Column([
                self.phone_field,
                self.password_field,
                self.api_dropdown
            ]),
            actions=[
                ft.TextButton("取消", on_click=self._close_dialog),
                ft.TextButton("登录", on_click=self._perform_login)
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _perform_login(self, e):
        """执行登录操作"""
        if self.phone_field.value == "" or self.password_field.value == "":
            self._show_error_dialog("请输入账号密码！")
            return

        success = self.user.login(
            self.phone_field.value,
            self.password_field.value,
            self.api_dropdown.value
        )

        if success:
            self._close_dialog()
            self._on_rail_change(None)  # 刷新界面
            self._show_info_dialog("登录成功！")
        else:
            self._show_error_dialog("登录失败，请检查凭证！")

    def _logout(self, e):
        """退出登录"""
        self.user.save_user_data({'code': 1})
        self._on_rail_change(None)
        self._show_info_dialog("已退出登录")

    def _close_dialog(self, e=None):
        """关闭当前对话框"""
        self.page.dialog.open = False
        self.page.update()

    def _show_error_dialog(self, message):
        """显示错误提示"""
        dialog = ft.AlertDialog(
            title=ft.Text("错误"),
            content=ft.Text(message),
            actions=[ft.TextButton("确定", on_click=self._close_dialog)]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _show_info_dialog(self, message):
        """显示信息提示"""
        dialog = ft.AlertDialog(
            title=ft.Text("提示"),
            content=ft.Text(message),
            actions=[ft.TextButton("确定", on_click=self._close_dialog)]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()