import flet as ft
from core import UserManager, HomeworkManager
import api.api_choose as api
from api.api_choose import api_choose
import function.random_addon as random_addon
import function.update as update
import asyncio

api_list = api_choose()

class HomeworkKillerUI:
    def __init__(self, page: ft.Page, user_manager: UserManager, homework_manager: HomeworkManager):
        self.page = page
        self.user = user_manager
        self.homework = homework_manager
        self.current_class_id = None
        self.current_subject_id = None
        self.current_homework_id = None
        self.student_list = []  # 存储学生列表
        self._setup_ui()

    def _setup_ui(self):
        """初始化主界面布局"""
        self.page.title = "Homework Killer"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

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
        
        try:
            if self.rail.selected_index == 0:
                self._show_home_page()
            elif self.rail.selected_index == 1:
                self._show_loading()
                self._show_classes_page()
            elif self.rail.selected_index == 2:
                self._show_settings_page()
        finally:
            self._hide_loading()

    def _show_loading(self):
        """显示加载指示器"""
        if not any(isinstance(control, ft.Row) for control in self.content_column.controls):
            self.content_column.controls.append(
                ft.Row(
                    [ft.ProgressRing()],
                    alignment=ft.MainAxisAlignment.CENTER,
                    key="loading"  # 添加唯一标识
                )
            )
            self.page.update()

    def _hide_loading(self):
        """隐藏加载指示器（精确移除）"""
        # 查找并移除所有加载指示器
        self.content_column.controls = [
            control for control in self.content_column.controls
            if not (isinstance(control, ft.Row) and control.key == "loading")
        ]
        self.page.update()

    def _show_home_page(self):
        """显示简约风格的主页（纯色背景）"""
        # ===== 创建主容器 =====
        main_card = ft.Card(
            elevation=8,
            margin=ft.margin.symmetric(horizontal=25, vertical=30),
            shape=ft.RoundedRectangleBorder(radius=12),
            content=ft.Container(
                bgcolor=ft.colors.WHITE,  # 使用纯白色背景
                padding=25,
                border_radius=12,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        # ===== 应用标题和Logo =====
                        ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                            controls=[
                                ft.Image(
                                    src="./logo.ico",
                                    width=70,
                                    height=70,
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                ft.Text(
                                    "Homework Killer",
                                    size=26,
                                    weight=ft.FontWeight.W_700,
                                    color=ft.colors.BLACK87
                                ),
                            ]
                        ),
                        
                        # ===== 开发者信息 =====
                        ft.Container(
                            bgcolor=ft.colors.GREY_50,  # 浅灰色背景
                            padding=15,
                            border_radius=10,
                            content=ft.Column(
                                spacing=12,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.PERSON_OUTLINE, size=20, color=ft.colors.BLUE_700),
                                            ft.Text("开发者", size=14, color=ft.colors.GREY_600),
                                        ]
                                    ),
                                    ft.Text("shuaiqiyy", 
                                            size=16, 
                                            weight=ft.FontWeight.W_500,
                                            color=ft.colors.BLACK87),
                                    
                                    ft.Divider(height=8, color=ft.colors.TRANSPARENT),
                                    
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.CODE_OUTLINED, size=20, color=ft.colors.BLUE_700),
                                            ft.Text("GitHub 项目", size=14, color=ft.colors.GREY_600),
                                        ]
                                    ),
                                    ft.TextButton(
                                        content=ft.Text("https://github.com/shuaiqiyy/Homework-Killer",
                                                        size=14,
                                                        color=ft.colors.BLUE_700),
                                        on_click=lambda _: self.page.launch_url(
                                            "https://github.com/shuaiqiyy/Homework-Killer")
                                    ),
                                ]
                            )
                        ),
                        
                        # ===== 重要提示 =====
                        ft.Container(
                            bgcolor=ft.colors.AMBER_50,
                            padding=15,
                            border_radius=10,
                            content=ft.Row(
                                spacing=10,
                                controls=[
                                    ft.Icon(ft.icons.INFO_OUTLINE, color=ft.colors.AMBER_700, size=20),
                                    ft.Container(
                                        content=ft.Text(
                                            "此产品为开源项目，所有收费均是骗子！",
                                            size=14,
                                            weight=ft.FontWeight.W_500,
                                            color=ft.colors.AMBER_900
                                        ),
                                        padding=ft.padding.only(left=5)
                                    )
                                ]
                            )
                        ),
                        
                        # ===== 操作按钮 =====
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                # 支持按钮
                                ft.OutlinedButton(
                                    content=ft.Row([
                                        ft.Icon(ft.icons.STAR_BORDER, size=16, color=ft.colors.BLUE_700),
                                        ft.Text("支持开发者", size=14, color=ft.colors.BLUE_700)
                                    ]),
                                    style=ft.ButtonStyle(
                                        padding=15,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=lambda _: self.page.launch_url(
                                        "https://github.com/shuaiqiyy/Homework-Killer")
                                ),
                                
                                # 更新按钮
                                ft.OutlinedButton(
                                    content=ft.Row([
                                        ft.Icon(ft.icons.UPDATE, size=16, color=ft.colors.GREEN_700),
                                        ft.Text("检查更新", size=14, color=ft.colors.GREEN_700)
                                    ]),
                                    style=ft.ButtonStyle(
                                        padding=15,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    on_click=self._check_update
                                )
                            ]
                        ),
                        
                        # ===== 版本信息 =====
                        ft.Text(
                            "版本 v1.0.0",
                            size=12,
                            color=ft.colors.GREY_600
                        )
                    ]
                )
            )
        )

        # 更新页面内容
        self.content_column.controls.clear()
        self.content_column.controls.append(main_card)
        self.page.update()

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
        """加载班级数据（修复加载状态）"""
        try:
            code, classes, ids, subjects = self.homework.get_classes()
            if code != 0:
                raise ValueError(f"获取班级失败，错误码：{code}")
            
            if not (len(classes) == len(ids) == len(subjects)):
                raise ValueError("返回的班级数据不完整")

            self.tabs.tabs = [
                ft.Tab(
                    text=class_name,
                    content=ft.Container(padding=10)
                ) for class_name in classes
            ]
        except Exception as e:
            self._show_error_dialog(str(e))
        finally:
            self._hide_loading()  # 确保加载完成时隐藏

    def _on_tab_change(self, e):
        """班级标签切换事件（添加加载状态）"""
        try:
            self._show_loading()
            code, classes, class_ids, subjects = self.homework.get_classes()
            if not class_ids or e.control.selected_index >= len(class_ids):
                return

            self.current_class_id = class_ids[e.control.selected_index]
            self.current_subject_id = subjects[e.control.selected_index]
            self._load_homeworks()
        except Exception as e:
            self._show_error_dialog(str(e))
        finally:
            self._hide_loading()

    def _load_homeworks(self):
        """加载作业列表（修复加载状态）"""
        try:
            self._show_loading()  # 显示加载状态
            if not self.current_class_id or not self.current_subject_id:
                raise ValueError("缺少班级或科目信息")

            code, hw_names, hw_ids = self.homework.get_homeworks(
                self.current_class_id, 
                self.current_subject_id
            )

            if code != 0:
                raise ValueError(f"获取作业失败，错误码：{code}")
            # 使用ListView优化布局
            homework_list = ft.ListView(expand=True, spacing=10)
            
            for idx, (name, hwid) in enumerate(zip(hw_names, hw_ids)):
                homework_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                leading=ft.Text(f"{idx+1}", style=ft.TextThemeStyle.TITLE_MEDIUM),
                                title=ft.Text(name, style=ft.TextThemeStyle.BODY_LARGE),
                                trailing=ft.FilledButton(
                                    "一键批改",
                                    style=ft.ButtonStyle(
                                        padding=ft.padding.symmetric(20, 15),
                                        shape=ft.RoundedRectangleBorder(radius=5)
                                    ),
                                    on_click=lambda e, hwid=hwid: self._show_grading_dialog(
                                        homework_id=hwid,
                                        class_id=self.current_class_id
                                    )
                                ),
                                height=60,
                                mouse_cursor=ft.MouseCursor.CLICK
                            ),
                            padding=10,
                        ),
                        elevation=2
                    )
                )

            content = homework_list if hw_names else ft.Text("当前没有待批改作业", style="italic")

            self.tabs.tabs[self.tabs.selected_index].content = ft.Container(
                content=content,
                padding=10,
                expand=True
            )
        except Exception as e:
            self._show_error_dialog(str(e))
        finally:
            self._hide_loading()  # 确保加载完成时隐藏

    def _show_grading_dialog(self, homework_id, class_id):
        """显示批改对话框 - 包含学生列表"""
        self.current_homework_id = homework_id
        self.current_class_id = class_id

        # 创建滑块
        self.grades_less_slider = ft.Slider(
            min=0, 
            max=10, 
            divisions=10, 
            label="{value}分差",
            value=3,
            width=300
        )
        
        # 获取学生列表
        self.student_list = self._get_student_list(homework_id, class_id)
        
        # 创建学生列表显示组件
        student_list_widget = self._create_student_list_widget()
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("自动批改设置"),
            content=ft.Column([
                ft.Text("学生列表:", weight=ft.FontWeight.BOLD),
                student_list_widget,
                ft.Divider(height=10),
                ft.Text("最大分差设置："),
                self.grades_less_slider,
                ft.FilledButton(
                    "开始批改",
                    icon=ft.icons.AUTO_AWESOME,
                    on_click=self._start_grading
                )
            ], scroll=ft.ScrollMode.AUTO, height=400),
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def _get_student_list(self, homework_id, class_id):
        """获取学生列表数据"""
        try:
            token = self.user.user_data.get('user_token')
            uid = self.user.user_data.get('user_uid')
            api_type = self.user.user_data.get('api')
            
            # 获取学生列表
            code, names, ids, msgs = api.api_student_list_iformance(
                token, uid, homework_id, class_id, api_type
            )
            
            if code == 0 and names:
                return list(zip(names, ids))
            return []
        except Exception as e:
            print(f"获取学生列表失败: {str(e)}")
            return []
    
    def _create_student_list_widget(self):
        """创建学生列表UI组件"""
        if not self.student_list:
            return ft.Text("⚠️ 未获取到学生列表", color=ft.colors.RED)
        
        # 创建可滚动的列表视图
        list_view = ft.ListView(expand=True, spacing=5, height=200)
        
        for name, student_id in self.student_list:
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(name),
                    subtitle=ft.Text(f"ID: {student_id}", size=12, color=ft.colors.GREY),
                    leading=ft.Icon(ft.icons.PERSON),
                    dense=True
                )
            )
        
        return ft.Container(
            content=list_view,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=5,
            padding=10
        )
    
    def _start_grading(self, e):
        """开始批改作业 - 显示进度"""
        try:
            if not self.student_list:
                self._show_error_dialog("没有学生需要批改")
                return
                
            # 创建进度对话框
            self._create_progress_dialog()
            
            # 启动批改任务
            self.page.run_task(self._run_grading_task)
        except Exception as err:
            self._show_error_dialog(f"❗ 批改失败：{str(err)}")
    
    def _create_progress_dialog(self):
        """创建批改进度对话框"""
        self.progress_bar = ft.ProgressBar(width=400, value=0)
        self.progress_text = ft.Text("准备开始批改...")
        
        self.progress_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("批改进度"),
            content=ft.Column([
                self.progress_text,
                self.progress_bar
            ]),
            actions=[]
        )
        
        # 关闭之前的对话框
        if self.page.dialog and self.page.dialog.open:
            self.page.dialog.open = False
            
        self.page.dialog = self.progress_dialog
        self.progress_dialog.open = True
        self.page.update()
    
    async def _run_grading_task(self):
        """执行批改任务"""
        try:
            total_students = len(self.student_list)
            
            for i, (name, student_id) in enumerate(self.student_list):
                # 更新进度
                progress = (i + 1) / total_students
                self.progress_bar.value = progress
                self.progress_text.value = f"正在批改 {name} 的作业 ({i+1}/{total_students})"
                self.page.update()
                
                # 执行批改
                success = await self._grade_student(student_id)
                
                if not success:
                    self.progress_text.value += " ❌"
                else:
                    self.progress_text.value += " ✅"
                
                self.page.update()
                await asyncio.sleep(0.5)
            
            # 完成后的处理
            self._close_dialog()
            self._show_info_dialog(f"✅ 批改完成！共批改 {total_students} 名学生")
            
            # 刷新作业列表
            self._load_homeworks()
            
        except Exception as e:
            self._close_dialog()
            self._show_error_dialog(f"批改过程中出错: {str(e)}")
    
    async def _grade_student(self, student_id):
        """批改单个学生的作业"""
        try:
            token = self.user.user_data.get('user_token')
            uid = self.user.user_data.get('user_uid')
            api_type = self.user.user_data.get('api')
            hight_grades, images, teacher_id = api.api_homework_informance(
                token, self.current_homework_id, student_id, uid, api_type
            )
            max_diff = int(self.grades_less_slider.value)
            grades = [
                random_addon.main(g, max_diff, images) 
                for g in hight_grades
            ]
            result = api.api_homework_work(
                token, self.current_homework_id, student_id, 
                teacher_id, hight_grades, grades, api_type
            )
            
            return result
        except Exception as e:
            print(f"批改学生 {student_id} 失败: {str(e)}")
            return False

    def _show_settings_page(self):
        """显示美化后的设置页面"""
        # 清空内容区域
        self.content_column.controls.clear()
        
        # 创建主卡片容器
        main_card = ft.Card(
            elevation=10,
            margin=ft.margin.all(20),
            shape=ft.RoundedRectangleBorder(radius=15),
            content=ft.Container(
                padding=20,
                border_radius=15,
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#f5f7fa", "#e4edf5"]
                ),
                content=ft.Column(
                    spacing=25,
                    controls=[]
                )
            )
        )
        
        # 用户信息部分
        if self.user.user_data['code'] == 0:
            user_section = ft.Container(
                padding=20,
                border_radius=10,
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_300),
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=36, color=ft.colors.BLUE_700),
                                ft.Text(f"{self.user.user_data['user_name']}", 
                                        size=20, 
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.colors.BLUE_900)
                            ]
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[
                                ft.FilledButton(
                                    content=ft.Row([
                                        ft.Icon(ft.icons.LOGOUT, color=ft.colors.WHITE),
                                        ft.Text("退出登录", color=ft.colors.WHITE)
                                    ]),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.RED_700,
                                        padding=15,
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    ),
                                    on_click=self._logout
                                ),
                                ft.FilledButton(
                                    content=ft.Row([
                                        ft.Icon(ft.icons.REFRESH, color=ft.colors.WHITE),
                                        ft.Text("重新登录", color=ft.colors.WHITE)
                                    ]),
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.colors.BLUE_700,
                                        padding=15,
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    ),
                                    on_click=self._show_login_dialog
                                )
                            ]
                        )
                    ]
                )
            )
            main_card.content.content.controls.append(user_section)
        else:
            login_button = ft.Container(
                padding=20,
                content=ft.FilledButton(
                    content=ft.Row([
                        ft.Icon(ft.icons.LOGIN, size=24, color=ft.colors.WHITE),
                        ft.Text("登录账号", size=18, color=ft.colors.WHITE)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.BLUE_700,
                        padding=20,
                        shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    width=250,
                    on_click=self._show_login_dialog
                ),
                alignment=ft.alignment.center
            )
            main_card.content.content.controls.append(login_button)
        
        # 检查更新按钮
        update_section = ft.Container(
            padding=ft.padding.symmetric(vertical=15),
            content=ft.FilledButton(
                content=ft.Row([
                    ft.Icon(ft.icons.UPDATE, size=24, color=ft.colors.WHITE),
                    ft.Text("检查更新", size=18, color=ft.colors.WHITE)
                ], alignment=ft.MainAxisAlignment.CENTER),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.PURPLE_700,
                    padding=20,
                    shape=ft.RoundedRectangleBorder(radius=12)
                ),
                width=250,
                on_click=self._check_update
            ),
            alignment=ft.alignment.center
        )
        main_card.content.content.controls.append(update_section)
        
        # 添加附加信息
        info_text = ft.Container(
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Homework Killer", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"版本 v1.0.0", color=ft.colors.GREY_600),
                    ft.Text("© 2023 shuaiqiyy", color=ft.colors.GREY_500),
                    ft.TextButton(
                        content=ft.Text("GitHub 项目主页", color=ft.colors.BLUE),
                        on_click=lambda _: self.page.launch_url(
                            "https://github.com/shuaiqiyy/Homework-Killer")
                    )
                ]
            )
        )
        main_card.content.content.controls.append(info_text)
        
        # 添加到内容区域
        self.content_column.controls.append(main_card)
        self.page.update()

    async def _check_update(self, e):
        """检查更新（异步）"""
        # 显示加载中
        self._show_info_dialog("正在检查更新...")
        self.page.update()
        
        try:
            # 在后台线程中运行更新检查
            update_result = await asyncio.to_thread(update.main)
            
            # 关闭之前的对话框
            self._close_dialog()
            
            # 显示更新结果
            self._show_info_dialog(update_result)
        except Exception as e:
            self._close_dialog()
            self._show_error_dialog(f"检查更新失败: {str(e)}")
    
    def _show_login_dialog(self, e):
        """显示美化后的登录对话框"""
        # 创建带图标的输入字段
        self.phone_field = ft.TextField(
            label="手机号",
            keyboard_type=ft.KeyboardType.PHONE,
            max_length=11,
            prefix_text="+86 ",
            helper_text="请输入注册手机号",
            prefix_icon=ft.icons.PHONE_ANDROID,
            border_radius=10,
            border_color=ft.colors.BLUE_GREY_300,
            focused_border_color=ft.colors.BLUE_700,
            content_padding=15,
            text_size=16,
            height=70
        )
        
        self.password_field = ft.TextField(
            label="密码",
            password=True,
            can_reveal_password=True,
            helper_text="6-20位字母数字组合",
            prefix_icon=ft.icons.LOCK,
            border_radius=10,
            border_color=ft.colors.BLUE_GREY_300,
            focused_border_color=ft.colors.BLUE_700,
            content_padding=15,
            text_size=16,
            height=70
        )
        
        # 创建带图标的API选择器
        self.api_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(api) for api in api_list],
            label="选择接口",
            prefix_icon=ft.icons.API,
            border_radius=10,
            border_color=ft.colors.BLUE_GREY_300,
            focused_border_color=ft.colors.BLUE_700,
            content_padding=15,
            text_size=16,
            height=60,
            width=300
        )
        
        # 创建对话框内容容器
        content_container = ft.Container(
            width=400,
            padding=20,
            bgcolor=ft.colors.GREY_50,
            border_radius=15,
            content=ft.Column(
                spacing=20,
                controls=[
                    # 标题行
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.icons.LOGIN, size=36, color=ft.colors.BLUE_700),
                            ft.Text("用户登录", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)
                        ]
                    ),
                    
                    # 表单区域
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=10, vertical=15),
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        border=ft.border.all(1, ft.colors.GREY_200),
                        content=ft.Column(
                            spacing=25,
                            controls=[
                                self.phone_field,
                                self.password_field,
                                self.api_dropdown
                            ]
                        )
                    ),
                    
                    # 按钮区域
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=15,
                        controls=[
                            ft.OutlinedButton(
                                content=ft.Row([
                                    ft.Icon(ft.icons.CANCEL, size=18),
                                    ft.Text("取消")
                                ]),
                                style=ft.ButtonStyle(
                                    padding=15,
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                ),
                                on_click=self._close_dialog
                            ),
                            ft.FilledButton(
                                content=ft.Row([
                                    ft.Icon(ft.icons.LOGIN, size=18, color=ft.colors.WHITE),
                                    ft.Text("登录", color=ft.colors.WHITE)
                                ]),
                                style=ft.ButtonStyle(
                                    bgcolor=ft.colors.BLUE_700,
                                    padding=15,
                                    shape=ft.RoundedRectangleBorder(radius=10)
                                ),
                                on_click=self._perform_login
                            )
                        ]
                    )
                ]
            )
        )
        
        # 创建对话框
        dialog = ft.AlertDialog(
            content=content_container,
            content_padding=0,
            shape=ft.RoundedRectangleBorder(radius=20)
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    async def _perform_login(self, e):
        """执行登录操作（异步版本）"""
        # 添加加载指示器
        loading_indicator = ft.ProgressRing(width=20, height=20, stroke_width=2)
        self.page.dialog.content.content.controls[2].controls[1].content = ft.Row([
            loading_indicator,
            ft.Text("登录中...", color=ft.colors.WHITE)
        ])
        self.page.update()
        
        if not all([self.phone_field.value, self.password_field.value]):
            self._show_error_dialog("请输入账号密码！")
            # 重置登录按钮
            self._reset_login_button()
            return

        try:
            success = await self.user.async_login(
                self.phone_field.value,
                self.password_field.value,
                self.api_dropdown.value
            )
        except Exception as e:
            self._show_error_dialog(f"登录错误：{str(e)}")
            # 重置登录按钮
            self._reset_login_button()
            return

        # 重置登录按钮
        self._reset_login_button()
        
        if success:
            self._close_dialog()
            self._on_rail_change(None)
            self._show_info_dialog("🎉 登录成功！")
        else:
            self._show_error_dialog("登录失败，请检查账号密码！")
    
    def _reset_login_button(self):
        """重置登录按钮状态"""
        if self.page.dialog and self.page.dialog.open:
            self.page.dialog.content.content.controls[2].controls[1].content = ft.Row([
                ft.Icon(ft.icons.LOGIN, size=18, color=ft.colors.WHITE),
                ft.Text("登录", color=ft.colors.WHITE)
            ])
            self.page.update()

    def _logout(self, e):
        """退出登录"""
        self.user.logout()
        self.current_class_id = None
        self.current_subject_id = None
        self.current_homework_id = None
        self._on_rail_change(None)
        self._show_info_dialog("已退出登录")

    def _close_dialog(self, e=None):
        """关闭当前对话框"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def _show_error_dialog(self, message):
        """显示错误提示"""
        dialog = ft.AlertDialog(
            title=ft.Text("错误", color=ft.colors.RED),
            content=ft.Text(message),
            actions=[ft.TextButton("确定", on_click=self._close_dialog)]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _show_info_dialog(self, message):
        """显示信息提示"""
        dialog = ft.AlertDialog(
            title=ft.Text("提示", color=ft.colors.BLUE),
            content=ft.Text(message),
            actions=[ft.TextButton("确定", on_click=self._close_dialog)]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()