from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import random
import os
import json

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = 'uploads'


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


@app.route('/')
def index():
    topics = ['Python', 'JavaScript', 'Data Science', 'Web Development']
    difficulties = ['easy', 'medium', 'hard']
    return render_template('index.html', topics=topics, difficulties=difficulties)


@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form.get('topic')
    difficulty = request.form.get('difficulty')
    num_questions = int(request.form.get('num_questions'))
    
    builder = AutomatedQuestionBuilder()
    question_bank = builder.build_question_bank(topic, difficulty, num_questions)
    
    filename = os.path.join(app.config['UPLOAD_FOLDER'], f'question_bank_{topic}_{difficulty}.json')
    builder.save_question_bank(question_bank, filename)
    
    return jsonify({"message": "Question bank generated!", "filename": filename, "question_bank": question_bank})


@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return jsonify({"message": "Download initiated", "filename": filepath})
    else:
        return jsonify({"error": "File not found!"}), 404


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
