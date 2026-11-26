import cv2
import numpy as np
import os
import json
import student_management

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

MODEL_FILE = "multi_faces.yml"
NAMES_FILE = "names.json"
DATA_FILE = "students_db.json"

def register_face():
    name = input("\nJiska face register karna hai uska NAAM likhein: ").strip()
    
    if os.path.exists(NAMES_FILE):
        with open(NAMES_FILE, "r") as f:
            names = json.load(f)
    else:
        names = {}

    user_id = len(names) + 1
    names[str(user_id)] = name

    cap = cv2.VideoCapture(0)
    print(f"Camera khul raha hai... {name}, camera ke samne dekhein. Photo lene ke liye 's' dabayein.")
    
    faces_samples = []
    ids = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, "Press 's' to Capture", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        cv2.imshow("Register Face", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and len(faces) > 0:
            (x, y, w, h) = faces[0]
            for _ in range(15):
                faces_samples.append(gray[y:y+h, x:x+w])
                ids.append(user_id)
            break

    cap.release()
    cv2.destroyAllWindows()

    if len(faces_samples) > 0:
        if os.path.exists(MODEL_FILE):
            recognizer.read(MODEL_FILE)
            recognizer.update(faces_samples, np.array(ids))
        else:
            recognizer.train(faces_samples, np.array(ids))
        
        recognizer.save(MODEL_FILE)
        with open(NAMES_FILE, "w") as f:
            json.dump(names, f)
        print(f"✅ {name} ka face successfully register ho gaya!")
    else:
        print("❌ Face capture nahi ho paya.")

def authenticate_user():
    if not os.path.exists(MODEL_FILE) or not os.path.exists(NAMES_FILE):
        print("⚠️ Pehle kam se kam ek face register karein!")
        return None

    recognizer.read(MODEL_FILE)
    with open(NAMES_FILE, "r") as f:
        names = json.load(f)

    cap = cv2.VideoCapture(0)
    print("\nCamera khul raha hai... Face verify karne ke liye camera mein dekhein ('q' se cancel karein).")
    verified_user = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if confidence < 70:
                verified_user = names.get(str(id_))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Verified: {verified_user}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Face Authentication", frame)
        key = cv2.waitKey(1) & 0xFF
        if verified_user or key == ord('q'):
            cv2.waitKey(1000)
            break

    cap.release()
    cv2.destroyAllWindows()
    return verified_user

while True:
    print("\n=========================================")
    print("   CONNECTED STUDENT & FACE SYSTEM")
    print("=========================================")
    print("1. Open Student Management (Add/View Data)")
    print("2. Register New Face")
    print("3. Verify Face & Show Student Details")
    print("4. Exit")

    main_choice = input("Apna option chunein (1/2/3/4): ")

    if main_choice == "1":
        student_management.run_student_manager()
    elif main_choice == "2":
        register_face()
    elif main_choice == "3":
        user = authenticate_user()
        if user:
            print(f"\n✅ Face Verified! Welcome {user}")
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    all_students = json.load(f)
                
                student_info = all_students.get(user.strip().lower())
                if student_info:
                    print("------ STUDENT DETAILS ------")
                    print(f"Name   : {user.title()}")
                    print(f"Roll No: {student_info['roll']}")
                    print(f"Marks  : {student_info['marks']}")
                    print(f"Result : {student_info['status']}")
                    print("-----------------------------")
                else:
                    print("⚠️ Face verify ho gaya, par Student Management mein is naam ka record nahi mila!")
            else:
                print("⚠️ Abhi tak Student Management mein koi record save nahi hua hai.")
    elif main_choice == "4":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")
