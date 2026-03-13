from pymongo import MongoClient

client = MongoClient("mongodb://mongos:27017")
db = client.university


def show_grades():
    student = input("student id: ")
    grades = db.grades.find({"student_id": student})
    for g in grades:
        print(g)


def add_grade():
    student = input("student id: ")
    course = input("course id: ")
    teacher = input("teacher id: ")
    grade = int(input("grade: "))
    db.grades.insert_one({
        "student_id": student,
        "course_id": course,
        "teacher_id": teacher,
        "grade": grade
    })
    print("added")


def avg_grade():
    student = input("student id: ")
    res = db.grades.aggregate([
        {"$match": {"student_id": student}},
        {"$group": {"_id": "avg", "avg": {"$avg": "$grade"}}}
    ])
    for r in res:
        print("average:", r["avg"])


while True:
    print("\nMENU")
    print("1 show grades")
    print("2 add grade")
    print("3 average")
    print("4 exit")
    choice = input("> ")
    if choice == "1":
        show_grades()
    if choice == "2":
        add_grade()
    if choice == "3":
        avg_grade()
    if choice == "4":
        break