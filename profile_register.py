import tkinter
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import ImageTk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import mysql.connector
import cv2
import numpy as np
import face_recognition


def enter_data():
    accepted = accept_var.get()

    if accepted == "Accepted":
        # User info
        firstname = first_name_entry.get()
        lastname = last_name_entry.get()

        if firstname and lastname:
            title = title_combobox.get()
            # age = age_spinbox.get()
            # nationality = nationality_combobox.get()

            # Course info
            registration_status = reg_status_var.get()
            courses = courses_spinbox.get()
            numsemesters = numsemesters_spinbox.get()
            student_id = title_combobox.get()

            print("First name: ", firstname, "Last name: ", lastname, "Student ID: ", student_id)
            #print("Title: ", title, "Age: ", age, "Nationality: ", nationality)
            print("# Courses: ", courses, "# Semesters: ", numsemesters)
            print("Registration status", registration_status)
            print("------------------------------------------")

            image = face_recognition.load_image_file(filename)
            face_encoding = face_recognition.face_encodings(image)[0]
            binary = face_encoding.tobytes()


            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="CollegeClassAttendance"
            )
            cursor = conn.cursor()

            # Create Table
            # conn = sqlite3.connect('data.db')
            # table_create_query = '''CREATE TABLE IF NOT EXISTS Student_Data
            #         (firstname TEXT, lastname TEXT, title TEXT, age INT, nationality TEXT,
            #         registration_status TEXT, num_courses INT, num_semesters INT)
            # '''
            # conn.execute(table_create_query)

            # Insert Data
            data_insert_query = 'INSERT INTO students(student_id,first_name,last_name,face_vector) values(%s,%s,%s,%s)'
            data_insert_tuple = (student_id,firstname, lastname,binary)
            cursor = conn.cursor()
            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            conn.close()



        else:
            tkinter.messagebox.showwarning(title="Error", message="First name and last name are required.")
    else:
        tkinter.messagebox.showwarning(title="Error", message="You have not accepted the terms")


window = tkinter.Tk()
window.title("Data Entry Form")


def my_upload():
    global filename, img
    f_types = [('All Files', '*.*'),
               ('JPG', '*.jpg'),
               ('PNG', '*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = ImageTk.PhotoImage(file=filename)
    # b3 = ttk.Button(window, image=img)  # display image on this button
    # b3.grid(row=4, column=1, columnspan=3, pady=20)


frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame = tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)

first_name_label = tkinter.Label(user_info_frame, text="First Name")
first_name_label.grid(row=0, column=0)
last_name_label = tkinter.Label(user_info_frame, text="Last Name")
last_name_label.grid(row=0, column=1)

first_name_entry = tkinter.Entry(user_info_frame)
last_name_entry = tkinter.Entry(user_info_frame)
first_name_entry.grid(row=1, column=0)
last_name_entry.grid(row=1, column=1)

student_id = tkinter.Label(user_info_frame, text="Student ID")
title_combobox = ttk.Entry(user_info_frame)
student_id.grid(row=0, column=2)
title_combobox.grid(row=1, column=2)

for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Saving Course Info
courses_frame = tkinter.LabelFrame(frame)
courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

registered_label = tkinter.Label(courses_frame, text="Registration Status")

reg_status_var = tkinter.StringVar(value="Not Registered")
registered_check = tkinter.Checkbutton(courses_frame, text="Currently Registered",
                                       variable=reg_status_var, onvalue="Registered", offvalue="Not registered")

registered_label.grid(row=0, column=0)
registered_check.grid(row=1, column=0)

courses_label = tkinter.Label(courses_frame, text="Courses")
courses_spinbox = ttk.Combobox(courses_frame,
                               values=("Architecture", "Civil", "CS", "IT", "Mechanical", "QEDS"))
courses_label.grid(row=0, column=1)
courses_spinbox.grid(row=1, column=1)

numsemesters_label = tkinter.Label(courses_frame, text="# Semesters")
numsemesters_spinbox = tkinter.Spinbox(courses_frame, from_=1, to=10)
numsemesters_label.grid(row=0, column=2)
numsemesters_spinbox.grid(row=1, column=2)

for widget in courses_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Accept terms
terms_frame = tkinter.LabelFrame(frame, text="Terms & Conditions")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text="I accept the terms and conditions.",
                                  variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)

# Button
upload = tkinter.Button(frame,text="Upload Photo",command=lambda :my_upload())
upload.grid(row=3, column=0, sticky="news", padx=20, pady=10)

button = tkinter.Button(frame, text="Enter data", command=enter_data)
button.grid(row=4, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
