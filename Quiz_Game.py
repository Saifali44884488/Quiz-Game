import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime
from pathlib import Path

# Load questions from JSON file
questions_file = Path(__file__).parent / "questions.json"
with open(questions_file, "r") as f:
    questions = json.load(f)

class QuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.q_index = 0
        self.score = 0
        self.time_left = 10
        self.timer_id = None

        # Style config
        self.bg_color = "#1e1e2f"
        self.fg_color = "#ffffff"
        self.button_bg = "#2e86de"
        self.button_hover = "#1b4f72"
        self.root.configure(bg=self.bg_color)
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Title label
        title_label = tk.Label(root, text="🧠 Quiz Challenge", font=("Arial", 18, "bold"),
                               bg=self.bg_color, fg="#f1c40f")
        title_label.pack(pady=10)

        # Frame for question and timer
        top_frame = tk.Frame(root, bg=self.bg_color)
        top_frame.pack(pady=10, fill='x')

        self.question_label = tk.Label(top_frame, text="", font=("Arial", 14),
                                       wraplength=450, justify="center", bg=self.bg_color, fg=self.fg_color)
        self.question_label.pack(side="left", padx=20)

        self.timer_label = tk.Label(top_frame, text="", font=("Arial", 14),
                                    bg=self.bg_color, fg="#e74c3c")
        self.timer_label.pack(side="right", padx=20)

        # Frame for option buttons
        self.buttons_frame = tk.Frame(root, bg=self.bg_color)
        self.buttons_frame.pack(pady=10)

        self.buttons = []
        self.option_labels = ['A', 'B', 'C', 'D']
        for i in range(4):
            btn = tk.Button(self.buttons_frame, text="", font=("Arial", 12),
                            width=50, anchor="center", relief="flat",
                            bg=self.button_bg, fg="white", activebackground=self.button_hover,
                            cursor="hand2", command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=8)
            self.buttons.append(btn)

        self.load_question()

    def load_question(self):
        if self.q_index < len(questions):
            q = questions[self.q_index]
            self.question_label.config(text=f"Q{self.q_index + 1}. {q['question']}")
            for i, option in enumerate(q["options"]):
                option_text = f"{self.option_labels[i]}. {option}"
                self.buttons[i].config(text=option_text)
            self.time_left = 10
            self.update_timer()
        else:
            self.show_result()

    def update_timer(self):
        self.timer_label.config(text=f"⏰ {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_id = None
            self.q_index += 1
            self.load_question()

    def check_answer(self, idx):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        selected_text = self.buttons[idx].cget("text")
        selected = selected_text.split('. ', 1)[1]
        correct = questions[self.q_index]["answer"]
        if selected == correct:
            self.score += 1
        self.q_index += 1
        self.load_question()

    def show_result(self):
        total = len(questions)
        result_text = f"You scored {self.score} out of {total}"
        messagebox.showinfo("Quiz Completed", result_text)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("results.txt", "a") as file:
            file.write(f"{now} - Score: {self.score}/{total}\n")
        self.root.destroy()

# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizGUI(root)
    root.mainloop()
