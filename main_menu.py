import tkinter as tk
from training_log_screen import open_traininglog_screen
from exercise_screen import open_exercise_screen
from equipment_screen import open_equipment_screen
from query_screen import open_query_screen
from members_screen import open_members_screen
from TrainingProgram import open_programs_screen


def main_menu():
    root = tk.Tk()
    root.title("Gym Manager - Main Menu")
    root.geometry("500x600")

    header = tk.Label(root, text="GYM MANAGEMENT SYSTEM", font=("Arial", 16, "bold"))
    header.pack(pady=20)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    button_width = 25
    button_height = 2
    button_padx = 10
    button_pady = 10

    tk.Button(button_frame, text="Members", command=open_members_screen,
              width=button_width, height=button_height).pack(pady=button_pady)

    tk.Button(button_frame, text="Training Programs", command=open_programs_screen,
              width=button_width, height=button_height).pack(pady=button_pady)

    tk.Button(button_frame, text="Training Logs", command=open_traininglog_screen,
              width=button_width, height=button_height).pack(pady=button_pady)

    tk.Button(button_frame, text="Exercises", command=open_exercise_screen,
              width=button_width, height=button_height).pack(pady=button_pady)

    tk.Button(button_frame, text="Equipment", command=open_equipment_screen,
              width=button_width, height=button_height).pack(pady=button_pady)

    tk.Button