from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Complete CORS configuration
CORS(app,
     resources={r"/api/*": {"origins": "http://localhost:8080"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Handle preflight requests
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({'status': 'OK'})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Database setup
def init_db():
    conn = sqlite3.connect('quiz_master.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        qualification TEXT,
        dob TEXT,
        role TEXT DEFAULT 'user'
    )''')
    
    # Subjects table
    c.execute('''CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )''')
    
    # Chapters table
    c.execute('''CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (subject_id) REFERENCES subjects (id)
    )''')
    
    # Quizzes table
    c.execute('''CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chapter_id INTEGER,
        name TEXT NOT NULL,
        date_of_quiz TEXT,
        time_duration INTEGER,
        remarks TEXT,
        FOREIGN KEY (chapter_id) REFERENCES chapters (id)
    )''')
    
    # Questions table
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        question_statement TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        correct_option INTEGER NOT NULL,
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
    )''')
    
    # Scores table
    c.execute('''CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER,
        user_id INTEGER,
        time_stamp TEXT,
        total_scored INTEGER,
        total_questions INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quizzes (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Create default admin user
    admin_password = hashlib.md5('admin123'.encode()).hexdigest()
    c.execute('INSERT OR IGNORE INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)',
              ('admin@quizmaster.com', admin_password, 'Quiz Master Admin', 'admin'))
    
    conn.commit()
    conn.close()

# Helper function to get db connection
def get_db():
    conn = sqlite3.connect('quiz_master.db')
    conn.row_factory = sqlite3.Row
    return conn

# Authentication endpoints
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = hashlib.md5(data.get('password').encode()).hexdigest()
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                       (username, password)).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user['id']
        session['role'] = user['role']
        return jsonify({
            'success': True, 
            'user': {
                'id': user['id'],
                'username': user['username'],
                'full_name': user['full_name'],
                'role': user['role']
            }
        })
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = hashlib.md5(data.get('password').encode()).hexdigest()
    full_name = data.get('full_name')
    qualification = data.get('qualification', '')
    dob = data.get('dob', '')
    
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (username, password, full_name, qualification, dob) VALUES (?, ?, ?, ?, ?)',
                    (username, password, full_name, qualification, dob))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'User registered successfully'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Username already exists'}), 400

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# Subject endpoints
@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    conn = get_db()
    subjects = conn.execute('SELECT * FROM subjects').fetchall()
    conn.close()
    return jsonify([dict(subject) for subject in subjects])

@app.route('/api/subjects', methods=['POST'])
def create_subject():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    conn = get_db()
    conn.execute('INSERT INTO subjects (name, description) VALUES (?, ?)',
                (data['name'], data.get('description', '')))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# Chapter endpoints
@app.route('/api/subjects/<int:subject_id>/chapters', methods=['GET'])
def get_chapters(subject_id):
    conn = get_db()
    chapters = conn.execute('SELECT * FROM chapters WHERE subject_id = ?', (subject_id,)).fetchall()
    conn.close()
    return jsonify([dict(chapter) for chapter in chapters])

@app.route('/api/chapters', methods=['POST'])
def create_chapter():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    conn = get_db()
    conn.execute('INSERT INTO chapters (subject_id, name, description) VALUES (?, ?, ?)',
                (data['subject_id'], data['name'], data.get('description', '')))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# Quiz endpoints
@app.route('/api/chapters/<int:chapter_id>/quizzes', methods=['GET'])
def get_quizzes(chapter_id):
    conn = get_db()
    quizzes = conn.execute('SELECT * FROM quizzes WHERE chapter_id = ?', (chapter_id,)).fetchall()
    conn.close()
    return jsonify([dict(quiz) for quiz in quizzes])

@app.route('/api/quizzes', methods=['POST'])
def create_quiz():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    conn = get_db()
    cursor = conn.execute('INSERT INTO quizzes (chapter_id, name, date_of_quiz, time_duration, remarks) VALUES (?, ?, ?, ?, ?)',
                         (data['chapter_id'], data['name'], data.get('date_of_quiz'), 
                          data.get('time_duration', 30), data.get('remarks', '')))
    quiz_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'quiz_id': quiz_id})

@app.route('/api/quiz/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    conn = get_db()
    quiz = conn.execute('SELECT * FROM quizzes WHERE id = ?', (quiz_id,)).fetchone()
    questions = conn.execute('SELECT id, question_statement, option1, option2, option3, option4 FROM questions WHERE quiz_id = ?', 
                            (quiz_id,)).fetchall()
    conn.close()
    
    return jsonify({
        'quiz': dict(quiz) if quiz else None,
        'questions': [dict(q) for q in questions]
    })

# Question endpoints
@app.route('/api/questions', methods=['POST'])
def create_question():
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    conn = get_db()
    conn.execute('INSERT INTO questions (quiz_id, question_statement, option1, option2, option3, option4, correct_option) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (data['quiz_id'], data['question_statement'], data['option1'], data['option2'], 
                 data['option3'], data['option4'], data['correct_option']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/quiz/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    answers = data.get('answers', {})
    
    conn = get_db()
    questions = conn.execute('SELECT id, correct_option FROM questions WHERE quiz_id = ?', (quiz_id,)).fetchall()
    
    score = 0
    total = len(questions)
    
    for question in questions:
        if str(question['id']) in answers and int(answers[str(question['id'])]) == question['correct_option']:
            score += 1
    
    # Save score
    conn.execute('INSERT INTO scores (quiz_id, user_id, time_stamp, total_scored, total_questions) VALUES (?, ?, ?, ?, ?)',
                (quiz_id, session['user_id'], datetime.now().isoformat(), score, total))
    conn.commit()
    conn.close()
    
    return jsonify({'score': score, 'total': total, 'percentage': (score/total)*100 if total > 0 else 0})

# User scores
@app.route('/api/user/scores', methods=['GET'])
def get_user_scores():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db()
    scores = conn.execute('''
        SELECT s.*, q.name as quiz_name, c.name as chapter_name, sub.name as subject_name
        FROM scores s
        JOIN quizzes q ON s.quiz_id = q.id
        JOIN chapters c ON q.chapter_id = c.id
        JOIN subjects sub ON c.subject_id = sub.id
        WHERE s.user_id = ?
        ORDER BY s.time_stamp DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return jsonify([dict(score) for score in scores])

# Serve frontend
@app.route('/')
def serve_frontend():
    with open('../frontend/index.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001, host='0.0.0.0')