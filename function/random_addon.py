import random

def main(hight_grades,grades_less,img_list):
    low_grades = hight_grades - grades_less
    hight_grades = int(hight_grades)
    low_grades = int(low_grades)
    if hight_grades > low_grades:
        grades = random.randint(low_grades,hight_grades)
        return grades
    else:
        grades = None
        return grades