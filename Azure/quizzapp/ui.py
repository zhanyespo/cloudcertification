import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Default file path
        self.default_file_path = "data/Enhanced_Question_Bank_with_Unique_Answers.csv"
        self.file_path = self.default_file_path

        # Variables
        self.questions = []
        self.current_question_index = -1
        self.current_question = None
        self.score = 0
        self.total_questions = 0
        self.incorrect_questions = []

        # UI Elements
        self.change_file_button = tk.Button(
            root, text="Change Question Bank", font=("Arial", 10, "bold"), command=self.select_file
        )
        self.change_file_button.pack(pady=10)

        self.stats_label = tk.Label(
            root,
            text=f"Total Questions: 0 | Correct: 0 | Wrong: 0",
            font=("Arial", 10, "bold"),
        )
        self.stats_label.pack(pady=5)

        self.question_label = tk.Label(
            root, text="", wraplength=580, font=("Arial", 12, "bold"), justify="center"
        )
        self.question_label.pack(pady=10)

        self.ok_button = tk.Button(
            root,
            text="OK",
            font=("Arial", 10, "bold"),
            command=self.load_next_question,
            state="disabled",
        )
        self.ok_button.pack(pady=10)

        self.options_frame = tk.Frame(root)
        self.options_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(4):  # Assume 4 answer choices per question
            btn = tk.Button(
                self.options_frame,
                text="",
                width=70,
                height=2,
                font=("Arial", 10),
                wraplength=580,
                anchor="w",
                justify="left",
                command=lambda i=i: self.check_answer(i),
            )
            btn.grid(row=i, column=0, pady=5, padx=10)
            self.option_buttons.append(btn)

        self.result_label = tk.Label(
            root, text="", wraplength=580, font=("Arial", 10, "italic"), fg="green", justify="left"
        )
        self.result_label.pack(pady=10)

        # Load default question bank
        self.load_default_questions()

    def load_default_questions(self):
        """Load the default question bank."""
        try:
            self.questions = self.load_questions(self.default_file_path)
            self.total_questions = len(self.questions)
            self.stats_label.config(
                text=f"Total Questions: {self.total_questions} | Correct: 0 | Wrong: 0"
            )
            self.load_next_question()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load default questions: {e}")

    def select_file(self):
        """Open a file dialog to select the question bank CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select Question Bank File",
            filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
        )

        if not file_path:
            messagebox.showerror("Error", "No file selected!")
            return

        try:
            self.questions = self.load_questions(file_path)
            self.total_questions = len(self.questions)
            self.file_path = file_path  # Update the current file path
            self.stats_label.config(
                text=f"Total Questions: {self.total_questions} | Correct: 0 | Wrong: 0"
            )
            self.load_next_question()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {e}")

    def load_questions(self, file_path):
        """Load questions from the selected CSV file."""
        df = pd.read_csv(file_path)
        questions = []
        for _, row in df.iterrows():
            question_data = {
                "Question Number": row["QuestionNumber"],
                "Question": row["FinalQuestion"],
                "Answer Options": row["GeneratedAnswerOptions"].split(", ") if pd.notna(row["GeneratedAnswerOptions"]) else ["No options available"],
                "Correct Answer & Explanation": f"{row['CorrectAnswer']} - {row['Explanation']}"
            }
            questions.append(question_data)
        return questions

    def load_next_question(self):
        """Load a new question and reset UI elements."""
        self.result_label.config(text="")
        self.ok_button.config(state="disabled")

        if self.current_question_index < self.total_questions - 1:
            self.current_question_index += 1
            self.current_question = self.questions[self.current_question_index]
        elif self.incorrect_questions:
            # Reattempt incorrect questions
            self.questions = self.incorrect_questions
            self.incorrect_questions = []
            self.current_question_index = 0
            self.current_question = self.questions[self.current_question_index]
            self.total_questions = len(self.questions)
        else:
            self.show_final_score()
            return

        self.question_label.config(text=self.current_question["Question"])

        # Display answer options
        options = self.current_question["Answer Options"]
        for i, btn in enumerate(self.option_buttons):
            if i < len(options):
                btn.config(text=options[i], state="normal")
            else:
                btn.config(text="", state="disabled")

    def check_answer(self, index):
        """Check the selected answer and display the correct answer below."""
        selected_answer = self.option_buttons[index].cget("text")
        correct_answer = self.current_question["Correct Answer & Explanation"]

        for btn in self.option_buttons:
            btn.config(state="disabled")

        if selected_answer.strip().lower() in correct_answer.lower():
            self.result_label.config(text="Correct! Well done!", fg="green")
            self.score += 1
        else:
            self.result_label.config(
                text=f"Wrong! Correct Answer: {correct_answer}",
                fg="red"
            )
            self.incorrect_questions.append(self.current_question)

        self.update_stats()
        self.ok_button.config(state="normal")  # Enable the OK button after answering

    def update_stats(self):
        """Update the stats label with the latest score."""
        wrong_count = len(self.incorrect_questions)
        correct_count = self.score
        self.stats_label.config(
            text=f"Total Questions: {self.total_questions} | Correct: {correct_count} | Wrong: {wrong_count}"
        )

    def show_final_score(self):
        """Display the final score and exit the application."""
        self.question_label.config(
            text=f"Quiz Completed! Your Score: {self.score}/{self.total_questions}"
        )
        self.options_frame.pack_forget()
        self.result_label.pack_forget()
        self.ok_button.config(text="Exit", command=self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
