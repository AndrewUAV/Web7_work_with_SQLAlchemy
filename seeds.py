import random
from faker import Faker
from connect_db import session
from classes import Student, Group, Teacher, Subject, Grade

fake = Faker()


def create_groups():
    groups = [Group(name=f'Group {i}') for i in range(1, 4)]
    session.add_all(groups)
    session.commit()
    return groups


def create_teachers():
    teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
    session.add_all(teachers)
    session.commit()
    return teachers


def create_subjects(teachers):
    subjects = []
    for teacher in teachers:
        for _ in range(random.randint(5, 8)):
            subject = Subject(name=fake.word(), teacher=teacher)
            session.add(subject)
            subjects.append(subject)
    session.commit()
    return subjects


def create_students(groups):
    students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(random.randint(30, 50))]
    session.add_all(students)
    session.commit()
    return students


def create_grades(students, subjects):
    for student in students:
        for subject in subjects:
            grade = Grade(
                value=random.randint(60, 100),
                date_received=fake.date_between(start_date='-1y', end_date='today'),
                student=student,
                subject=subject
            )
            session.add(grade)
    session.commit()
    session.close()


def clear():
    session.query(Student).delete()
    session.query(Group).delete()
    session.query(Teacher).delete()
    session.query(Subject).delete()
    session.query(Grade).delete()
    session.commit()


def main():
    clear()
    groups = create_groups()
    teachers = create_teachers()
    subjects = create_subjects(teachers)
    students = create_students(groups)
    create_grades(students, subjects)
    print("Database seeded successfully!")


if __name__ == "__main__":
    main()
