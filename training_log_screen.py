import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database_connection import connect_db


def open_traininglog_screen():
    window = tk.Toplevel()
    window.title("Training Log Management")
    window.geometry("900x600")

    # === Input Fields ===
    input_frame = tk.Frame(window)
    input_frame.pack(pady=10, fill="x")

    tk.Label(input_frame, text="Member ID").grid(row=0, column=0, padx=10, pady=5)
    memberid_entry = tk.Entry(input_frame)
    memberid_entry.grid(row=0, column=1, padx=5)

    tk.Label(input_frame, text="Program ID").grid(row=1, column=0, padx=10, pady=5)
    programid_entry = tk.Entry(input_frame)
    programid_entry.grid(row=1, column=1, padx=5)

    tk.Label(input_frame, text="Duration (minutes)").grid(row=0, column=2, padx=10, pady=5)
    duration_entry = tk.Entry(input_frame)
    duration_entry.grid(row=0, column=3, padx=5)

    tk.Label(input_frame, text="Repetitions").grid(row=1, column=2, padx=10, pady=5)
    repetitions_entry = tk.Entry(input_frame)
    repetitions_entry.grid(row=1, column=3, padx=5)

    selected_log_id = tk.StringVar()

    # === Treeview ===
    tree_frame = tk.Frame(window)
    tree_frame.pack(pady=10, fill="both", expand=True)

    cols = ("Log ID", "Member ID", "Program ID", "Duration", "Repetitions", "Program Name")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings")

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120)

    tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=tree_scroll.set)
    tree_scroll.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    def fetch_traininglogs():
        conn = connect_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute("""
                    SELECT t.logid, t.memberid, t.programid, t.duration, t.repetitions, p.programname
                    FROM traininglog t
                             JOIN trainingprogram p ON t.programid = p.programid
                    ORDER BY t.logid
                    """)
        rows = cur.fetchall()
        conn.close()
        return rows

    def refresh_tree():
        for row in tree.get_children():
            tree.delete(row)
        for row in fetch_traininglogs():
            tree.insert("", "end", values=row)

    def on_row_select(event):
        selected = tree.focus()
        if selected:
            values = tree.item(selected)["values"]
            selected_log_id.set(values[0])
            memberid_entry.delete(0, tk.END)
            programid_entry.delete(0, tk.END)
            duration_entry.delete(0, tk.END)
            repetitions_entry.delete(0, tk.END)

            memberid_entry.insert(0, values[1])
            programid_entry.insert(0, values[2])
            duration_entry.insert(0, values[4])
            repetitions_entry.insert(0, values[5])

    tree.bind("<<TreeviewSelect>>", on_row_select)

    # === Button Frame ===
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10, fill="x")

    def insert_traininglog():
        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        INSERT INTO traininglog (memberid, programid, duration, repetitions)
                        VALUES (%s, %s, %s, %s, %s)
                        """, (memberid_entry.get(), programid_entry.get(),
                              duration_entry.get(), repetitions_entry.get()))
            conn.commit()
            messagebox.showinfo("Success", "Training log added successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error adding training log: {e}")
        finally:
            conn.close()

    def update_traininglog():
        if not selected_log_id.get():
            messagebox.showwarning("Update", "Select a training log to update")
            return

        conn = connect_db()
        if not conn:
            return
        cur = conn.cursor()
        try:
            cur.execute("""
                        UPDATE traininglog
                        SET memberid=%s,
                            programid=%s,
                            duration=%s,
                            repetitions=%s
                        WHERE logid = %s
                        """, (memberid_entry.get(), programid_entry.get(),
                              duration_entry.get(), repetitions_entry.get(), selected_log_id.get()))
            conn.commit()
            messagebox.showinfo("Success", "Training log updated successfully")
            refresh_tree()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating training log: {e}")
        finally:
            conn.close()

    def delete_traininglog():
        if not selected_log_id.get():
            messagebox.showwarning("Delete", "Select a training log to delete")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this log?"):
            conn = connect_db()
            if not conn:
                return
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM traininglog WHERE logid=%s", (selected_log_id.get(),))
                conn.commit()
                messagebox.showinfo("Success", "Training log deleted successfully")
                refresh_tree()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting training log: {e}")
            finally:
                conn.close()

    tk.Button(button_frame, text="Add Log", width=15, command=insert_traininglog).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Update Log", width=15, command=update_traininglog).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Delete Log", width=15, command=delete_traininglog).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Refresh", width=15, command=refresh_tree).pack(side=tk.LEFT, padx=10)

    refresh_tree()