import fileinput
import glob, os

#dir_path = r"/home/maitreyee/Downloads/SchoolCollege.com/rajasthan_data1/"

file_list = glob.glob("*.txt")
with open('course_2result.txt', 'w') as file:
	input_lines = fileinput.input(file_list)
	file.writelines(input_lines)
