import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import connect_db


def open_exercise_screen():
    window = tk.Toplevel()
    window.title("Exercise Management")
    window.geometry("800x500")

    # Input fields
    tk.Label(window, text="Exercise Name").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(window, width=30)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Description").grid(row=1, column=0, padx=10, pady=5)
    desc_entry = tk.Entry(window, width=30)
    desc_entry.grid(row=1, column=1)

    tk.Label(window, text="Program ID").grid(row=2, column=0, padx=10, pady=5)
    programid_entry = tk.Entry(window, width=30)
    programid_entry.grid(row=2, column=1)

    selected_exercise_id = tk.StringVar()

    # TreeView
    cols = ("Exercise ID", "Name", "Description", "Program ID")
    tree = ttk.Treeview(window, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)

    tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def fetch_exercises():
        conn = connect_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("SELECT exerciseid, exname, description, programid FROM exercise ORDER BY exerciseid")
        rows = cur.fetchall()
        conn.close()
        return rows

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for row in fetch_exercises():
            tree.insert("", "end", values=row)

    def on_row_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            selected_exercise_id.set(values[0])
            name_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
            programid_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            desc_entry.insert(0, values[2])
            programid_entry.insert(0, values[3])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    # Buttons and functions
    def insert_exercise():
        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        INSERT INTO exercise (exname, description, programid)
                        VALUES (%s, %s, %s)
                        """, (name_entry.get(), desc_entry.get(), programid_entry.get()))
            conn.commit()
            messagebox.showinfo("Success", "Exercise added successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding exercise: {e}")
        finally:
            conn.close()

    def update_exercise():
        if not selected_exercise_id.get():
            messagebox.showwarning("Update", "Select an exercise to update")
            return

        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        UPDATE exercise
                        SET exname=%s,
                            description=%s,
                            programid=%s
                        WHERE exerciseid = %s
                        """, (name_entry.get(), desc_entry.get(), programid_entry.get(), selected_exercise_id.get()))
            conn.commit()
            messagebox.showinfo("Success", "Exercise updated successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating exercise: {e}")
        finally:
            conn.close()

    def delete_exercise():
        if not selected_exercise_id.get():
            messagebox.showwarning("Delete", "Select an exercise to delete")
            return

        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM exercise WHERE exerciseid=%s", (selected_exercise_id.get(),))
            conn.commit()
            messagebox.showinfo("Success", "Exercise deleted successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting exercise: {e}")
        finally:
            conn.close()

    tk.Button(window, text="Add", width=10, command=insert_exercise).grid(row=0, column=2, padx=10)
    tk.Button(window, text="Update", width=10, command=update_exercise).grid(row=1, column=2, padx=10)
    tk.Button(window, text="Delete", width=10, command=delete_exercise).grid(row=2, column=2, padx=10)

    refresh_tree()
    window.grid_rowconfigure(4, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_columnconfigure(3, weight=1)