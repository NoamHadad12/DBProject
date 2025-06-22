import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import connect_db

def open_members_screen():
    window = tk.Toplevel()
    window.title("Member Management")
    window.geometry("800x500")

    # Input fields
    tk.Label(window, text="First Name").grid(row=0, column=0, padx=10, pady=5)
    firstname_entry = tk.Entry(window, width=30)
    firstname_entry.grid(row=0, column=1)

    tk.Label(window, text="Last Name").grid(row=1, column=0, padx=10, pady=5)
    lastname_entry = tk.Entry(window, width=30)
    lastname_entry.grid(row=1, column=1)

    tk.Label(window, text="Date of Birth (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5)
    dateofbirth_entry = tk.Entry(window, width=30)
    dateofbirth_entry.grid(row=2, column=1)

    tk.Label(window, text="Phone").grid(row=0, column=2, padx=10, pady=5)
    phone_entry = tk.Entry(window, width=30)
    phone_entry.grid(row=0, column=3)

    tk.Label(window, text="Email").grid(row=1, column=2, padx=10, pady=5)
    email_entry = tk.Entry(window, width=30)
    email_entry.grid(row=1, column=3)

    selected_member_id = tk.StringVar()

    # TreeView
    cols = ("Member ID", "First Name", "Last Name", "Date of Birth", "Phone", "Email")
    tree = ttk.Treeview(window, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)

    tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def fetch_members():
        conn = connect_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("SELECT memberid, firstname, lastname, dateofbirth, phone, email FROM member ORDER BY memberid")
        rows = cur.fetchall()
        conn.close()
        return rows

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
            firstname_entry.delete(0, tk.END)
            lastname_entry.delete(0, tk.END)
            dateofbirth_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)

            firstname_entry.insert(0, values[1])
            lastname_entry.insert(0, values[2])
            dateofbirth_entry.insert(0, values[3])
            phone_entry.insert(0, values[4])  # Changed from 5 to 4
            email_entry.insert(0, values[5])  # Changed from 6 to 5
    tree.bind("<<TreeviewSelect>>", on_row_select)

    # Buttons and functions
    def insert_member():
        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        INSERT INTO member (firstname, lastname, dateofbirth, phone, email)
                        VALUES (%s, %s, %s, %s, %s)
                        """, (firstname_entry.get(), lastname_entry.get(), dateofbirth_entry.get(),
                              phone_entry.get(), email_entry.get()))
            conn.commit()
            messagebox.showinfo("Success", "Member added successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding member: {e}")
        finally:
            conn.close()
    def update_member():
        if not selected_member_id.get():
            messagebox.showwarning("Update", "Select a member to update")
            return

        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE member SET firstname=%s,lastname=%s,dateofbirth=%s,phone=%s,email=%s
                WHERE memberid=%s
            """, (firstname_entry.get(), lastname_entry.get(), dateofbirth_entry.get(),
                 phone_entry.get(), email_entry.get(), selected_member_id.get()))
            conn.commit()
            messagebox.showinfo("Success", "Member updated successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating member: {e}")
        finally:
            conn.close()

    def delete_member():
        if not selected_member_id.get():
            messagebox.showwarning("Delete", "Select a member to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?"):
            conn = connect_db()
            if not conn:
                return
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM member WHERE memberid=%s", (selected_member_id.get(),))
                conn.commit()
                messagebox.showinfo("Success", "Member deleted successfully")
                refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting member: {e}")
            finally:
                conn.close()

    tk.Button(window, text="Add", width=10, command=insert_member).grid(row=0, column=4, padx=10)
    tk.Button(window, text="Update", width=10, command=update_member).grid(row=1, column=4, padx=10)
    tk.Button(window, text="Delete", width=10, command=delete_member).grid(row=2, column=4, padx=10)

    refresh_tree()
    window.grid_rowconfigure(5, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_columnconfigure(3, weight=1)