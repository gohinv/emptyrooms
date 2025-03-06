import csv
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS database (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        course_num TEXT,
        days TEXT,
        start_time INTEGER,
        end_time INTEGER,
        building TEXT,
        room_number TEXT
    )
''')

with open('../src/all_sections.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        c.execute('''
            INSERT INTO database (subject, course_num, days, start_time, end_time, building, room_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['subject'],
            row['course_num'],
            row['days'],
            row['start'],
            row['end'],
            row['building'],
            row['room_number']
        ))
conn.commit()
conn.close()