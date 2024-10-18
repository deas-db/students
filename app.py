from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = '1qaz!QAZ'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'  # В реальном приложении используйте безопасные пароли

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('students_rewards.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    classes = conn.execute('SELECT * FROM classes').fetchall()
    conn.close()
    return render_template('index.html', classes=classes)

@app.route('/view_classes')
def view_classes():
    conn = get_db_connection()
    classes = conn.execute('SELECT * FROM classes').fetchall()
    conn.close()
    return render_template('view_classes.html', classes=classes)

@app.route('/class/<int:class_id>')
def view_students_by_class(class_id):
    conn = get_db_connection()
    students = conn.execute("""
        SELECT students.first_name, students.last_name 
        FROM students 
        WHERE class_id = ?
    """, (class_id,)).fetchall()
    
    class_info = conn.execute("SELECT grade, letter FROM classes WHERE id = ?", (class_id,)).fetchone()
    conn.close()
    return render_template('view_students_by_class.html', students=students, class_info=class_info)    

@app.route('/add_class', methods=('GET', 'POST'))
def add_class():
    if not session.get('admin_logged_in'):
        flash('Только администратор может добавлять классы.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        grade = request.form['grade']
        letter = request.form['letter']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO classes (grade, letter) VALUES (?, ?)', (grade, letter))
        conn.commit()
        conn.close()
        
        flash('Класс добавлен!')
        return redirect(url_for('index'))

    return render_template('add_class.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Вы успешно вошли как администратор!')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль!')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Вы вышли из системы.')
    return redirect(url_for('index'))   
    
@app.route('/delete_class/<int:class_id>', methods=['POST'])
def delete_class(class_id):
    if not session.get('admin_logged_in'):
        flash('Только администратор может удалять классы.')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    conn.execute('DELETE FROM classes WHERE id = ?', (class_id,))
    conn.commit()
    conn.close()
    
    flash('Класс удален!')
    return redirect(url_for('index'))     


@app.route('/class/<int:class_id>/students', methods=['GET', 'POST'])
def manage_students(class_id):
    if not session.get('admin_logged_in'):
        flash('Только администратор может управлять учениками.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    if request.method == 'POST':
        # Добавление нового ученика
        student_name = request.form['student_name']
        conn.execute('INSERT INTO students (name, class_id) VALUES (?, ?)', (student_name, class_id))
        conn.commit()
        flash(f'Ученик {student_name} добавлен!')

    students = conn.execute('SELECT * FROM students WHERE class_id = ?', (class_id,)).fetchall()
    conn.close()

    return render_template('manage_students.html', class_id=class_id, students=students)

@app.route('/delete_student/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    if not session.get('admin_logged_in'):
        flash('Только администратор может удалять учеников.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()

    flash('Ученик удалён!')
    return redirect(request.referrer)  # Возвращаемся на ту же страницу


@app.route('/class/<int:class_id>')
def class_students(class_id):
    # Получаем информацию о классе из базы данных
    class_info = get_class_by_id(class_id)  # Ваша функция, которая вернёт информацию о классе по его ID
    students = get_students_by_class_id(class_id)  # Функция для получения списка учеников
    return render_template('manage_students.html', students=students, class_info=class_info)
    

    




if __name__ == '__main__':
    app.run(host='172.17.76.237', port=5000, debug=True)