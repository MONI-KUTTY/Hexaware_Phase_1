from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import json
import random

app = Flask(__name__)
app.secret_key = "supersecretadminkey"
app.config['UPLOAD_FOLDER'] = 'uploads'


# Simulated user database for admin management
users = [
    {'username': 'admin', 'role': 'admin'},
    {'username': 'trainer', 'role': 'trainer'},
    {'username': 'employee', 'role': 'employee'}
]

# Simulated system metrics and logs for admin monitoring
system_metrics = {
    'cpu_usage': '15%',
    'memory_usage': '45%',
    'question_banks_generated': 34
}
system_logs = ["System initialized", "User admin logged in", "Question bank generated"]


class AutomatedQuestionBuilder:
    def __init__(self):
        self.topics = {
            'Python': ['variables', 'loops', 'functions', 'data structures'],
            'JavaScript': ['DOM manipulation', 'event handling', 'promises', 'ES6 features'],
            'Data Science': ['pandas', 'numpy', 'data visualization', 'machine learning'],
            'Web Development': ['HTML', 'CSS', 'React', 'Bootstrap']
        }
        
        self.templates = {
            'easy': ["What is {}?", "Explain {} in simple terms.", "Define {}."],
            'medium': ["How does {} work?", "Give an example of {}.", "What are the benefits of using {}?"],
            'hard': ["Explain the underlying concepts of {}.", "Discuss the pros and cons of {}.", "How can you optimize {}?"]
        }

    def generate_question(self, topic, difficulty):
        subtopic = random.choice(self.topics.get(topic, []))
        template = random.choice(self.templates.get(difficulty, []))
        question = template.format(subtopic)
        return question

    def generate_mcq(self, topic, difficulty, num_options=4):
        question = self.generate_question(topic, difficulty)
        correct_answer = f"Correct answer about {topic}"
        incorrect_answers = [f"Incorrect answer {i}" for i in range(1, num_options)]
        options = [correct_answer] + incorrect_answers[:num_options-1]
        random.shuffle(options)
        return {
            'question': question,
            'options': options,
            'answer': correct_answer
        }

    def build_question_bank(self, topic, difficulty, num_questions):
        question_bank = []
        for _ in range(num_questions):
            question_data = self.generate_mcq(topic, difficulty)
            question_bank.append(question_data)
        return question_bank

    def save_question_bank(self, question_bank, filename):
        with open(filename, 'w') as file:
            json.dump(question_bank, file, indent=4)
        return filename


# Admin Route: Dashboard
@app.route('/admin')
def admin_dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        flash("You must be logged in as an admin to access this page.")
        return redirect(url_for('admin_login'))
    return render_template('admin_dashboard.html', metrics=system_metrics, logs=system_logs)


# Admin Route: User Management
@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    if 'username' not in session or session.get('role') != 'admin':
        flash("You must be logged in as an admin to access this page.")
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        # Handle adding a new user
        username = request.form['username']
        role = request.form['role']
        users.append({'username': username, 'role': role})
        flash(f"User {username} added successfully.")

    return render_template('admin_users.html', users=users)


@app.route('/admin/delete_user/<username>')
def delete_user(username):
    global users
    if 'username' not in session or session.get('role') != 'admin':
        flash("You must be logged in as an admin to access this page.")
        return redirect(url_for('admin_login'))

    users = [user for user in users if user['username'] != username]
    flash(f"User {username} removed successfully.")
    return redirect(url_for('admin_users'))


# Admin Route: Generate Reports
@app.route('/admin/reports')
def admin_reports():
    if 'username' not in session or session.get('role') != 'admin':
        flash("You must be logged in as an admin to access this page.")
        return redirect(url_for('admin_login'))
    
    # Simulate report generation
    report = {
        "Total Users": len(users),
        "Total Question Banks Generated": system_metrics['question_banks_generated'],
        "CPU Usage": system_metrics['cpu_usage'],
        "Memory Usage": system_metrics['memory_usage']
    }
    return render_template('admin_reports.html', report=report)


# Admin Route: Issue Resolution (Placeholder)
@app.route('/admin/issues')
def admin_issues():
    if 'username' not in session or session.get('role') != 'admin':
        flash("You must be logged in as an admin to access this page.")
        return redirect(url_for('admin_login'))

    # Placeholder for issue resolution functionality
    return render_template('admin_issues.html')


# Admin Route: Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Dummy login validation
        if username == 'admin' and password == 'adminpass':
            session['username'] = 'admin'
            session['role'] = 'admin'
            flash("Logged in successfully.")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials. Please try again.")

    return render_template('admin_login.html')


# Admin Route: Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('username', None)
    session.pop('role', None)
    flash("Logged out successfully.")
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True)
