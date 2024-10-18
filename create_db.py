import sqlite3

# Создаем (или подключаемся к) базу данных
conn = sqlite3.connect('students_rewards.db')
cursor = conn.cursor()

# Создаем таблицу для классов
cursor.execute('''
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade INTEGER,
    letter TEXT
)
''')

# Создаем таблицу для учеников
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    class_id INTEGER,
    FOREIGN KEY(class_id) REFERENCES classes(id)
)
''')

# Создаем таблицу для поощрений
cursor.execute('''
CREATE TABLE IF NOT EXISTS rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    type TEXT,
    points INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id)
)
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных и таблицы успешно созданы!")
