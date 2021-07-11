# import random
#
#
# class Robot:
#
#     def __init__(self, name):
#         self.name = name
#         self.health_level = random.random()
#
#     def say_hi(self):
#         print("Hi, I am " + self.name)
#
#     def need_a_doctor(self):
#         if self.health_level < 0.8:
#             return True
#         else:
#             return False
#
#
# class PhysicianRobot(Robot):
#     def new_method_for_PR(self):
#         pass
#
#     def say_hi(self):
#         super().say_hi()
#         print("and I am a physician!")
#
#     def heal(self, robot):
#         robot.health_level = random.uniform(robot.health_level, 1)
#         print(robot.name + " has been healed by " + self.name + "!")
#
#
# x = Robot("Marvin")
# y = PhysicianRobot("James")
#
# print(x, type(x))
# print(y, type(y))
#
# x.say_hi()
# y.say_hi()
# print()
# print(isinstance(x, Robot), isinstance(y, Robot))
# print(isinstance(x, PhysicianRobot))
# print(isinstance(y, PhysicianRobot))
#
# print(type(y) == Robot, type(y) == PhysicianRobot)
# print()
# doc = PhysicianRobot("Dr. Frankenstein")
# doc.say_hi()
# rob_list = []
# for i in range(5):
#     x = Robot("Marvin" + str(i))
#     if x.need_a_doctor():
#         print("health_level of " + x.name + " before healing: ", x.health_level)
#         doc.heal(x)
#         print("health_level of " + x.name + " after healing: ", x.health_level)
#     rob_list.append((x.name, x.health_level))
#
# print(rob_list)

class Student:
    students = 0

    def __init__(self, name, ta):
        self.name = name
        self.understanding = 0
        Student.students += 1
        print("There are now", Student.students, "students")
        ta.add_student(self)

    def visit_office_hour(self, staff):
        staff.assist(self)
        print("Thanks, " + staff.name)


class Professor:
    def __init__(self, name):
        self.name = name
        self.students = {}

    def add_student(self, student):
        self.students[student.name] = student

    def assist(self, student):
        student.understanding += 1


snape = Professor("Snape")
harry = Student("Harry", snape)
print()
harry.visit_office_hour(snape)
print()
harry.visit_office_hour(Professor("Hagrid"))
print()
print(harry.understanding)
print()
for name in snape.students:
    print(name)
print()
x = Student("Hermonie", Professor("McGonagall")).name
print()
print(x)
print()
for name in snape.students:
    print(name)