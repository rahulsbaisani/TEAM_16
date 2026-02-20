# Tuple for student basic details (Application No, Name, Course)
student1 = (1001, "Anu", "BCA")
student2 = (1002, "Ravi", "BSc")

# Dictionary for additional details (Application No as key)
details = {
    1001: {"Age": 19, "City": "Chennai"},
    1002: {"Age": 20, "City": "Bangalore"}
}

# List to store all students
students = [student1, student2]

# Display Student Application Details
for student in students:
    app_no = student[0]
    name = student[1]
    course = student[2]

    print("Application No:", app_no)
    print("Name:", name)
    print("Course:", course)

    # Get additional details from dictionary
    print("Age:", details[app_no]["Age"])
    print("City:", details[app_no]["City"])

    print("------------------------")
