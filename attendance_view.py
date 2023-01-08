import mysql.connector
import csv

# Connect to the database
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="CollegeClassAttendance"
)

# Create a cursor object
cursor = conn.cursor()

# Execute a query to fetch all the rows from the table
cursor.execute("SELECT * FROM attendance")

# Fetch all the results
results = cursor.fetchall()

# Open a CSV file for writing
with open("mytable.csv", "w", newline="") as csvfile:
  # Create a CSV writer object
  writer = csv.writer(csvfile)

  # Write the column names
  writer.writerow([i[0] for i in cursor.description])

  # Write the rows
  writer.writerows(results)

# Print a message
print("Table exported to attendance.csv.")

# Close the connection to the database
conn.close()
