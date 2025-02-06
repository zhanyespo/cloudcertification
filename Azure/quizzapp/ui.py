import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random

class QuizApp:
    def __init__(self, root, file_path):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.questions = pd.read_csv(file_path)
        self.current_question = None

        # UI Elements
        self.question_label = tk.Label(root, text="", wraplength=400, font=("Arial", 12, "bold"))
        self.question_label.pack(pady=20)

        self.options_frame = tk.Frame(root)
        self.options_frame.pack()

        self.option_buttons = []
        for i in range(4):  # Assume 4 answer choices per question
            btn = tk.Button(self.options_frame, text="", width=50, height=2, command=lambda i=i: self.check_answer(i))
            btn.grid(row=i, column=0, pady=5)
            self.option_buttons.append(btn)

        self.next_button = tk.Button(root, text="Next Question", command=self.load_question, state="disabled")
        self.next_button.pack(pady=20)

        self.load_question()  # Load first question

    def load_question(self):
        """Load a new random question from the question bank."""
        self.current_question = self.questions.sample(1).iloc[0]
        self.question_label.config(text=self.current_question["Question"])

        options = self.current_question["Answer Options"].split("\n")  # Split multi-line options
        for i, btn in enumerate(self.option_buttons):
            if i < len(options):
                btn.config(text=options[i], state="normal")
            else:
                btn.config(text="", state="disabled")

        self.next_button.config(state="disabled")

    def check_answer(self, index):
        """Check the selected answer and display a message box."""
        selected_answer = self.option_buttons[index].cget("text")
        correct_answer = self.current_question["Correct Answer & Explanation"].split(".")[0]

        if selected_answer.strip().lower() == correct_answer.strip().lower():
            messagebox.showinfo("Correct!", "Well done! That's the right answer!")
        else:
            messagebox.showerror("Wrong!", f"Incorrect. The correct answer is: {correct_answer}")

        for btn in self.option_buttons:
            btn.config(state="disabled")

        self.next_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root, "data/structured_question_bank.csv")
    root.mainloop()
