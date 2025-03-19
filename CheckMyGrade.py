import csv
import os
from encdyc import TextSecurity  # Import the TextSecurity class from encdyc.py

# Student Class
class Student:
    def __init__(self, first_name, last_name, email_address, course_id, grades, marks):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.course_id = course_id
        self.grades = grades
        self.marks = marks

    def display_records(self):
        """Display student details."""
        print(f"Name: {self.first_name} {self.last_name}")
        print(f"Email: {self.email_address}")
        print(f"Course ID: {self.course_id}")
        print(f"Grades: {self.grades}")
        print(f"Marks: {self.marks}")

    def update_student_record(self, first_name=None, last_name=None, email_address=None, course_id=None, grades=None, marks=None):
        """Update student details."""
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email_address:
            self.email_address = email_address
        if course_id:
            self.course_id = course_id
        if grades:
            self.grades = grades
        if marks:
            self.marks = marks


# Course Class
class Course:
    def __init__(self, course_id, course_name, credits, description):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.description = description

    def display_courses(self):
        """Display course details."""
        print(f"Course ID: {self.course_id}")
        print(f"Course Name: {self.course_name}")
        print(f"Credits: {self.credits}")
        print(f"Description: {self.description}")


# Professor Class
class Professor:
    def __init__(self, professor_id, name, email_address, rank, course_id):
        self.professor_id = professor_id
        self.name = name
        self.email_address = email_address
        self.rank = rank
        self.course_id = course_id

    def professors_details(self):
        """Display professor details."""
        print(f"Professor ID: {self.professor_id}")
        print(f"Name: {self.name}")
        print(f"Email: {self.email_address}")
        print(f"Rank: {self.rank}")
        print(f"Course ID: {self.course_id}")


# LoginUser Class
class LoginUser:
    def __init__(self, email_id, password, role):
        self.email_id = email_id
        self.cipher = TextSecurity(4)  # Use a shift of 4 for encryption
        self.password = self.cipher.encrypt(password)  # Encrypt password
        self.role = role

    def login(self, entered_password):
        """Authenticate user by comparing encrypted passwords."""
        # Encrypt the entered password
        encrypted_entered_password = self.cipher.encrypt(entered_password)
        # Compare the encrypted passwords
        return self.password == encrypted_entered_password
    def change_password(self, new_password):
        """Change the password and encrypt it."""
        self.password = self.cipher.encrypt(new_password)
    def add_login_user(self, email_id, password, role):
        """Add a new login user."""
        login_user = LoginUser(email_id, password, role)
        self.login_users.append(login_user)
        self.save_all_data()  # Save data to CSV files


# Main Application Class
class CheckMyGrade:
    def __init__(self):
        self.students = []  # List to store student objects
        self.courses = []   # List to store course objects
        self.professors = []  # List to store professor objects
        self.login_users = []  # List to store login users

    def add_student(self, student):
        """Add a new student."""
        self.students.append(student)
        self.save_all_data()  # Save data to CSV files

    def delete_student(self, email):
        """Delete a student by email."""
        self.students = [s for s in self.students if s.email_address != email]
        self.save_all_data()  # Save data to CSV files

    def search_student(self, email):
        """Search for a student by email."""
        for student in self.students:
            if student.email_address == email:
                return student
        return None

    def sort_students_by_name(self):
        """Sort students by name."""
        return sorted(self.students, key=lambda x: x.first_name)

    def sort_students_by_marks(self):
        """Sort students by marks."""
        return sorted(self.students, key=lambda x: x.marks, reverse=True)

    def calculate_average_marks(self):
        """Calculate average marks of all students."""
        total_marks = sum(student.marks for student in self.students)
        return total_marks / len(self.students)

    def calculate_median_marks(self):
        """Calculate median marks of all students."""
        marks = sorted([student.marks for student in self.students])
        n = len(marks)
        mid = n // 2
        if n % 2 == 0:
            return (marks[mid - 1] + marks[mid]) / 2
        else:
            return marks[mid]

    def load_data_from_csv(self, filename, data_type):
        """Load data from CSV file."""
        try:
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if data_type == "student":
                        student = Student(
                            row['First_name'],
                            row['Last_name'],
                            row['Email_address'],
                            row['Course_id'],
                            row['Grades'],
                            int(row['Marks'])
                        )
                        self.students.append(student)
                    elif data_type == "course":
                        course = Course(
                            row['Course_id'],
                            row['Course_name'],
                            row['Credits'],
                            row['Description']
                        )
                        self.courses.append(course)
                    elif data_type == "professor":
                        professor = Professor(
                            row['Professor_id'],
                            row['Professor_Name'],
                            row['Rank'],
                            row['Course_id']
                        )
                        self.professors.append(professor)
                    elif data_type == "login":
                        login_user = LoginUser(
                            row['User_id'],
                            row['Password'],
                            row['Role']
                        )
                        self.login_users.append(login_user)
        except FileNotFoundError:
            print(f"Error: {filename} not found. Creating a new file.")
            # Create an empty CSV file with headers
            with open(filename, mode='w', newline='') as file:
                if data_type == "student":
                    writer = csv.writer(file)
                    writer.writerow(['Email_address', 'First_name', 'Last_name', 'Course_id', 'Grades', 'Marks'])
                elif data_type == "course":
                    writer = csv.writer(file)
                    writer.writerow(['Course_id', 'Course_name', 'Credits', 'Description'])
                elif data_type == "professor":
                    writer = csv.writer(file)
                    writer.writerow(['Professor_id', 'Professor_Name', 'Rank', 'Course_id'])
                elif data_type == "login":
                    writer = csv.writer(file)
                    writer.writerow(['User_id', 'Password', 'Role'])

    def save_data_to_csv(self, filename, data_type):
        """Save data to CSV file."""
        with open(filename, mode='w', newline='') as file:
            if data_type == "student":
                writer = csv.writer(file)
                writer.writerow(['Email_address', 'First_name', 'Last_name', 'Course_id', 'Grades', 'Marks'])
                for student in self.students:
                    writer.writerow([student.email_address, student.first_name, student.last_name, student.course_id, student.grades, student.marks])
            elif data_type == "course":
                writer = csv.writer(file)
                writer.writerow(['Course_id', 'Course_name', 'Credits', 'Description'])
                for course in self.courses:
                    writer.writerow([course.course_id, course.course_name, course.credits, course.description])
            elif data_type == "professor":
                writer = csv.writer(file)
                writer.writerow(['Professor_id', 'Professor_Name', 'Rank', 'Course_id'])
                for professor in self.professors:
                    writer.writerow([professor.professor_id, professor.name, professor.rank, professor.course_id])
            elif data_type == "login":
                writer = csv.writer(file)
                writer.writerow(['User_id', 'Password', 'Role'])
                for login_user in self.login_users:
                    writer.writerow([login_user.email_id, login_user.password, login_user.role])
    def save_all_data(self):
        """Save all data to CSV files."""
        self.save_data_to_csv("students.csv", "student")
        self.save_data_to_csv("courses.csv", "course")
        self.save_data_to_csv("professors.csv", "professor")
        self.save_data_to_csv("login.csv", "login")


