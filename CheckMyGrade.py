import csv
from encdyc import TextSecurity


cipher = TextSecurity(4) 


def main():
    while True:
        print("\nCheckMyGrade Application")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Add Professor")
        print("4. Authenticate User")
        print("5. Sort Students by Marks")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            email = input("Enter student email: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            course_id = input("Enter course ID: ")
            grade = input("Enter grade: ")
            marks = input("Enter marks: ")
            Student.add_student(Student(email, first_name, last_name, course_id, grade, marks))
            print("Student added successfully.")
        
        elif choice == "2":
            course_id = input("Enter course ID: ")
            course_name = input("Enter course name: ")
            description = input("Enter course description: ")
            Course.add_course(Course(course_id, course_name, description))
            print("Course added successfully.")
        
        elif choice == "3":
            email = input("Enter professor email: ")
            name = input("Enter professor name: ")
            rank = input("Enter professor rank: ")
            course_id = input("Enter course ID: ")
            Professor.add_professor(Professor(email, name, rank, course_id))
            print("Professor added successfully.")
        
        elif choice == "4":
            email = input("Enter email: ")
            password = input("Enter password: ")
            if LoginUser.authenticate(email, password):
                print("Login successful!")
            else:
                print("Invalid credentials.")
        
        elif choice == "5":
            sorted_students = Student.sort_students_by_marks()
            for student in sorted_students:
                print(f"{student.email} - {student.marks}")
        
        elif choice == "6":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")

class Student:
    def __init__(self, email, first_name, last_name, course_id, grade, marks):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.grade = grade
        self.marks = marks
    
    def to_list(self):
        return [self.email, self.first_name, self.last_name, self.course_id, self.grade, self.marks]

    @staticmethod
    def add_student(student):
        with open("students.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(student.to_list())
    
    @staticmethod
    def load_students():
        students = []
        with open("students.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                students.append(Student(*row))
        return students
    
    @staticmethod
    def sort_students_by_marks():
        students = Student.load_students()
        students.sort(key=lambda x: int(x.marks), reverse=True)
        return students

class Course:
    def __init__(self, course_id, course_name, description):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
    
    def to_list(self):
        return [self.course_id, self.course_name, self.description]
    
    @staticmethod
    def add_course(course):
        with open("courses.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(course.to_list())
    
    @staticmethod
    def load_courses():
        courses = []
        with open("courses.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                courses.append(Course(*row))
        return courses

class Professor:
    def __init__(self, email, name, rank, course_id):
        self.email = email
        self.name = name
        self.rank = rank
        self.course_id = course_id
    
    def to_list(self):
        return [self.email, self.name, self.rank, self.course_id]
    
    @staticmethod
    def add_professor(professor):
        with open("professors.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(professor.to_list())
    
    @staticmethod
    def load_professors():
        professors = []
        with open("professors.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                professors.append(Professor(*row))
        return professors

class LoginUser:
    def __init__(self, email, password):
        self.email = email
        self.password = cipher.encrypt(password)  # Encrypt password
    
    def to_list(self):
        return [self.email, self.password]

    @staticmethod
    def add_user(user):
        with open("login.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(user.to_list())

    @staticmethod
    def authenticate(email, password):
        with open("login.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                stored_email, stored_password = row
                if stored_email == email and cipher.decrypt(stored_password) == password:  # Decrypt for verification
                    return True
        return False

if __name__ == "__main__":
    main()
