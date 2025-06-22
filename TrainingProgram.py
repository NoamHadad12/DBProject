import psycopg2
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Label, Entry, StringVar, END, Button
from database_connection import connect_db

# === CRUD Functions ===
def fetch_programs():
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute("SELECT * FROM trainingprogram ORDER BY programid")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_program(name, start, end, memberid):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trainingprogram (programname, startdate, enddate, memberid)
        VALUES (%s, %s, %s, %s)
    """, (name, start, end, memberid))
    conn.commit()
    conn.close()

def update_program(programid, name, start, end, memberid):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("""
        UPDATE trainingprogram
        SET programname=%s, startdate=%s, enddate=%s, memberid=%s
        WHERE programid=%s
    """, (name, start, end, memberid, programid))
    conn.commit()
    conn.close()

def delete_program(programid):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("DELETE FROM trainingprogram WHERE programid=%s", (programid,))
    conn.commit()
    conn.close()

# === Training Program Management Screen ===
def open_programs_screen():
    window = Toplevel()
    window.title("Training Program Management")
    window.geometry("800x500")

    # === Input Fields ===
    Label(window, text="Program Name").grid(row=0, column=0, padx=10, pady=5)
    name_entry = Entry(window)
    name_entry.grid(row=0, column=1)

    Label(window, text="Start Date (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=5)
    start_entry = Entry(window)
    start_entry.grid(row=1, column=1)

    Label(window, text="End Date (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5)
    end_entry = Entry(window)
    end_entry.grid(row=2, column=1)

    Label(window, text="Member ID").grid(row=3, column=0, padx=10, pady=5)
    memberid_entry = Entry(window)
    memberid_entry.grid(row=3, column=1)

    selected_program_id = StringVar()

    # === Treeview ===
    cols = ("Program ID", "Name", "Start", "End", "Member ID")
    tree = ttk.Treeview(window, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
    tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for row in fetch_programs():
            tree.insert("", "end", values=row)

    def on_row_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            selected_program_id.set(values[0])
            name_entry.delete(0, END)
            start_entry.delete(0, END)
            end_entry.delete(0, END)
            memberid_entry.delete(0, END)
            name_entry.insert(0, values[1])
            start_entry.insert(0, values[2])
            end_entry.insert(0, values[3])
            memberid_entry.insert(0, values[4])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    # === Buttons ===
    def handle_add():
        insert_program(name_entry.get(), start_entry.get(), end_entry.get(), memberid_entry.get())
        refresh_tree()

    def handle_update():
        if not selected_program_id.get():
            messagebox.showwarning("Update", "Select a program to update.")
            return
        update_program(selected_program_id.get(), name_entry.get(), start_entry.get(), end_entry.get(), memberid_entry.get())
        refresh_tree()

    def handle_delete():
        if not selected_program_id.get():
            messagebox.showwarning("Delete", "Select a program to delete.")
            return
        delete_program(selected_program_id.get())
        refresh_tree()

    Button(window, text="Add", width=10, command=handle_add).grid(row=0, column=2, padx=10)
    Button(window, text="Update", width=10, command=handle_update).grid(row=1, column=2, padx=10)
    Button(window, text="Delete", width=10, command=handle_delete).grid(row=2, column=2, padx=10)

    refresh_tree()
