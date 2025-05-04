from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database setup
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  email TEXT UNIQUE,
                  password TEXT,
                  streak INTEGER DEFAULT 0,
                  last_login DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS vocabulary
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  word TEXT,
                  definition TEXT,
                  added_date DATE)''')
    conn.commit()

# User registration
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
                 (email, password))
        conn.commit()
        return redirect('/')
    except:
        return "Email already exists"

# Daily check-in
@app.route('/login', methods=['POST'])
def login():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE email=?", (request.form['email'],))
    user = c.fetchone()
    
    if user and check_password_hash(user[2], request.form['password']):
        today = datetime.now().date()
        last_login = datetime.strptime(user[4], '%Y-%m-%d').date() if user[4] else None
        
        # Update streak if not logged in today
        if last_login != today:
            new_streak = user[3] + 1 if last_login and (today - last_login).days == 1 else 1
            c.execute("UPDATE users SET streak=?, last_login=? WHERE id=?",
                     (new_streak, today, user[0]))
            conn.commit()
        
        session['user_id'] = user[0]
        return redirect('/')
    return "Login failed"

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
