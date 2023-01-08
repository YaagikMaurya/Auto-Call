import mysql.connector
import cv2 as cv
import numpy as np
import face_recognition
import datetime

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="CollegeClassAttendance"
)
cursor = conn.cursor()
# find all faces in a picture
# focus on faces and recognise them even if angle is different or lighting
# be able to pick out unique features of face
# compare a face to a database to determine identity

# known_face_encoding = array of encodings of images in database
# known_face_names = array of corresponding identities

cursor.execute("SELECT face_vector FROM students")

# Fetch the result
results = cursor.fetchall()

# Convert the binary strings to ndarrays
known_face_encodings = []
for result in results:
    face_encoding = np.frombuffer(result[0], dtype=np.float64).reshape(128, )
    known_face_encodings.append(face_encoding)

# student id
cursor.execute("SELECT student_id FROM students")

# Fetch the result
results = cursor.fetchall()

known_ids = []
for result in results:
    known_ids.append(str(result[0]))
process_frame = True

capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Cannot open camera.")

identified_ids = []
date_lst = []
time_lst = []
while True:
    ret, frame = capture.read()
    if not ret:
        print("Cannot open camera")

    if process_frame:
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            id = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                id = known_ids[best_match_index]

            if id not in identified_ids:
                now = datetime.datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")
                # Execute a query to insert the date and time into the table
                #cursor.execute("INSERT INTO attendance (date, time) VALUES (%s, %s)", (date, time))
                identified_ids.append(id)
                date_lst.append(date)
                time_lst.append(time)

    process_frame = not process_frame

    for (top, right, bottom, left), name in zip(face_locations, identified_ids):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv.imshow('Video', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()
print(identified_ids)
print(date_lst)
print(time_lst)

# If a matching student was found
for i in range(len(identified_ids)):
    # Insert an attendance record for the student
        attendance_record = [identified_ids[i], date_lst[i], time_lst[i], "Present"]
        query = "INSERT INTO attendance (attendance_id, date, time, attendance_status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, attendance_record)
        conn.commit()

