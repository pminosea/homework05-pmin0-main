#Average Score
#https://www.codechef.com/practice/course/python/LPPYAS06/problems/LPYAS60B

grades_input = input("Type your grades separated by spaces")
grades_list = grades_input.split()
grades_float = list(map(float, grades_list))
print("Here are your grades", (grades_float))
sum_grades = sum(grades_float)
print(sum_grades)
average_grades = sum_grades/3
print(average_grades)

