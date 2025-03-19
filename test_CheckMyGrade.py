import unittest
import os
import csv
import time
from CheckMyGrade import CheckMyGrade, Student, Course, Professor, LoginUser

class TestCheckMyGrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        cls.app = CheckMyGrade()
        # Load initial data from CSV files if they exist
        if os.path.exists("students.csv"):
            cls.app.load_data_from_csv("students.csv", "student")
        if os.path.exists("courses.csv"):
            cls.app.load_data_from_csv("courses.csv", "course")
        if os.path.exists("professors.csv"):
            cls.app.load_data_from_csv("professors.csv", "professor")
        if os.path.exists("login.csv"):
            cls.app.load_data_from_csv("login.csv", "login")

    def setUp(self):
        """Reset the app data before each test."""
        self.app.students = []
        self.app.courses = []
        self.app.professors = []
        self.app.login_users = []

    def test_student_addition_deletion_modification(self):
        """Test adding, deleting, and modifying student records."""
        # Add a student
        student = Student("John", "Doe", "john@example.com", "DATA200", "A", 95)
        self.app.add_student(student)
        self.assertEqual(len(self.app.students), 1)

        # Delete the student
        self.app.delete_student("john@example.com")
        self.assertEqual(len(self.app.students), 0)

        # Modify the student
        student = Student("Jane", "Doe", "jane@example.com", "DATA200", "B", 85)
        self.app.add_student(student)
        student.update_student_record(first_name="UpdatedJane")
        updated_student = self.app.search_student("jane@example.com")
        self.assertEqual(updated_student.first_name, "UpdatedJane")

    def test_load_and_search_data(self):
        """Test loading data from CSV files and searching for records."""
        # Create a temporary students.csv file
        with open("students.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Email_address', 'First_name', 'Last_name', 'Course_id', 'Grades', 'Marks'])
            writer.writerow(['john@example.com', 'John', 'Doe', 'DATA200', 'A', 95])

        # Load data from CSV files
        self.app.load_data_from_csv("students.csv", "student")

        # Verify that students were loaded
        self.assertGreater(len(self.app.students), 0)

        # Search for a student
        student = self.app.search_student("john@example.com")
        self.assertIsNotNone(student)
        self.assertEqual(student.first_name, "John")

    def test_sort_students(self):
        """Test sorting student records by marks and email address, and display run times."""
        # Add students for sorting
        self.app.students = [
            Student("John", "Doe", "john@example.com", "DATA200", "A", 95),
            Student("Jane", "Doe", "jane@example.com", "DATA200", "B", 85),
            Student("Alice", "Smith", "alice@example.com", "DATA200", "C", 75),
        ]

        # Sort by marks (descending) and measure time
        start_time = time.time()
        sorted_by_marks = self.app.sort_students_by_marks()
        marks_sort_time = time.time() - start_time
        print(f"\nTime taken to sort students by marks: {marks_sort_time:.6f} seconds")

        # Verify the sorting by marks
        self.assertEqual(sorted_by_marks[0].marks, 95)
        self.assertEqual(sorted_by_marks[1].marks, 85)
        self.assertEqual(sorted_by_marks[2].marks, 75)

        # Sort by email address (ascending) and measure time
        start_time = time.time()
        sorted_by_email = sorted(self.app.students, key=lambda x: x.email_address)
        email_sort_time = time.time() - start_time
        print(f"Time taken to sort students by email: {email_sort_time:.6f} seconds")

        # Verify the sorting by email
        self.assertEqual(sorted_by_email[0].email_address, "alice@example.com")
        self.assertEqual(sorted_by_email[1].email_address, "jane@example.com")
        self.assertEqual(sorted_by_email[2].email_address, "john@example.com")
    def test_course_management(self):
        """Test adding, deleting, and modifying courses."""
        # Add a course
        course = Course("DATA300", "Advanced Data Science", 3, "Advanced topics in data science")
        self.app.courses.append(course)
        self.assertEqual(len(self.app.courses), 1)

        # Modify the course
        course.course_name = "Updated Course Name"
        self.assertEqual(self.app.courses[0].course_name, "Updated Course Name")

        # Delete the course
        self.app.courses = [c for c in self.app.courses if c.course_id != "DATA300"]
        self.assertEqual(len(self.app.courses), 0)

    def test_professor_management(self):
        """Test adding, deleting, and modifying professors."""
        # Add a professor
        professor = Professor("prof1@example.com", "John Doe", "john@example.com", "Senior Professor", "DATA200")
        self.app.professors.append(professor)
        self.assertEqual(len(self.app.professors), 1)

        # Modify the professor
        professor.name = "Updated Name"
        self.assertEqual(self.app.professors[0].name, "Updated Name")

        # Delete the professor
        self.app.professors = [p for p in self.app.professors if p.professor_id != "prof1@example.com"]
        self.assertEqual(len(self.app.professors), 0)

    def test_login_functionality(self):
        """Test login functionality."""
        # Add a login user
        login_user = LoginUser("user@example.com", "password123", "student")
        self.app.login_users.append(login_user)
        self.app.save_all_data()  # Save data to CSV files

        # Test successful login
        self.assertTrue(login_user.login("password123"), "Login failed with correct password")

        # Test failed login
        self.assertFalse(login_user.login("wrongpassword"), "Login succeeded with incorrect password")
    def test_csv_file_updates(self):
        """Test saving data to CSV files."""
        # Add a student
        student = Student("John", "Doe", "john@example.com", "DATA200", "A", 95)
        self.app.add_student(student)

        # Save data to CSV files
        self.app.save_all_data()

        # Verify that the students.csv file was updated
        with open("students.csv", mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 2)  # Header + 1 student
            self.assertEqual(rows[1], ["john@example.com", "John", "Doe", "DATA200", "A", "95"])

    def tearDown(self):
        """Reset the app data after each test without deleting CSV files."""
        self.app.students = []
        self.app.courses = []
        self.app.professors = []
        self.app.login_users = []

if __name__ == "__main__":
    unittest.main()