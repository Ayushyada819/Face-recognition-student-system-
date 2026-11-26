import json
import os

DATA_FILE = "students_db.json"

def run_student_manager():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            student = json.load(f)
    else:
        student = {}

    while True:
        print("\n/----STUDENT MANAGER APP----/")
        print("1. ADD STUDENT")
        print("2. VIEW STUDENTS")
        print("3. Check Result")
        print("4. BACK TO FACE SYSTEM")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter student name: ").strip().lower()
            roll = input("Enter roll number: ")
            marks = float(input("Enter marks: "))
            student[name] = {
                "roll": roll,
                "marks": marks,
                "status": "PASS" if marks >= 40 else "FAIL"
            }
            with open(DATA_FILE, "w") as f:
                json.dump(student, f, indent=4)
            print(f"✅ {name.title()} successfully added & saved!")

        elif choice == "2":
            if not student:
                print("No students found.")
            else:
                for name, info in student.items():
                    print(f"Name: {name.title()}, Roll: {info['roll']}, Marks: {info['marks']}")

        elif choice == "3":
            name = input("Enter student name to check result: ").strip().lower()
            if name in student:
                info = student[name]
                print(f"Marks: {info['marks']} -> {info['status']}")
            else:
                print("Student not found!")

        elif choice == "4":
            break
