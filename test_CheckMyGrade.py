import unittest
import time
import os
from CheckMyGrade import CheckMyGrade, Student, Course, Professor

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

    def test_student_addition_deletion_modification(self):
        """Test adding, deleting, and modifying student records."""
        # Clear existing students
        self.app.students = []

        # Add 1000 students
        for i in range(1000):
            student = Student(f"First{i}", f"Last{i}", f"email{i}@example.com", "DATA200", "A", 90 + i % 10)
            self.app.add_student(student)
        self.assertEqual(len(self.app.students), 1000)

        # Delete a student
        self.app.delete_student("email500@example.com")
        self.assertIsNone(self.app.search_student("email500@example.com"))

        # Modify a student
        student = self.app.search_student("email501@example.com")
        student.update_student_record(first_name="UpdatedFirst", last_name="UpdatedLast")
        updated_student = self.app.search_student("email501@example.com")
        self.assertEqual(updated_student.first_name, "UpdatedFirst")
        self.assertEqual(updated_student.last_name, "UpdatedLast")

    def test_load_and_search_data(self):
        """Test loading data from CSV files and searching for records."""
        # Ensure the students.csv file exists
        if not os.path.exists("students.csv"):
            self.fail("students.csv file does not exist")

        # Load data from CSV files
        self.app.load_data_from_csv("students.csv", "student")
        self.app.load_data_from_csv("courses.csv", "course")
        self.app.load_data_from_csv("professors.csv", "professor")

        # Verify that students were loaded
        self.assertGreater(len(self.app.students), 0)

        # Search for a student and measure time
        start_time = time.time