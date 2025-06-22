import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import connect_db


def open_programs_screen():
    window = tk.Toplevel()
    window.title("Training Program Management")
    window.geometry("800x500")

    # Input fields
    tk.Label(window, text="Program Name").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(window, width=30)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Description").grid(row=1, column=0, padx=10, pady=5)
    desc_entry = tk.Entry(window, width=30)
    desc_entry.grid(row=1, column=1)

    tk.Label(window, text="Start Date (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=5)
    start_entry = tk.Entry(window, width=30)
    start_entry.grid(row=2, column=1)

    tk.Label(window, text="End Date (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5)
    end_entry = tk.Entry(window, width=30)
    end_entry.grid(row=3, column=1)

    tk.Label(window, text="Member ID").grid(row=0, column=2, padx=10, pady=5)
    memberid_entry = tk.Entry(window, width=30)
    memberid_entry.grid(row=0, column=3)

    selected_program_id = tk.StringVar()

    # TreeView
    cols = ("Program ID", "Program Name", "Description", "Start Date", "End Date", "Member ID")
    tree = ttk.Treeview(window, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)

    tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def fetch_programs():
        conn = connect_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute(
            "SELECT programid, programname, description, startdate, enddate, memberid FROM trainingprogram ORDER BY programid")
        rows = cur.fetchall()
        conn.close()
        return rows

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
            name_entry.delete(0, tk.END)
            desc_entry.delete(0, tk.END)
            start_entry.delete(0, tk.END)
            end_entry.delete(0, tk.END)
            memberid_entry.delete(0, tk.END)

            name_entry.insert(0, values[1])
            desc_entry.insert(0, values[2])
            start_entry.insert(0, values[3])
            end_entry.insert(0, values[4])
            memberid_entry.insert(0, values[5])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    # Buttons and functions
    def insert_program():
        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        INSERT INTO trainingprogram (programname, description, startdate, enddate, memberid)
                        VALUES (%s, %s, %s, %s, %s)
                        """, (name_entry.get(), desc_entry.get(), start_entry.get(),
                              end_entry.get(), memberid_entry.get()))
            conn.commit()
            messagebox.showinfo("Success", "Training program added successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding program: {e}")
        finally:
            conn.close()

    def update_program():
        if not selected_program_id.get():
            messagebox.showwarning("Update", "Select a program to update")
            return

        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        UPDATE trainingprogram
                        SET programname=%s,
                            description=%s,
                            startdate=%s,
                            enddate=%s,
                            memberid=%s
                        WHERE programid = %s
                        """, (name_entry.get(), desc_entry.get(), start_entry.get(),
                              end_entry.get(), memberid_entry.get(), selected_program_id.get()))
            conn.commit()
            messagebox.showinfo("Success", "Training program updated successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating program: {e}")
        finally:
            conn.close()

    def delete_program():
        if not selected_program_id.get():
            messagebox.showwarning("Delete", "Select a program to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this program?"):
            conn = connect_db()
            if not conn:
                return
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM trainingprogram WHERE programid=%s", (selected_program_id.get(),))
                conn.commit()
                messagebox.showinfo("Success", "Training program deleted successfully")
                refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting program: {e}")
            finally:
                conn.close()

    tk.Button(window, text="Add", width=10, command=insert_program).grid(row=0, column=4, padx=10)
    tk.Button(window, text="Update", width=10, command=update_program).grid(row=1, column=4, padx=10)
    tk.Button(window, text="Delete", width=10, command=delete_program).grid(row=2, column=4, padx=10)

    refresh_tree()
    window.grid_rowconfigure(5, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_columnconfigure(3, weight=1)