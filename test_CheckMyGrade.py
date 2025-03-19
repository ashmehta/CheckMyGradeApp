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
        start_time = time.time()
        student = self.app.search_student("email1@example.com")
        end_time = time.time()
        self.assertIsNotNone(student)
        print(f"\nTime taken to search for a student: {end_time - start_time:.6f} seconds")

    def test_sort_students(self):
        """Test sorting student records by marks and email address."""
        # Add some students for sorting
        self.app.students = [
            Student("First1", "Last1", "email1@example.com", "DATA200", "A", 95),
            Student("First2", "Last2", "email2@example.com", "DATA200", "B", 85),
            Student("First3", "Last3", "email3@example.com", "DATA200", "C", 75),
        ]

        # Sort by marks (descending)
        start_time = time.time()
        sorted_by_marks = self.app.sort_students_by_marks()
        end_time = time.time()
        self.assertEqual(sorted_by_marks[0].marks, 95)  # Highest marks should be first
        print(f"\nTime taken to sort students by marks: {end_time - start_time:.6f} seconds")

        # Sort by email address (ascending)
        start_time = time.time()
        sorted_by_email = sorted(self.app.students, key=lambda x: x.email_address)
        end_time = time.time()
        self.assertEqual(sorted_by_email[0].email_address, "email1@example.com")  # First email alphabetically
        print(f"\nTime taken to sort students by email: {end_time - start_time:.6f} seconds")

    def test_course_management(self):
        """Test adding, deleting, and modifying courses."""
        # Add a course
        course = Course("DATA300", "Advanced Data Science", 3, "Advanced topics in data science")
        self.app.courses.append(course)
        self.assertEqual(len(self.app.courses), 1)

        # Modify a course
        course.course_name = "Updated Course Name"
        self.assertEqual(self.app.courses[0].course_name, "Updated Course Name")

        # Delete a course
        self.app.courses = [c for c in self.app.courses if c.course_id != "DATA300"]
        self.assertEqual(len(self.app.courses), 0)

    def test_professor_management(self):
        """Test adding, deleting, and modifying professors."""
        # Add a professor
        professor = Professor("prof1@example.com", "John Doe", "john@example.com", "Senior Professor", "DATA200")
        self.app.professors.append(professor)
        self.assertEqual(len(self.app.professors), 1)

        # Modify a professor
        professor.name = "Updated Name"
        self.assertEqual(self.app.professors[0].name, "Updated Name")

        # Delete a professor
        self.app.professors = [p for p in self.app.professors if p.professor_id != "prof1@example.com"]
        self.assertEqual(len(self.app.professors), 0)

if __name__ == "__main__":
    unittest.main()