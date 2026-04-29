from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT,
            answer TEXT
        )
    ''')

    cur.execute("SELECT COUNT(*) FROM questions")
    if cur.fetchone()[0] == 0:
        sample_questions = [
            ("Capital of India?", "Delhi", "Mumbai", "Chennai", "Hyderabad", "Delhi"),
            ("Brain of computer?", "ROM", "RAM", "Mouse", "CPU", "CPU"),
            ("10 + 5?", "12", "15", "20", "25", "15"),
            ("Python is?", "Language", "Game", "Car", "Animal", "Language"),
            ("HTML stands for?", "Markup", "Machine", "Code", "Logic", "Markup"),
            ("CSS used for?", "Styling", "Logic", "DB", "Server", "Styling"),
            ("5 * 3?", "15", "10", "20", "8", "15"),
            ("RAM is?", "Memory", "CPU", "Disk", "GPU", "Memory"),
            ("Sun is?", "Star", "Planet", "Moon", "Galaxy", "Star"),
            ("India currency?", "Rupee", "Dollar", "Euro", "Yen", "Rupee"),
            ("Largest planet?", "Earth", "Mars", "Jupiter", "Venus", "Jupiter"),
            ("Water formula?", "H2O", "CO2", "O2", "NaCl", "H2O")
        ]

        cur.executemany('''
            INSERT INTO questions 
            (question, option1, option2, option3, option4, answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_questions)

    conn.commit()
    conn.close()

init_db()

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz')
def quiz():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 10")
    questions = cur.fetchall()

    conn.close()
    return render_template('quiz.html', questions=questions)

@app.route('/result', methods=['POST'])
def result():
    score = 0
    total = 0

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT id, answer FROM questions")
    correct_answers = cur.fetchall()

    conn.close()

    for q_id, real_ans in correct_answers:
        user_ans = request.form.get(str(q_id))

        if user_ans is not None:
            total += 1
            if user_ans == real_ans:
                score += 1

    return render_template('result.html', score=score, total=total)

if __name__ == "__main__":
    app.run(debug=True)