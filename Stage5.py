import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# === PostgreSQL Connection ===
def connect_db():
    try:
        conn = psycopg2.connect(
            host="192.168.1.209",
            port=5432,
            database="mydatabase",
            user="NoamHadad1",
            password="Noam.123"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None

# === CRUD Functions ===
def fetch_members():
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute("SELECT * FROM member ORDER BY memberid")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_member(fname, lname, email):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("INSERT INTO member (firstname, lastname, email) VALUES (%s, %s, %s)",
                (fname, lname, email))
    conn.commit()
    conn.close()

def update_member(memberid, fname, lname, email):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("UPDATE member SET firstname=%s, lastname=%s, email=%s WHERE memberid=%s",
                (fname, lname, email, memberid))
    conn.commit()
    conn.close()

def delete_member(memberid):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute("DELETE FROM member WHERE memberid=%s", (memberid,))
    conn.commit()
    conn.close()

# === Member Management Screen ===
def open_members_screen():
    member_window = tk.Toplevel()
    member_window.title("Member Management")
    member_window.geometry("700x500")

    # Input form
    tk.Label(member_window, text="First Name").grid(row=0, column=0, padx=10, pady=5)
    fname_entry = tk.Entry(member_window)
    fname_entry.grid(row=0, column=1)

    tk.Label(member_window, text="Last Name").grid(row=1, column=0, padx=10, pady=5)
    lname_entry = tk.Entry(member_window)
    lname_entry.grid(row=1, column=1)

    tk.Label(member_window, text="Email").grid(row=2, column=0, padx=10, pady=5)
    email_entry = tk.Entry(member_window)
    email_entry.grid(row=2, column=1)

    selected_member_id = tk.StringVar()

    # TreeView to show members
    cols = ("ID", "First Name", "Last Name", "Email")
    tree = ttk.Treeview(member_window, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
    tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for row in fetch_members():
            tree.insert("", "end", values=row)

    def on_row_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            selected_member_id.set(values[0])
            fname_entry.delete(0, tk.END)
            lname_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            fname_entry.insert(0, values[1])
            lname_entry.insert(0, values[2])
            email_entry.insert(0, values[3])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    # Buttons
    def handle_add():
        insert_member(fname_entry.get(), lname_entry.get(), email_entry.get())
        refresh_tree()

    def handle_update():
        if not selected_member_id.get():
            messagebox.showwarning("Update", "Select a member to update.")
            return
        update_member(selected_member_id.get(), fname_entry.get(), lname_entry.get(), email_entry.get())
        refresh_tree()

    def handle_delete():
        if not selected_member_id.get():
            messagebox.showwarning("Delete", "Select a member to delete.")
            return
        delete_member(selected_member_id.get())
        refresh_tree()

    tk.Button(member_window, text="Add", width=10, command=handle_add).grid(row=0, column=2, padx=10)
    tk.Button(member_window, text="Update", width=10, command=handle_update).grid(row=1, column=2, padx=10)
    tk.Button(member_window, text="Delete", width=10, command=handle_delete).grid(row=2, column=2, padx=10)

    refresh_tree()

# === Main Menu ===
def main_menu():
    root = tk.Tk()
    root.title("Gym Manager - Main Menu")
    root.geometry("400x400")

    tk.Button(root, text="Manage Members", command=open_members_screen, width=20, height=2).pack(pady=20)

    root.mainloop()

# === Run the App ===
main_menu()
