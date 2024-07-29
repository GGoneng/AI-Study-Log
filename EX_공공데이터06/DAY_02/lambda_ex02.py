class Student:
    def __init__(self, name, grade, number):
        self.name = name
        self.grade = grade
        self.number = number

    def __repr__(self):
        return f"({self.name}, {self.grade}, {self.number})"
    
students = [Student("홍길동", 3.9, 20240303),
            Student("김유신", 3.0, 20240302),
            Student("박문수", 4.3, 20240301)]

print(students[0])

sorted_list = sorted(students, key = lambda s: s.name)
print(sorted_list)

sorted_grade_list = sorted(students, key = lambda s: s.grade)
print(sorted_grade_list)