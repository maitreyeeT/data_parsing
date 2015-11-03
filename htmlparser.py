from bs4 import BeautifulSoup
from os import listdir
import os
from os.path import isfile, join
import fnmatch
import shelve
import json


class College:
    def __init__(self, name, college, recognition, address, phone, fax, email, website):
        if name is None:
            name = ''
        if college is None:
            college = ''
        if recognition is None:
            recognition = ''
        if address is None:
            address = ''
        if phone is None:
            phone = ''
        if fax is None:
            fax = ''
        if email is None:
            email = ''
        if website is None:
            website = ''
        self.name = name
        self.college = college
        self.recognition = recognition
        self.address = address
        self.phone = phone
        self.fax = fax
        self.email = email
        self.website = website
        self.courses = []

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Course:
    def __init__(self, college_name, course_title, course_type,
                 course_duration, course_nature, qualifications,
                 brief_details, selection_process, course_branch, no_of_seats):
        if college_name is None:
            college_name = ''
        if course_title is None:
            course_title = ''
        if course_type is None:
            course_type = ''
        if course_duration is None:
            course_duration = ''
        if course_nature is None:
            course_nature = ''
        if qualifications is None:
            qualifications = ''
        if brief_details is None:
            brief_details = ''
        if selection_process is None:
            selection_process = ''
        if course_branch is None:
            selection_process = ''
        if no_of_seats is None:
            no_of_seats = ''

        self.college_name = college_name
        self.course_title = course_title
        self.course_type = course_type
        self.course_duration = course_duration
        self.course_nature = course_nature
        self.qualifications = qualifications
        self.brief_details = brief_details
        self.selection_process = selection_process
        self.course_branch = course_branch
        self.no_of_seats = no_of_seats
        # self.file_name = file_name


def get_colleges(file):
    Colleges = []
    fax = ''
    phone = ''
    address = ''
    email = ''
    website = ''
    soup = BeautifulSoup(open(file).read(), 'html.parser')
    table = soup.body.find('table', attrs={'class': 'text'})
    rows = table.find_all('tr', attrs={'onmouseover': "this.className='pa-row-highlight'"})

    for name in rows:
        td = name.find_all('td')
        collegename = td[0].find('span', attrs={'class': 'text1'}).text
        college = td[0].find('i')
        if college is not None:
            college = college.text.replace('&nbsp;', '')
        recognition = td[0].find('b')
        if recognition is not None and recognition.next_sibling is not None:
            recognition = recognition.next_sibling.replace('&nbsp;', '')

        td2s = td[1].find_all('b')
        for item in td2s:
            if item is not None:
                if item.text.upper().find('ADDRESS') != -1:
                    address = item.next_sibling.replace('&nbsp;', '')

                if item.text.upper().find('TEL') != -1:
                    phone = item.next_sibling.replace('&nbsp;', '')

                if item.text.upper().find('FAX') != -1:
                    fax = item.next_sibling.replace('&nbsp;', '')

                if item.text.upper().find('WEBSITE') != -1:
                    website = item.next_sibling.replace('&nbsp;', '')

                if item.text.upper().find('EMAIL') != -1:
                    email = item.next_sibling.replace('&nbsp;', '')

        Colleges.append(College(collegename, college, recognition, address, phone, fax, email, website))
    return Colleges


def new_write_file(file, colleges):
    json_strs = []
    for college in colleges:
        json_str = college.to_json()
        json_str = json_str.replace('\u00a0', '')
        json_strs.append(json_str)

    i = 0
    len_json_strs = len(json_strs) - 1
    f = open(file, 'w')
    f.write('[')
    for string1 in json_strs:
        f.write(string1)
        if i != len_json_strs:
            f.write(',')
        i += 1

    f.write(']')
    f.close()


def write_file(file, colleges):
    db = shelve.open(file)
    for college in colleges:
        db[college.name] = college
    db.close()


def read_colleges(directoryPath=''):
    Colleges = []
    if directoryPath == '':
        directoryPath = os.getcwd()

    for file in listdir(directoryPath):
        filepath = join(directoryPath, file)
        if isfile(filepath) and fnmatch.fnmatch(filepath, '*.htm'):
            Colleges = Colleges + get_colleges(filepath)
    return Colleges


def get_courses(file):
    Courses = []
    college_name = ''
    course_title = ''
    course_type = ''
    course_duration = ''
    course_nature = ''
    qualifications = ''
    brief_details = ''
    selection_process = ''
    no_of_seats = 0
    course_branch = ''
    html_start = '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>SchoolColleges</title>
/head>

<body>
'''
    html_end = '''
    </body>
    </html>
    '''
    table_end = '''
    </td></tr></table>
    '''
    soup = BeautifulSoup(html_start + open(file).read().replace('</td></tr></table>', '') + table_end + html_end,
                         'html.parser')

    if soup.body is not None:
        table = soup.body.find('table', attrs={'class': 'text'})
    else:
        table = soup.find('table', attrs={'class': 'text'})

    if table is None:
        return Courses

    td_college = table.find('td', attrs={'class': 'text1'})

    if td_college is not None:
        college_name = td_college.text

    rows = soup.find_all('tr', recursive=True)

    for row in rows:

        add_course = False

        if row is None:
            continue
        # td = row.parent.find('b')
        all_block_quotes = row.parent.find_all('b')
        if all_block_quotes is None:
            continue

        for b in all_block_quotes:
            if b is None:
                continue

            if b.text.upper().find('COURSE TYPE') != -1:
                course_type = b.next_sibling.replace('&nbsp;', '')
                course_branch = b.parent.parent.find('span').b.text.replace('&nbsp;', '')

            if b.text.upper().find('NO OF SEATS') != -1:
                no_of_seats = b.next_sibling.replace('&nbsp;', '')

            if b.text.upper().find('COURSE DURATION') != -1:
                course_duration = b.next_sibling.replace('&nbsp;', '')

            if b.text.upper().find('QUALIFICATION REQUIRED') != -1:
                qualifications = b.next_sibling.replace('&nbsp;', '')

            if b.text.upper().find('BRIEF DETAILS') != -1:
                brief_details = b.next_sibling.replace('&nbsp;', '')

            if b.text.upper().find('SELECTION PROCESS') != -1:
                selection_process = b.next_sibling.replace('&nbsp;', '')

            if b.text.upper().find('COURSE NATURE') != -1:
                course_nature = b.next_sibling.replace('&nbsp;', '')

            add_course = any([course_title, course_type,
                              course_duration, course_nature, qualifications,
                              brief_details, selection_process, no_of_seats])

        if add_course:
            Courses.append(Course(college_name, course_title, course_type,
                                  course_duration, course_nature, qualifications,
                                  brief_details, selection_process, course_branch, no_of_seats))
    return Courses


def read_courses(directoryPath=''):
    Courses = []
    if directoryPath == '':
        directoryPath = os.getcwd()
    for file in listdir(directoryPath):
        filepath = join(directoryPath, file)
        if isfile(filepath) and fnmatch.fnmatch(filepath, '*.html'):
            Courses = Courses + get_courses(filepath)
    return Courses


colleges = read_colleges(r'~/college1')
courses = read_courses(r'~/course1')

for college in colleges:
    college_courses = [course for course in courses if course.college_name.upper() == college.name.upper()]
    college.courses = college_courses

new_write_file(r'/home/maitreyee/collegesdb1', colleges)

print('done!!!')
