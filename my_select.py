
from sqlalchemy import func
from connect_db import session
from classes import Student, Group, Teacher, Subject, Grade


def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    return session.query(
        Student.name, func.avg(Grade.value).label("average_score")
    ).join(Grade).group_by(Student.id).order_by(func.avg(Grade.value).desc()).limit(5).all()


def select_2():
    # Знайти студента із найвищим середнім балом з певного предмета.
    subject_id = input("subject_id: ")
    return session.query(
        Student.name,
        func.avg(Grade.value).label('average_score'),
        Grade.subject_id
    ).join(Grade).filter(Grade.subject_id == subject_id).group_by(Student.id).order_by(
        func.avg(Grade.value).desc()).first()


def select_3():
    group_id = input("group_id: ")
    subject_id = input("subject_id: ")
    # Знайти середній бал у групах з певного предмета.
    return session.query(
        Group.name,
        func.avg(Grade.value).label('average_score')
    ).select_from(Group).join(Student, Group.id == Student.group_id).join(Grade, Student.id == Grade.student_id).filter(
        Student.group_id == group_id,
        Grade.subject_id == subject_id
    ).group_by(Group.id).all()


def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок).
    return session.query(
        func.avg(Grade.value).label('stream_average_score')
    ).scalar()


def select_5():
    teacher_id = input("teacher_id: ")
    return session.query(
        Subject.name
    ).filter(Subject.teacher_id == teacher_id).all()


def select_6():
    # Знайти список студентів у певній групі.
    group_id = input("group_id: ")
    return session.query(
        Student.name
    ).filter(Student.group_id == group_id).all()


def select_7():
    group_id = input("group_id: ")
    subject_id = input("subject_id: ")
    # Знайти оцінки студентів у окремій групі з певного предмета.
    return session.query(
        Student.name,
        Grade.value
    ).join(Grade).filter(Student.group_id == group_id, Grade.subject_id == subject_id).all()


def select_8():
    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    teacher_id = input("teacher_id: ")
    return session.query(
        func.avg(Grade.value).label('teacher_average_score')
    ).join(Subject).filter(Subject.teacher_id == teacher_id).scalar()


def select_9():
    # Знайти список курсів, які відвідує певний студент.
    student_id = input("student_id: ")
    return session.query(
        Subject.name
    ).join(Grade, Grade.subject_id == Subject.id).filter(Grade.student_id == student_id).group_by(Subject.id).all()

def select_10():
    # Список курсів, які певному студенту читає певний викладач.
    student_id = input("student_id: ")
    teacher_id = input("teacher_id: ")
    return (session.query(
        Subject.name
    ).join(Grade, Grade.subject_id == Subject.id)
            .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
            .group_by(Subject.id)).all()

def main():
    dict_of_selects = {
        1: select_1,
        2: select_2,
        3: select_3,
        4: select_4,
        5: select_5,
        6: select_6,
        7: select_7,
        8: select_8,
        9: select_9,
        10: select_10
    }

    while True:
        user_input = input("Please enter select id from 1 to 10, 0 - for close: ")
        select_id = int(user_input)
        if select_id == 0:
            break
        elif select_id in dict_of_selects:
            result = dict_of_selects[select_id]()
            print(result)
        else:
            print(f"Param {select_id} does not exist")


if __name__ == "__main__":
    main()