def main():
    app = CheckMyGrade()

    # Load data from CSV files
    app.load_data_from_csv("students.csv", "student")
    app.load_data_from_csv("courses.csv", "course")
    app.load_data_from_csv("professors.csv", "professor")
    app.load_data_from_csv("login.csv", "login")

    while True:
        print("\n--- CheckMyGrade Application ---")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Search Student")
        print("4. Display Students Sorted by Name")
        print("5. Display Students Sorted by Marks")
        print("6. Calculate Average Marks")
        print("7. Calculate Median Marks")
        print("8. Add Course")
        print("9. Delete Course")
        print("10. Add Professor")
        print("11. Delete Professor")
        print("12. Add Login User")
        print("13. Login")
        print("14. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Add Student
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            email_address = input("Enter Email Address: ")
            course_id = input("Enter Course ID: ")
            grades = input("Enter Grades: ")
            marks = int(input("Enter Marks: "))
            student = Student(first_name, last_name, email_address, course_id, grades, marks)
            app.add_student(student)
            print("Student added successfully!")

        elif choice == "2":
            # Delete Student
            email = input("Enter Email Address of the student to delete: ")
            app.delete_student(email)
            print("Student deleted successfully!")

        elif choice == "3":
            # Search Student
            email = input("Enter Email Address of the student to search: ")
            student = app.search_student(email)
            if student:
                student.display_records()
            else:
                print("Student not found!")

        elif choice == "4":
            # Display Students Sorted by Name
            print("\nStudents sorted by name:")
            for student in app.sort_students_by_name():
                student.display_records()

        elif choice == "5":
            # Display Students Sorted by Marks
            print("\nStudents sorted by marks:")
            for student in app.sort_students_by_marks():
                student.display_records()

        elif choice == "6":
            # Calculate Average Marks
            average_marks = app.calculate_average_marks()
            print(f"\nAverage Marks: {average_marks}")

        elif choice == "7":
            # Calculate Median Marks
            median_marks = app.calculate_median_marks()
            print(f"\nMedian Marks: {median_marks}")

        elif choice == "8":
            # Add Course
            course_id = input("Enter Course ID: ")
            course_name = input("Enter Course Name: ")
            credits = input("Enter Credits: ")
            description = input("Enter Description: ")
            course = Course(course_id, course_name, credits, description)
            app.courses.append(course)
            app.save_all_data()
            print("Course added successfully!")

        elif choice == "9":
            # Delete Course
            course_id = input("Enter Course ID to delete: ")
            app.courses = [c for c in app.courses if c.course_id != course_id]
            app.save_all_data()
            print("Course deleted successfully!")

        elif choice == "10":
            # Add Professor
            professor_id = input("Enter Professor ID: ")
            name = input("Enter Professor Name: ")
            email_address = input("Enter Email Address: ")
            rank = input("Enter Rank: ")
            course_id = input("Enter Course ID: ")
            professor = Professor(professor_id, name, email_address, rank, course_id)
            app.professors.append(professor)
            app.save_all_data()
            print("Professor added successfully!")

        elif choice == "11":
            # Delete Professor
            professor_id = input("Enter Professor ID to delete: ")
            app.professors = [p for p in app.professors if p.professor_id != professor_id]
            app.save_all_data()
            print("Professor deleted successfully!")

        elif choice == "12":
            # Add Login User
            email_id = input("Enter Email ID: ")
            password = input("Enter Password: ")
            role = input("Enter Role (student/professor/admin): ")
            login_user = LoginUser(email_id, password, role)
            app.login_users.append(login_user)
            app.save_all_data()
            print("Login user added successfully!")

        elif choice == "13":
            # Login
            email_id = input("Enter Email ID: ")
            password = input("Enter Password: ")
            for user in app.login_users:
                if user.email_id == email_id and user.login(password):
                    print("Login successful!")
                    break
            else:
                print("Invalid email or password.")

        elif choice == "14":
            # Exit
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


# Run the Application
if __name__ == "__main__":
    main()