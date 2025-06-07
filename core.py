import asyncio
import json
import logging
import api.api_choose as api
import function.update as update
import function.random_addon as random_addon

class UserManager:
    def __init__(self):
        self.user_data = self._load_user_data()
        
    def _load_user_data(self):
        try:
            with open('user.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'code': 1}

    def save_user_data(self, data):
        with open("user.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.user_data = data

    def login(self, number, password, api_type):
        code, token, uid, name = api.api_user_informance(number, password, api_type)
        if name is None:
            self.save_user_data({'code': 1})
            return False
        else:
            self.save_user_data({
                'code': 0,
                'user_number': number,
                'user_password': password,
                'api': api_type,
                'user_name': name,
                'user_token': token,
                'user_uid': uid,
            })
            return True
    
    # 修复后的异步登录方法
    async def async_login(self, *args):
        """异步登录方法（通用参数处理）"""
        return await asyncio.to_thread(self.login, *args)
    
    def logout(self):
        self.save_user_data({'code': 1})
        return True

class HomeworkManager:
    def __init__(self, user_manager):
        self.user = user_manager
        self.current_class = None
        self.current_homework = None

    def get_classes(self):
        token = self.user.user_data.get('user_token')
        uid = self.user.user_data.get('user_uid')
        api_type = self.user.user_data.get('api')
        return api.api_class_informance(token, uid, api_type)

    def get_homeworks(self, class_id, subject_id):
        token = self.user.user_data.get('user_token')
        uid = self.user.user_data.get('user_uid')
        api_type = self.user.user_data.get('api')
        return api.api_homework_list_informance(token, uid, class_id, subject_id, api_type)

    def get_students(self, hid, class_id):
        """获取学生列表"""
        token = self.user.user_data.get('user_token')
        uid = self.user.user_data.get('user_uid')
        api_type = self.user.user_data.get('api')
        
        return api.api_student_list_iformance(token, uid, hid, class_id, api_type)

    def grade_homework(self, hid, class_id, max_grade_diff):
        token = self.user.user_data.get('user_token')
        uid = self.user.user_data.get('user_uid')
        api_type = self.user.user_data.get('api')
        
        # 添加调试输出
        print(f"[DEBUG] 获取学生列表: hid={hid}, class_id={class_id}, api_type={api_type}")
        
        # 获取学生列表
        code, names, ids, msgs = api.api_student_list_iformance(token, uid, hid, class_id, api_type)
        
        # 检查返回结果
        if code != 0:
            error_msg = f"获取学生列表失败 (错误码: {code})"
            if msgs:  # 如果有错误消息
                error_msg += f": {msgs}"
            print(f"[ERROR] {error_msg}")
            return False

        if not ids or not names:
            print("[WARNING] 学生列表为空")
            return False
            
        print(f"[INFO] 获取到 {len(ids)} 名学生")
        
        # 遍历所有学生进行批改
        for sid, name in zip(ids, names):
            try:
                print(f"[INFO] 批改学生作业: {name} (ID: {sid})")
                
                # 获取学生作业信息
                hight_grades, images, teacher_id = api.api_homework_informance(
                    token, hid, sid, uid, api_type
                )
                
                # 生成随机分数
                grades = [
                    random_addon.main(g, max_grade_diff, images) 
                    for g in hight_grades
                ]
                
                # 提交批改结果
                result = api.api_homework_work(
                    token, hid, sid, teacher_id, hight_grades, grades, api_type
                )
                
                print(f"[SUCCESS] 学生 {name} 批改完成")
                
            except Exception as e:
                print(f"[ERROR] 批改学生 {name} 失败: {str(e)}")
                continue  # 继续处理下一个学生
        
        return True