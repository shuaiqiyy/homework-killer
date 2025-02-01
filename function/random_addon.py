import random

def main(hight_grades, grades_less, img_list):
    try:
        low_grades = float(hight_grades) - float(grades_less)
        hight_grades = float(hight_grades)
        low_grades = int(low_grades)
        hight_grades = int(hight_grades)
        
        if hight_grades > low_grades:
            grades = random.randint(low_grades, hight_grades)
            return grades
        else:
            return None
    except ValueError:
        return None