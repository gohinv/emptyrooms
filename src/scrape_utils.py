import requests
import datetime
import xml.etree.ElementTree as ET

def get_root(url):
    if "xml" not in url:
        return None
    response = requests.get(url)
    xml_data = response.text
    root = ET.fromstring(xml_data)
    return root

def get_time(time_str):
    # print(time_str)
    if time_str == "ARRANGED":
        return 0
    time_part, meridiem = time_str.split(" ")
    hour_str, minute_str = time_part.split(":")

    hour = int(hour_str)
    minute = int(minute_str)
    
    if meridiem == "PM" and hour != 12:
        hour += 12
    elif meridiem == "AM" and hour == 12:
        hour = 0
    return hour * 100 + minute

def populate_subj(subj_url):
    root = get_root(subj_url)
    if root is None:
        return []
    # print(root.find('courses')[0].attrib)
    courses = root.find('courses')
    num_courses = len(courses)
    courses_urls = [courses[i].attrib['href'] for i in range(num_courses)]
    subj_data = []

    for course_url in courses_urls:
        course_data = populate_course(course_url)
        subj_data.extend(course_data)
    
    return subj_data

def populate_course(course_url):
    root = get_root(course_url)
    if root is None:
        return []
    sections = root.find('sections')
    num_sections = len(sections)
    sections_urls = [sections[i].attrib['href'] for i in range(num_sections)]
    course_data = []

    for section_url in sections_urls:
        print(section_url)
        section_data = populate_section(section_url)
        course_data.append(section_data)

    return course_data

def populate_section(section_url):
    root = get_root(section_url)
    if root is None:
        return ("none", "none", "none", 0, 0, "none", "none")
    subject = root.find('parents').find('subject').attrib['id']
    course_num = root.find('parents').find('course').attrib['id']
    section_type = root.find('meetings').find('meeting').find('type').attrib['code']
    if section_type == 'ONL':
        days = "none"
        start = 0
        end = 0
        building = "none"
        room_number = "none"
    else:
        days = root.find('meetings').find('meeting').find('daysOfTheWeek').text if root.find('meetings').find('meeting').find('daysOfTheWeek') is not None else "none"
        start = get_time(root.find('meetings').find('meeting').find('start').text) if root.find('meetings').find('meeting').find('start') is not None else 0
        end = get_time(root.find('meetings').find('meeting').find('end').text) if root.find('meetings').find('meeting').find('end') is not None else 0
        building = root.find('meetings').find('meeting').find('buildingName').text if root.find('meetings').find('meeting').find('buildingName') is not None else "none"
        room_number = root.find('meetings').find('meeting').find('roomNumber').text if root.find('meetings').find('meeting').find('roomNumber') is not None else "none"

    return (subject, course_num, days, start, end, building, room_number)

    