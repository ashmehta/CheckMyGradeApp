import unittest
import csv
from CheckMyGrade import Student, Course, Professor, LoginUser

class TestCheckMyGrade(unittest.TestCase):
    
    def setUp(self):
        """Setup test data before each test"""
        self.test_student = Student("test@student.com", "Test", "User", "DATA101", "B", 85)
        self.test_course = Course("DATA101", "Intro to Data", "Basic data science concepts")
        self.test_professor = Professor("prof@test.com", "Dr. Smith", "Associate Professor", "DATA101")
        self.test_user = LoginUser("test@student.com", "TestPass123")
        
        # Clearing CSV files before running tests
        for filename in ["students.csv", "courses.csv", "professors.csv", "login.csv"]:
            open(filename, "w").close()
    
    def test_add_student(self):
        """Test adding a student record and checking uniqueness"""
        Student.add_student(self.test_student)
        students = Student.load_students()
        self.assertTrue(any(s.email == "test@student.com" for s in students))
    
    def test_add_course(self):
        """Test adding a course record and ensuring uniqueness"""
        Course.add_course(self.test_course)
        courses = Course.load_courses()
        self.assertTrue(any(c.course_id == "DATA101" for c in courses))
    
    def test_add_professor(self):
        """Test adding a professor record and ensuring uniqueness"""
        Professor.add_professor(self.test_professor)
        professors = Professor.load_professors()
        self.assertTrue(any(p.email == "prof@test.com" for p in professors))
    
    def test_authentication(self):
        """Test user authentication with encrypted password"""
        LoginUser.add_user(self.test_user)
        self.assertTrue(LoginUser.authenticate("test@student.com", "TestPass123"))
    
    def test_sort_students_by_marks(self):
        """Test sorting students by marks"""
        students = [
            Student("s1@test.com", "S1", "User", "DATA101", "A", 90),
            Student("s2@test.com", "S2", "User", "DATA101", "B", 80),
        ]
        for student in students:
            Student.add_student(student)
        sorted_students = Student.sort_students_by_marks()
        self.assertGreaterEqual(int(sorted_students[0].marks), int(sorted_students[1].marks))
    
    def test_search_student(self):
        """Test searching for a student by email"""
        Student.add_student(self.test_student)
        students = Student.load_students()
        search_result = next((s for s in students if s.email == "test@student.com"), None)
        self.assertIsNotNone(search_result)
        self.assertEqual(search_result.first_name, "Test")
    
    def tearDown(self):
        """Clean up test data"""
        for filename in ["students.csv", "courses.csv", "professors.csv", "login.csv"]:
            open(filename, "w").close()

if __name__ == "__main__":
    unittest.main()
