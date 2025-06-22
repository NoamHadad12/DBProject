import tkinter as tk
from tkinter import ttk, scrolledtext
from database_connection import connect_db


def open_query_screen():
    window = tk.Toplevel()
    window.title("Database Queries and Functions")
    window.geometry("900x700")

    notebook = ttk.Notebook(window)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)

    # === Query Tab ===
    query_tab = ttk.Frame(notebook)
    notebook.add(query_tab, text='Run Queries')

    tk.Label(query_tab, text="Available Queries").pack(pady=5)

    queries = {
        "Members with Active Programs": """
                                        SELECT m.memberid, m.firstname, m.lastname, COUNT(p.programid) as program_count
                                        FROM member m
                                                 JOIN trainingprogram p ON m.memberid = p.memberid
                                        WHERE p.enddate >= CURRENT_DATE
                                        GROUP BY m.memberid, m.firstname, m.lastname
                                        ORDER BY program_count DESC
                                        """,

        "Equipment Condition Report": """
                                      SELECT conditionstatus, COUNT(*) as count
                                      FROM equipment
                                      GROUP BY conditionstatus
                                      ORDER BY count DESC
                                      """,

        "Training Logs Summary by Member": """
                                           SELECT m.memberid,
                                                  m.firstname,
                                                  m.lastname,
                                                  COUNT(l.logid)  as log_count,
                                                  SUM(l.duration) as total_duration
                                           FROM member m
                                                    LEFT JOIN traininglog l ON m.memberid = l.memberid
                                           GROUP BY m.memberid, m.firstname, m.lastname
                                           ORDER BY total_duration DESC
                                           """,

        "Exercises per Program": """
                                 SELECT p.programid, p.programname, COUNT(e.exerciseid) as exercise_count
                                 FROM trainingprogram p
                                          LEFT JOIN exercise e ON p.programid = e.programid
                                 GROUP BY p.programid, p.programname
                                 ORDER BY exercise_count DESC
                                 """
    }

    query_var = tk.StringVar()
    query_dropdown = ttk.Combobox(query_tab, textvariable=query_var, width=50)
    query_dropdown['values'] = list(queries.keys())
    query_dropdown.current(0)
    query_dropdown.pack(pady=5)

    result_text = scrolledtext.ScrolledText(query_tab, height=20)
    result_text.pack(fill='both', expand=True, pady=10)

    def run_query():
        query_name = query_var.get()
        if query_name in queries:
            sql = queries[query_name]
            conn = connect_db()
            if not conn:
                return

            try:
                cur = conn.cursor()
                cur.execute(sql)
                rows = cur.fetchall()

                # Get column names
                col_names = [desc[0] for desc in cur.description]

                # Format and display results
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Query Results: {query_name}\n\n")

                # Format column headers
                result_text.insert(tk.END, " | ".join(col_names) + "\n")
                result_text.insert(tk.END,
                                   "-" * (sum(len(name) for name in col_names) + 3 * (len(col_names) - 1)) + "\n")

                # Format rows
                for row in rows:
                    result_text.insert(tk.END, " | ".join(str(val) for val in row) + "\n")

                result_text.insert(tk.END, f"\n{len(rows)} rows returned")

            except Exception as e:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Error executing query: {e}")
            finally:
                conn.close()

    tk.Button(query_tab, text="Run Query", width=15, command=run_query).pack(pady=10)

    # === Function Tab ===
    function_tab = ttk.Frame(notebook)
    notebook.add(function_tab, text='Run Functions')

    tk.Label(function_tab, text="Available Functions").pack(pady=5)

    functions = {
        "Calculate Member Training Stats": {
            "description": "Calculate total training duration and count for a member",
            "param_labels": ["Member ID"],
            "sql": """
                   SELECT COUNT(logid)  as training_count,
                          SUM(duration) as total_duration,
                          AVG(duration) as avg_duration
                   FROM traininglog
                   WHERE memberid = %s
                   """
        },

        "Check Equipment Due for Maintenance": {
            "description": "List equipment that needs maintenance based on condition",
            "param_labels": ["Condition (e.g. 'Poor', 'Fair')"],
            "sql": """
                   SELECT equipmentid, eqname, purchasedate, conditionstatus
                   FROM equipment
                   WHERE conditionstatus = %s
                   ORDER BY purchasedate
                   """
        }
    }

    function_var = tk.StringVar()
    function_dropdown = ttk.Combobox(function_tab, textvariable=function_var, width=50)
    function_dropdown['values'] = list(functions.keys())
    function_dropdown.current(0)
    function_dropdown.pack(pady=5)

    # Description label
    desc_label = tk.Label(function_tab, text="", wraplength=500)
    desc_label.pack(pady=5)

    # Parameter frame
    param_frame = tk.Frame(function_tab)
    param_frame.pack(pady=10, fill="x")

    param_entries = []

    def update_function_ui(*args):
        # Clear previous param entries
        for widget in param_frame.winfo_children():
            widget.destroy()

        param_entries.clear()

        func_name = function_var.get()
        if func_name in functions:
            func_info = functions[func_name]
            desc_label.config(text=func_info["description"])

            # Create input fields for parameters
            for i, param_label in enumerate(func_info["param_labels"]):
                tk.Label(param_frame, text=param_label).grid(row=i, column=0, padx=10, pady=5)
                entry = tk.Entry(param_frame, width=30)
                entry.grid(row=i, column=1, padx=10, pady=5)
                param_entries.append(entry)

    function_var.trace("w", update_function_ui)

    function_result = scrolledtext.ScrolledText(function_tab, height=20)
    function_result.pack(fill='both', expand=True, pady=10)

    def run_function():
        func_name = function_var.get()
        if func_name in functions:
            func_info = functions[func_name]
            params = [entry.get() for entry in param_entries]

            conn = connect_db()
            if not conn:
                return

            try:
                cur = conn.cursor()
                cur.execute(func_info["sql"], params)
                rows = cur.fetchall()

                # Get column names
                col_names = [desc[0] for desc in cur.description]

                # Format and display results
                function_result.delete(1.0, tk.END)
                function_result.insert(tk.END, f"Function Results: {func_name}\n\n")

                # Format column headers
                function_result.insert(tk.END, " | ".join(col_names) + "\n")
                function_result.insert(tk.END,
                                       "-" * (sum(len(name) for name in col_names) + 3 * (len(col_names) - 1)) + "\n")

                # Format rows
                for row in rows:
                    function_result.insert(tk.END, " | ".join(str(val) for val in row) + "\n")

                function_result.insert(tk.END, f"\n{len(rows)} rows returned")

            except Exception as e:
                function_result.delete(1.0, tk.END)
                function_result.insert(tk.END, f"Error executing function: {e}")
            finally:
                conn.close()

    tk.Button(function_tab, text="Run Function", width=15, command=run_function).pack(pady=10)

    # Initialize the function UI
    update_function_ui()