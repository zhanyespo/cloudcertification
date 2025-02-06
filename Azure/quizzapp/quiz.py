import pandas as pd
import random

class Quiz:
    def __init__(self, file_path):
        self.questions = pd.read_csv(file_path)
        self.current_question = None

    def get_random_question(self):
        """Select a random question from the question bank."""
        self.current_question = self.questions.sample(1).iloc[0]
        return self.current_question["Question"], self.current_question["Answer Options"]

    def check_answer(self, user_answer):
        """Check if the user's answer is correct."""
        correct_answer = self.current_question["Correct Answer & Explanation"].split(".")[0]
        return user_answer.strip().lower() == correct_answer.strip().lower(), self.current_question["Correct Answer & Explanation"]

# Usage example:
if __name__ == "__main__":
    quiz = Quiz("data/structured_question_bank.csv")
    question, options = quiz.get_random_question()
    print(f"Question: {question}")
    print(f"Options:\n{options}")
