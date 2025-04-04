import flet as ft
from core import UserManager, HomeworkManager
from ui import HomeworkKillerUI

def main(page: ft.Page):
    # 初始化核心组件
    user_manager = UserManager()
    homework_manager = HomeworkManager(user_manager)
    
    # 初始化UI
    ui = HomeworkKillerUI(page, user_manager, homework_manager)
    
    # 自动登录检查
    if user_manager.user_data['code'] == 0:
        try:
            user_manager.login(
                user_manager.user_data['user_number'],
                user_manager.user_data['user_password'],
                user_manager.user_data['api']
            )
        except Exception as e:
            ui._show_error(f"自动登录失败: {str(e)}")

ft.app(target=main)