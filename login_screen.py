import tkinter as tk
from tkinter import messagebox
from main_menu import main_menu


def login_screen():
    login_window = tk.Tk()
    login_window.title("Gym Manager - Login")
    login_window.geometry("400x300")

    tk.Label(login_window, text="Welcome to Gym Management System", font=("Arial", 14)).pack(pady=20)

    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, width=30, show="*")
    password_entry.pack(pady=5)

    def verify_login():
        if username_entry.get() == "Noam" and password_entry.get() == "Noam":
            login_window.destroy()
            main_menu()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    tk.Button(login_window, text="Login", command=verify_login, width=15).pack(pady=20)

    login_window.mainloop()