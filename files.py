# Student Application using Dict + List + Tuple

students = []   # List to store multiple students

while True:
    print("\n--- Enter Student Details ---")
    
    name = input("Enter Name: ")
    roll = input("Enter Roll Number: ")
    section = input("Enter Section: ")

    # Tuple for extra fixed details
    extra_details = (
        input("Enter Father's Name: "),
        input("Enter Mother's Name: ")
    )

    # Dictionary for student
    student = {
        "name": name,
        "roll": roll,
        "section": section,
        "extra_details": extra_details
    }

    # Add dictionary to list
    students.append(student)

    choice = input("Add another student? (y/n): ")
    if choice.lower() != 'y':
        break


print("\n========= STORED STUDENT DATA =========")
for s in students:
    print("\nName:", s["name"])
    print("Roll:", s["roll"])
    print("Section:", s["section"])
    print("Father/Mother:", s["extra_details"])
