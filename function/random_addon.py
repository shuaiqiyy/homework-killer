import random

def homwork_evaluation_random(hight_grades,low_grades):
    hight_grades = int(hight_grades)
    low_grades = int(low_grades)
    if hight_grades > low_grades:
        grades = random.randint(hight_grades,low_grades)
        return grades
    else:
        grades = None
        return grades