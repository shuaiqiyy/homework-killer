# core.py
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
        if name == None:
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

    def grade_homework(self, hid, class_id, max_grade_diff):
        token = self.user.user_data.get('user_token')
        uid = self.user.user_data.get('user_uid')
        api_type = self.user.user_data.get('api')
        
        code, names, ids, msgs = api.api_student_list_iformance(token, uid, hid, class_id, api_type)
        if code != 0:
            return False

        for sid in ids:
            hight_grades, images, teacher_id = api.api_homework_informance(token, hid, sid, uid, api_type)
            grades = [random_addon.main(g, max_grade_diff, images) for g in hight_grades]
            api.api_homework_work(token, hid, sid, teacher_id, hight_grades, grades, api_type)
        return True