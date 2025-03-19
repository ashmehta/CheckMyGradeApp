# check_my_grade.py
import csv
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

    def update_student_record(self, first_name=None, last_name=None, course_id=None, grades=None, marks=None):
        """Update student details."""
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
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
        """Authenticate user by comparing decrypted password."""
        return self.cipher.decrypt(self.password) == entered_password

    def change_password(self, new_password):
        """Change the password and encrypt it."""
        self.password = self.cipher.encrypt(new_password)


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

    def delete_student(self, email):
        """Delete a student by email."""
        self.students = [s for s in self.students if s.email_address != email]

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
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if data_type == "student":
                    student = Student(row['First_name'], row['Last_name'], row['Email_address'], row['Course_id'], row['Grades'], int(row['Marks']))
                    self.add_student(student)
                elif data_type == "course":
                    course = Course(row['Course_id'], row['Course_name'], row['Credits'], row['Description'])
                    self.courses.append(course)
                elif data_type == "professor":
                    professor = Professor(row['Professor_id'], row['Professor_Name'], row['Rank'], row['Course_id'])
                    self.professors.append(professor)
                elif data_type == "login":
                    login_user = LoginUser(row['User_id'], row['Password'], row['Role'])
                    self.login_users.append(login_user)

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

# Main Function to Run the Application
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
        print("8. Save Data to CSV")
        print("9. Exit")

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
            # Save Data to CSV
            app.save_data_to_csv("students_updated.csv", "student")
            app.save_data_to_csv("courses_updated.csv", "course")
            app.save_data_to_csv("professors_updated.csv", "professor")
            app.save_data_to_csv("login_updated.csv", "login")
            print("Data saved to CSV files successfully!")

        elif choice == "9":
            # Exit
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


# Run the Application
if __name__ == "__main__":
    main()