CREATE DATABASE CollegeClassAttendance;

USE CollegeClassAttendance;

CREATE TABLE students (
  student_id INT PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  face_vector BLOB NOT NULL
);

CREATE TABLE courses (
  course_id INT PRIMARY KEY,
  course_name VARCHAR(255) NOT NULL,
  instructor_name VARCHAR(255) NOT NULL
);

CREATE TABLE student_enrollment (
  enrollment_id INT PRIMARY KEY,
  student_id INT NOT NULL,
  course_id INT NOT NULL,
  FOREIGN KEY (student_id) REFERENCES students(student_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id)
);


CREATE TABLE attendance (
  attendance_id INT PRIMARY KEY,
  date DATE NOT NULL,
  time TIME NOT NULL,
  attendance_status VARCHAR(255) NOT NULL
  
  );
  
  
  