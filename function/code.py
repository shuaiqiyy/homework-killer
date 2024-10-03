def main(code):
    if code == 1:
        return "用户登录信息错误"
    elif code == 2:
        return "班级信息错误"
    elif code == 3:
        return "作业列表错误"
    elif code == 4:
        return "学生列表错误"
    elif code == 5:
        return "无当前插件信息"
    elif code == 6:
        return "作业提交失败"
    else:
        return "未知错误"