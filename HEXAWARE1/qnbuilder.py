import random
import json

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
        # Pick a random subtopic within the selected topic
        subtopic = random.choice(self.topics.get(topic, []))
        
        # Pick a random template for the selected difficulty
        template = random.choice(self.templates.get(difficulty, []))
        
        # Generate the question using the template and subtopic
        question = template.format(subtopic)
        return question

    def generate_mcq(self, topic, difficulty, num_options=4):
        question = self.generate_question(topic, difficulty)
        
        # Generate incorrect answers and one correct answer
        correct_answer = f"Correct answer about {topic}"
        incorrect_answers = [f"Incorrect answer {i}" for i in range(1, num_options)]
        
        # Combine and shuffle answers
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

    def save_question_bank(self, question_bank, filename='question_bank.json'):
        with open(filename, 'w') as file:
            json.dump(question_bank, file, indent=4)
        print(f"Question bank saved to {filename}.")


# Usage
if __name__ == "__main__":
    builder = AutomatedQuestionBuilder()
    
    # Generate a question bank for Python with medium difficulty, 5 questions
    topic = 'Python'
    difficulty = 'medium'
    num_questions = 5
    
    question_bank = builder.build_question_bank(topic, difficulty, num_questions)
    
    # Save the generated question bank to a file
    builder.save_question_bank(question_bank)

    # Print the question bank
    for idx, question in enumerate(question_bank, start=1):
        print(f"Question {idx}: {question['question']}")
        for opt in question['options']:
            print(f"- {opt}")
        print(f"Answer: {question['answer']}\n")
