from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'
DATABASE = 'expense_tracker.db'


# Initialize the database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT NOT NULL,
                        date TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')
    print("Database initialized.")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DATABASE) as conn:
            try:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return "Username already exists!"
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DATABASE) as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
            if user:
                session['username'] = username
                session['user_id'] = user[0]
                return redirect(url_for('dashboard'))
            return "Invalid credentials!"
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    with sqlite3.connect(DATABASE) as conn:
        expenses = conn.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,)).fetchall()

    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)",
                         (user_id, amount, category, date))
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', expenses=expenses)


@app.route('/visualize')
def visualize():
    if 'username' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    with sqlite3.connect(DATABASE) as conn:
        expenses = conn.execute("SELECT category, SUM(amount) FROM expenses WHERE user_id = ? GROUP BY category",
                                (user_id,)).fetchall()

    categories = [row[0] for row in expenses]
    amounts = [row[1] for row in expenses]

    # Create a bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(categories, amounts, color='skyblue')
    plt.title('Spending by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.tight_layout()

    # Save chart to a buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('visualize.html', plot_url=plot_url)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
