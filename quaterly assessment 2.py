import sqlite3

def initialize_database():
    conn = sqlite3.connect('quiz_bowl.db')
    cursor = conn.cursor()
    
    # Create tables for 5 course categories
    courses = [
        "BMGT",
        "DS3850",
        "DS3860",
        "Accounting",
        "History"
    ]
    
    for course in courses:
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {course} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            correct_answer TEXT NOT NULL
        )
        ''')
    
    # Insert sample questions if tables are empty
    for course in courses:
        cursor.execute(f"SELECT COUNT(*) FROM {course}")
        if cursor.fetchone()[0] == 0:
            # Add sample questions (10 per course)
            for i in range(1, 11):
                cursor.execute(f'''
                INSERT INTO {course} (question_text, option1, option2, option3, option4, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    f"Sample question {i} for {course}",
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D",
                    "Option B"  # Sample correct answer
                ))
    
    conn.commit()
    conn.close()

class Question:
    def __init__(self, question_id, question_text, options, correct_answer):
        self.question_id = question_id
        self.question_text = question_text
        self.options = options
        self.correct_answer = correct_answer
    
    def check_answer(self, user_answer):
        return user_answer == self.correct_answer
    
    def display_question(self):
        return {
            "id": self.question_id,
            "text": self.question_text,
            "options": self.options,
            "correct_answer": self.correct_answer
        }

import tkinter as tk
from tkinter import messagebox, ttk

class QuizBowlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Bowl Application")
        self.root.geometry("800x600")
        
        # Initialize database
        initialize_database()
        
        # Admin credentials
        self.admin_password = "admin123"
        
        # Create main menu
        self.show_main_menu()
    
    def show_main_menu(self):
        """Display the main menu with admin and quiz taker options"""
        self.clear_window()
        
        tk.Label(self.root, text="Welcome to Quiz Bowl", font=("Arial", 20)).pack(pady=20)
        
        tk.Button(self.root, text="Administrator Login", 
                 command=self.show_admin_login, width=20).pack(pady=10)
        tk.Button(self.root, text="Take a Quiz", 
                 command=self.show_quiz_category_selection, width=20).pack(pady=10)
        tk.Button(self.root, text="Exit", 
                 command=self.root.quit, width=20).pack(pady=10)
    
    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ... (other methods will be implemented below)

    def show_admin_login(self):
        """Display admin login screen"""
        self.clear_window()
        
        tk.Label(self.root, text="Administrator Login", font=("Arial", 16)).pack(pady=20)
        
        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        
        tk.Button(self.root, text="Login", command=self.verify_admin).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)
    
    def verify_admin(self):
        """Verify admin password"""
        if self.password_entry.get() == self.admin_password:
            self.show_admin_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect password")
    
    def show_admin_dashboard(self):
        """Display admin dashboard with options"""
        self.clear_window()
        
        tk.Label(self.root, text="Administrator Dashboard", font=("Arial", 16)).pack(pady=20)
        
        tk.Button(self.root, text="Add Questions", 
                 command=self.show_add_question, width=20).pack(pady=10)
        tk.Button(self.root, text="View/Edit Questions", 
                 command=self.show_view_questions, width=20).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", 
                 command=self.show_main_menu, width=20).pack(pady=10)
    
    def show_add_question(self):
        """Display form to add new questions"""
        self.clear_window()
        
        tk.Label(self.root, text="Add New Question", font=("Arial", 16)).pack(pady=20)
        
        # Course selection
        tk.Label(self.root, text="Select Course:").pack()
        self.course_var = tk.StringVar()
        courses = ["Computer_Science", "Mathematics", "Physics", "Literature", "History"]
        course_menu = ttk.Combobox(self.root, textvariable=self.course_var, values=courses)
        course_menu.pack(pady=5)
        
        # Question text
        tk.Label(self.root, text="Question Text:").pack()
        self.question_text = tk.Text(self.root, height=4, width=50)
        self.question_text.pack(pady=5)
        
        # Options
        tk.Label(self.root, text="Options:").pack()
        
        tk.Label(self.root, text="Option 1:").pack()
        self.option1 = tk.Entry(self.root, width=50)
        self.option1.pack(pady=2)
        
        tk.Label(self.root, text="Option 2:").pack()
        self.option2 = tk.Entry(self.root, width=50)
        self.option2.pack(pady=2)
        
        tk.Label(self.root, text="Option 3:").pack()
        self.option3 = tk.Entry(self.root, width=50)
        self.option3.pack(pady=2)
        
        tk.Label(self.root, text="Option 4:").pack()
        self.option4 = tk.Entry(self.root, width=50)
        self.option4.pack(pady=2)
        
        # Correct answer
        tk.Label(self.root, text="Correct Answer (1-4):").pack()
        self.correct_answer = tk.Entry(self.root, width=5)
        self.correct_answer.pack(pady=5)
        
        # Buttons
        tk.Button(self.root, text="Submit", command=self.submit_question).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_admin_dashboard).pack(pady=5)
    
    def submit_question(self):
        """Submit new question to database"""
        try:
            course = self.course_var.get()
            question_text = self.question_text.get("1.0", tk.END).strip()
            options = [
                self.option1.get().strip(),
                self.option2.get().strip(),
                self.option3.get().strip(),
                self.option4.get().strip()
            ]
            correct_idx = int(self.correct_answer.get().strip()) - 1
            
            if not all(options) or correct_idx not in range(4):
                raise ValueError("Invalid options or correct answer")
            
            conn = sqlite3.connect('quiz_bowl.db')
            cursor = conn.cursor()
            
            cursor.execute(f'''
            INSERT INTO {course} (question_text, option1, option2, option3, option4, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (question_text, *options, options[correct_idx]))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Question added successfully!")
            self.show_add_question()  # Clear form
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add question: {str(e)}")
    
    def show_view_questions(self):
        """Display interface to view and edit questions"""
        self.clear_window()
        
        tk.Label(self.root, text="View/Edit Questions", font=("Arial", 16)).pack(pady=20)
        
        # Course selection
        tk.Label(self.root, text="Select Course:").pack()
        self.view_course_var = tk.StringVar()
        courses = ["BMGT", "DS3850", "DS3860", "Accounting", "History"]
        course_menu = ttk.Combobox(self.root, textvariable=self.view_course_var, values=courses)
        course_menu.pack(pady=5)
        
        # Button to load questions
        tk.Button(self.root, text="Load Questions", 
                 command=self.load_questions_for_viewing).pack(pady=10)
        
        # Treeview for displaying questions
        self.questions_tree = ttk.Treeview(self.root, columns=("ID", "Question", "Correct Answer"), show="headings")
        self.questions_tree.heading("ID", text="ID")
        self.questions_tree.heading("Question", text="Question")
        self.questions_tree.heading("Correct Answer", text="Correct Answer")
        self.questions_tree.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Buttons for edit/delete
        tk.Button(self.root, text="Edit Selected", 
                 command=self.edit_selected_question).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(self.root, text="Delete Selected", 
                 command=self.delete_selected_question).pack(side=tk.RIGHT, padx=20, pady=10)
        tk.Button(self.root, text="Back", 
                 command=self.show_admin_dashboard).pack(pady=10)
    
    def load_questions_for_viewing(self):
        """Load questions from selected course"""
        course = self.view_course_var.get()
        if not course:
            messagebox.showerror("Error", "Please select a course")
            return
        
        try:
            conn = sqlite3.connect('quiz_bowl.db')
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT id, question_text, correct_answer FROM {course}")
            questions = cursor.fetchall()
            
            # Clear existing items
            for item in self.questions_tree.get_children():
                self.questions_tree.delete(item)
            
            # Add new items
            for q in questions:
                self.questions_tree.insert("", tk.END, values=q)
            
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions: {str(e)}")
    
    def edit_selected_question(self):
        """Edit selected question"""
        selected = self.questions_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a question")
            return
        
        course = self.view_course_var.get()
        if not course:
            messagebox.showerror("Error", "Please select a course")
            return
        
        item = self.questions_tree.item(selected[0])
        question_id = item['values'][0]
        
        # Show edit form (similar to add question form)
        self.show_edit_question(course, question_id)
    
    def show_edit_question(self, course, question_id):
        """Display form to edit existing question"""
        self.clear_window()
        
        tk.Label(self.root, text="Edit Question", font=("Arial", 16)).pack(pady=20)
        
        try:
            conn = sqlite3.connect('quiz_bowl.db')
            cursor = conn.cursor()
            
            cursor.execute(f'''
            SELECT question_text, option1, option2, option3, option4, correct_answer 
            FROM {course} WHERE id = ?
            ''', (question_id,))
            
            question_data = cursor.fetchone()
            conn.close()
            
            if not question_data:
                raise ValueError("Question not found")
            
            # Course display (read-only)
            tk.Label(self.root, text=f"Course: {course}").pack()
            
            # Question text
            tk.Label(self.root, text="Question Text:").pack()
            self.edit_question_text = tk.Text(self.root, height=4, width=50)
            self.edit_question_text.insert(tk.END, question_data[0])
            self.edit_question_text.pack(pady=5)
            
            # Options
            tk.Label(self.root, text="Options:").pack()
            
            tk.Label(self.root, text="Option 1:").pack()
            self.edit_option1 = tk.Entry(self.root, width=50)
            self.edit_option1.insert(0, question_data[1])
            self.edit_option1.pack(pady=2)
            
            tk.Label(self.root, text="Option 2:").pack()
            self.edit_option2 = tk.Entry(self.root, width=50)
            self.edit_option2.insert(0, question_data[2])
            self.edit_option2.pack(pady=2)
            
            tk.Label(self.root, text="Option 3:").pack()
            self.edit_option3 = tk.Entry(self.root, width=50)
            self.edit_option3.insert(0, question_data[3])
            self.edit_option3.pack(pady=2)
            
            tk.Label(self.root, text="Option 4:").pack()
            self.edit_option4 = tk.Entry(self.root, width=50)
            self.edit_option4.insert(0, question_data[4])
            self.edit_option4.pack(pady=2)
            
            # Correct answer
            correct_answer = question_data[5]
            correct_idx = question_data[1:5].index(correct_answer) + 1
            
            tk.Label(self.root, text="Correct Answer (1-4):").pack()
            self.edit_correct_answer = tk.Entry(self.root, width=5)
            self.edit_correct_answer.insert(0, str(correct_idx))
            self.edit_correct_answer.pack(pady=5)
            
            # Buttons
            tk.Button(self.root, text="Update", 
                     command=lambda: self.update_question(course, question_id)).pack(pady=10)
            tk.Button(self.root, text="Cancel", 
                     command=self.show_view_questions).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load question: {str(e)}")
            self.show_view_questions()
    
    def update_question(self, course, question_id):
        """Update question in database"""
        try:
            question_text = self.edit_question_text.get("1.0", tk.END).strip()
            options = [
                self.edit_option1.get().strip(),
                self.edit_option2.get().strip(),
                self.edit_option3.get().strip(),
                self.edit_option4.get().strip()
            ]
            correct_idx = int(self.edit_correct_answer.get().strip()) - 1
            
            if not all(options) or correct_idx not in range(4):
                raise ValueError("Invalid options or correct answer")
            
            conn = sqlite3.connect('quiz_bowl.db')
            cursor = conn.cursor()
            
            cursor.execute(f'''
            UPDATE {course} 
            SET question_text = ?, option1 = ?, option2 = ?, option3 = ?, option4 = ?, correct_answer = ?
            WHERE id = ?
            ''', (question_text, *options, options[correct_idx], question_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Question updated successfully!")
            self.show_view_questions()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update question: {str(e)}")
    
    def delete_selected_question(self):
        """Delete selected question"""
        selected = self.questions_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a question")
            return
        
        course = self.view_course_var.get()
        if not course:
            messagebox.showerror("Error", "Please select a course")
            return
        
        item = self.questions_tree.item(selected[0])
        question_id = item['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this question?"):
            try:
                conn = sqlite3.connect('quiz_bowl.db')
                cursor = conn.cursor()
                
                cursor.execute(f"DELETE FROM {course} WHERE id = ?", (question_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Question deleted successfully!")
                self.load_questions_for_viewing()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete question: {str(e)}")

    def show_quiz_category_selection(self):
        """Display category selection for quiz taker"""
        self.clear_window()
        
        tk.Label(self.root, text="Select Quiz Category", font=("Arial", 16)).pack(pady=20)
        
        courses = ["BMGT", "DS3850", "DS3860", "Accounting", "History"]
        
        for course in courses:
            tk.Button(self.root, text=course.replace("_", " "), 
                     command=lambda c=course: self.start_quiz(c),
                     width=20).pack(pady=5)
        
        tk.Button(self.root, text="Back to Main Menu", 
                 command=self.show_main_menu, width=20).pack(pady=10)
    
    def start_quiz(self, course):
        """Start a quiz for the selected course"""
        try:
            conn = sqlite3.connect('quiz_bowl.db')
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM {course}")
            questions_data = cursor.fetchall()
            conn.close()
            
            if not questions_data:
                messagebox.showerror("Error", "No questions found for this course")
                return
            
            # Convert to Question objects
            self.quiz_questions = []
            for q in questions_data:
                options = [q[2], q[3], q[4], q[5]]  # option1 to option4
                self.quiz_questions.append(Question(q[0], q[1], options, q[6]))
            
            self.current_question_index = 0
            self.score = 0
            self.show_quiz_question()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start quiz: {str(e)}")
    
    def show_quiz_question(self):
        """Display the current quiz question"""
        self.clear_window()
        
        if self.current_question_index >= len(self.quiz_questions):
            self.show_quiz_results()
            return
        
        question = self.quiz_questions[self.current_question_index]
        
        # Question text
        tk.Label(self.root, text=f"Question {self.current_question_index + 1} of {len(self.quiz_questions)}",
                font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=question.question_text, 
                font=("Arial", 14), wraplength=700).pack(pady=10)
        
        # Options
        self.selected_option = tk.StringVar()
        self.selected_option.set(None)  # No option selected initially
        
        for i, option in enumerate(question.options, start=1):
            tk.Radiobutton(self.root, text=option, variable=self.selected_option,
                          value=option, font=("Arial", 12), wraplength=700).pack(anchor=tk.W, padx=20)
        
        # Submit button
        tk.Button(self.root, text="Submit Answer", 
                 command=self.check_quiz_answer, width=20).pack(pady=20)
        
        # Score display
        tk.Label(self.root, text=f"Current Score: {self.score}/{len(self.quiz_questions)}",
                font=("Arial", 12)).pack(pady=10)
    
    def check_quiz_answer(self):
        """Check the submitted answer and provide feedback"""
        if not self.selected_option.get():
            messagebox.showerror("Error", "Please select an answer")
            return
        
        question = self.quiz_questions[self.current_question_index]
        is_correct = question.check_answer(self.selected_option.get())
        
        if is_correct:
            self.score += 1
            messagebox.showinfo("Correct", "Your answer is correct!")
        else:
            messagebox.showerror("Incorrect", 
                               f"Wrong answer. The correct answer is: {question.correct_answer}")
        
        self.current_question_index += 1
        self.show_quiz_question()
    
    def show_quiz_results(self):
        """Display final quiz results"""
        self.clear_window()
        
        tk.Label(self.root, text="Quiz Completed!", font=("Arial", 20)).pack(pady=20)
        tk.Label(self.root, text=f"Your final score: {self.score}/{len(self.quiz_questions)}",
                font=("Arial", 16)).pack(pady=10)
        
        percentage = (self.score / len(self.quiz_questions)) * 100
        tk.Label(self.root, text=f"{percentage:.1f}%", font=("Arial", 14)).pack(pady=5)
        
        # Feedback based on score
        if percentage >= 80:
            feedback = "Excellent work!"
        elif percentage >= 60:
            feedback = "Good job!"
        else:
            feedback = "Keep practicing!"
        
        tk.Label(self.root, text=feedback, font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self.root, text="Take Another Quiz", 
                 command=self.show_quiz_category_selection, width=20).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", 
                 command=self.show_main_menu, width=20).pack(pady=5)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizBowlApp(root)
    root.mainloop()