import tkinter as tk
from tkinter import ttk, messagebox
from database_connection import connect_db


def open_equipment_screen():
    window = tk.Toplevel()
    window.title("Equipment Management")
    window.geometry("800x500")

    # Input fields
    tk.Label(window, text="Equipment Name").grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(window, width=30)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Purchase Date (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=5)
    date_entry = tk.Entry(window, width=30)
    date_entry.grid(row=1, column=1)

    tk.Label(window, text="Condition Status").grid(row=2, column=0, padx=10, pady=5)
    status_entry = tk.Entry(window, width=30)
    status_entry.grid(row=2, column=1)

    tk.Label(window, text="Exercise ID").grid(row=3, column=0, padx=10, pady=5)
    exerciseid_entry = tk.Entry(window, width=30)
    exerciseid_entry.grid(row=3, column=1)

    selected_equipment_id = tk.StringVar()

    # TreeView
    cols = ("Equipment ID", "Name", "Purchase Date", "Condition", "Exercise ID")
    tree = ttk.Treeview(window, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)

    tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def fetch_equipment():
        conn = connect_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("""
                    SELECT equipmentid, eqname, purchasedate, conditionstatus, exerciseid
                    FROM equipment
                    ORDER BY equipmentid
                    """)
        rows = cur.fetchall()
        conn.close()
        return rows

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for row in fetch_equipment():
            tree.insert("", "end", values=row)

    def on_row_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            selected_equipment_id.set(values[0])
            name_entry.delete(0, tk.END)
            date_entry.delete(0, tk.END)
            status_entry.delete(0, tk.END)
            exerciseid_entry.delete(0, tk.END)
            name_entry.insert(0, values[1])
            date_entry.insert(0, values[2])
            status_entry.insert(0, values[3])
            exerciseid_entry.insert(0, values[4])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    # Buttons and functions
    def insert_equipment():
        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        INSERT INTO equipment (eqname, purchasedate, conditionstatus, exerciseid)
                        VALUES (%s, %s, %s, %s)
                        """, (name_entry.get(), date_entry.get(), status_entry.get(), exerciseid_entry.get()))
            conn.commit()
            messagebox.showinfo("Success", "Equipment added successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding equipment: {e}")
        finally:
            conn.close()

    def update_equipment():
        if not selected_equipment_id.get():
            messagebox.showwarning("Update", "Select equipment to update")
            return

        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        UPDATE equipment
                        SET eqname=%s,
                            purchasedate=%s,
                            conditionstatus=%s,
                            exerciseid=%s
                        WHERE equipmentid = %s
                        """, (name_entry.get(), date_entry.get(), status_entry.get(),
                              exerciseid_entry.get(), selected_equipment_id.get()))
            conn.commit()
            messagebox.showinfo("Success", "Equipment updated successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating equipment: {e}")
        finally:
            conn.close()

    def delete_equipment():
        if not selected_equipment_id.get():
            messagebox.showwarning("Delete", "Select equipment to delete")
            return

        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM equipment WHERE equipmentid=%s", (selected_equipment_id.get(),))
            conn.commit()
            messagebox.showinfo("Success", "Equipment deleted successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting equipment: {e}")
        finally:
            conn.close()

    tk.Button(window, text="Add", width=10, command=insert_equipment).grid(row=0, column=2, padx=10)
    tk.Button(window, text="Update", width=10, command=update_equipment).grid(row=1, column=2, padx=10)
    tk.Button(window, text="Delete", width=10, command=delete_equipment).grid(row=2, column=2, padx=10)

    refresh_tree()
    window.grid_rowconfigure(5, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_columnconfigure(3, weight=1)