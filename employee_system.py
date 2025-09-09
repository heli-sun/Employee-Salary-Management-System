import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

# Try to import data science packages with error handling
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Pandas not available - table functionality disabled")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("Numpy not available")

try:
    import matplotlib
    matplotlib.use('TkAgg')  # Set the backend to TkAgg
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available - chart functionality disabled")


# Employee data storage with persistence
employees = []
DATA_FILE = "employee_data.json"

# Currency conversion rates (relative to USD)
currency_rates = {"$": 1.0, "€": 1.08, "3": 1.27, "¥": 0.0062, "₽": 0.011, "₹": 0.012, "﷼": 0.0027}

# Data persistence functions
def load_data():
    """Load employee data from JSON file"""
    global employees
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                employees = json.load(f)
        except:
            employees = []
    else:
        employees = []

def save_data():
    """Save employee data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(employees, f)

# Load data when the application starts
load_data()

def convert_to_usd(salary, symbol):
    """Convert salary from any currency to USD"""
    rate = currency_rates.get(symbol, 1)
    return salary * rate

def ask_sequential_inputs(prompts, title, callback):
    """Ask user for multiple inputs sequentially"""
    responses = []

    def ask_next(index):
        if index >= len(prompts):
            callback(responses)
            return

        top = tk.Toplevel(root)
        top.title(title)
        tk.Label(top, text=prompts[index]).pack(padx=10, pady=(10, 0))
        entry = tk.Entry(top)
        entry.pack(padx=10, pady=(0, 10))
        entry.focus_set()

        def on_enter(k=''):
            responses.append(entry.get())
            top.destroy()
            ask_next(index + 1)

        entry.bind("<Return>", on_enter)

    ask_next(0)

def register_employee(b=''):
    """Register a new employee"""
    prompts = ["Full Name:", "Employee ID:", "Job Title:"]
    
    def process(responses):
        name, emp_id, position = responses 
        if not name or not emp_id or not position:
            messagebox.showwarning("Input Error", "❌ All fields are required.")
            return
        if not name.replace(" ", "").isalpha():
            messagebox.showwarning("Name Error", "❌ Name must contain only letters.")
            return
        if not position.replace(" ", "").isalpha():
            messagebox.showwarning("Job Title Error", "❌ Job Title must contain only letters.")
            return
            
        if any(emp['id'] == emp_id for emp in employees): 
            messagebox.showerror("Duplicate ID", "❌ Employee ID already exists. Use a unique ID.")
            return
            
        employees.append({'id': emp_id, 'name': name,'position': position, 'salary': None, 'symbol': None})
        save_data()
        
        messagebox.showinfo("Success", "✅ Employee registered.")
        
    ask_sequential_inputs(prompts, "Register Employee", process)

def set_salary(o=''):
    """Set salary for an employee"""
    prompts = ["Enter Employee ID:", "Currency symbol (e.g., $, €, £):", "Salary amount:"]
    
    def process(responses):
        emp_id, symbol, salary_str = responses 
        for emp in employees:
            if emp['id'] == emp_id:
                if symbol not in currency_rates:
                    messagebox.showerror("Error", "❌ Unsupported currency symbol.")
                    return
                try:
                    salary = float(salary_str)
                    emp['salary'] = salary
                    emp['symbol'] = symbol
                    save_data()
                    messagebox.showinfo("Success", "💰 Salary recorded.")
                except ValueError:
                    messagebox.showerror("Error", "❌ Invalid salary amount.")
                return
        messagebox.showerror("Error", "❌ Employee not found.")
        
    ask_sequential_inputs(prompts, "Set Salary", process)

def search_employee(l=''):
    """Search for an employee by ID"""
    prompts = ["Enter Employee ID:"]
    
    def process(responses):
        emp_id = responses[0]
        for emp in employees:
            if emp['id'] == emp_id:
                info = f"👤 Name: {emp['name']}\n📌 Position: {emp['position']}"
                if emp['salary'] and emp['symbol']:
                    usd = convert_to_usd(emp['salary'], emp['symbol'])
                    info += f"\n💰 Salary: {emp['salary']} {emp['symbol']} (~${usd:.2f} USD)"
                else:
                    info += "\n💬 Salary: Not set yet."
                messagebox.showinfo("Employee Info", info)
                return
        messagebox.showerror("Error", "❌ Employee not found.")
        
    ask_sequential_inputs(prompts, "Search Employee", process)

def edit_employee(p=''):
    """Edit employee information"""
    prompts = ["Enter Employee ID:", "New Full Name (leave blank):", "New Job Title (leave blank):", "Update salary? (yes/no):"]
    
    def process(responses):
        emp_id, new_name, new_pos, update_salary = responses 
        for emp in employees:
            if emp['id'] == emp_id:
                emp['name'] = new_name or emp['name']
                emp['position'] = new_pos or emp['position']
                if update_salary.lower() == "yes":
                    ask_sequential_inputs(["New Currency symbol (e.g., $, €, £):", "New Salary amount:"], 
                    "Update Salary", lambda sal_resp: update_salary_data(emp, sal_resp))
                else:
                    save_data()
                    messagebox.showinfo("Success", "✏️ Info updated.")
                return
        messagebox.showerror("Error", "❌ Employee not found.")
        
    ask_sequential_inputs(prompts, "Edit Employee", process)

def update_salary_data(emp, sal_resp):
    """Update salary data for an employee"""
    symbol, salary_str = sal_resp  
    
    if symbol not in currency_rates:
        messagebox.showerror("Error", "❌ Unsupported currency symbol.")
        return
    try:
        salary = float(salary_str)
        emp['salary'] = salary
        emp['symbol'] = symbol
        save_data()
        messagebox.showinfo("Success", "💵 Salary updated.")
    except ValueError:
        messagebox.showerror("Error", "❌ Invalid salary input.")

def show_employee_table(z=''):
    """Display employee data in a table"""
    if not employees:
        messagebox.showinfo("Info", "⚠️ No employee data to display.")
        return
        
    if not PANDAS_AVAILABLE:
        messagebox.showerror("Error", "Pandas is not installed. Please install it with: pip install pandas")
        return

    table_rows = []
    for idx, emp in enumerate(employees, start=1):
        salary = f"{emp['salary']} {emp['symbol']}" if emp['salary'] and emp['symbol'] else "Not Set"
        table_rows.append({
            "No.": idx,
            "Name": emp['name'],
            "Job Title": emp['position'],
            "Salary": salary,
            "Employee ID": emp['id']
        })

    df = pd.DataFrame(table_rows)

    # Clear existing table if any
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()

    # Style the table
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Custom.Treeview",
                    background="black",
                    foreground="white",
                    fieldbackground="black",
                    bordercolor="white",
                    borderwidth=1)
    style.map("Custom.Treeview",
              background=[("selected", "#444")],
              foreground=[("selected", "white")])

    # Create and populate table
    tree = ttk.Treeview(root, style="Custom.Treeview", columns=list(df.columns), show="headings")

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill="both", expand=True)

def show_salary_chart():
    """Generate a bar chart of employee salaries"""
    if not employees:
        messagebox.showinfo("Info", "⚠️ No employee data available.")
        return
        
    if not MATPLOTLIB_AVAILABLE or not NUMPY_AVAILABLE:
        messagebox.showerror("Error", "Matplotlib or Numpy is not installed. Please install them with: pip install matplotlib numpy")
        return

    labels = []
    salaries = []

    for emp in employees:
        if emp['salary'] and emp['symbol']:
            usd_salary = convert_to_usd(emp['salary'], emp['symbol'])
            label = f"{emp['name']} ({emp['position']})"
            labels.append(label)
            salaries.append(usd_salary)

    if not salaries:
        messagebox.showinfo("Info", "ℹ️ No valid salary data to plot.")
        return

    df = pd.DataFrame({
        'Employee': labels,
        'Salary (USD)': salaries })

    plt.figure(figsize=(12, 7))
    
    colors = plt.cm.viridis(np.linspace(0.4, 0.9, len(df)))
    bars = plt.bar(df['Employee'], df['Salary (USD)'], color=colors, edgecolor='black', linewidth=1)

    plt.title("Employee Salaries by Name and Job Title", fontsize=16, fontweight='bold', color='#0c5180')
    plt.ylabel("Monthly Salary (USD)", fontsize=12)
    plt.xticks(rotation=30, ha='right', fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 7, f"${yval:,.0f}", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1f1f1f')

    plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))

    plt.tight_layout()
    plt.show()

def on_show_chart(y=''):
    show_salary_chart()

def exit_program(x=''):
    """Exit the application with confirmation"""
    if messagebox.askyesno("Exit", "Do you want to exit the program?"):
        root.destroy()

# Create the main application window
root = tk.Tk()
root.title("🧾 Employee Salary Management System 🧾")
root.configure(bg="black")

# Create main frame
frame_main = tk.Frame(root, relief="ridge", bd=10, bg="black")
frame_main.pack(pady=10)

# Application title
lbl_title = tk.Label(frame_main, text="🧾 Employee Salary Management System 🧾", width=40, 
                     font=("Arial", 13, "bold italic"), bg="black", fg="white")
lbl_title.pack(pady=15)

# Button styling
btn_font = ("Arial", 10, "bold italic")

# Create buttons for all functionalities
tk.Button(frame_main, text="Register New Employee", width=30, relief="groove",
          bd=7, font=btn_font, command=register_employee, bg='#659aff').pack(pady=5)

tk.Button(frame_main, text="Set Salary", width=30, relief="groove",
          bd=7, font=btn_font, command=set_salary, bg='#3668c9').pack(pady=5)

tk.Button(frame_main, text="Edit Employee Info", width=30, relief="groove",
          bd=7, font=btn_font, command=edit_employee, bg='#003190').pack(pady=5)

tk.Button(frame_main, text="Search Employee", width=30, relief="groove",
          bd=7, font=btn_font, command=search_employee, bg='#0c5180').pack(pady=5)

tk.Button(frame_main, text="Employee Table", width=30, relief="groove",
          bd=7, font=btn_font, command=show_employee_table, bg='#24578b').pack(pady=5)

tk.Button(frame_main, text="Salary Chart", width=30, relief="groove",
          bd=7, font=btn_font, command=show_salary_chart, bg='#0c5180').pack(pady=5)

tk.Button(frame_main, text="Exit", width=30, relief="groove",
          bd=7, font=btn_font, command=exit_program, bg='#0e2962').pack(pady=10)

# Keyboard shortcuts info
tk.Label(frame_main, text="🎯 Shortcuts: 1=Register | 2=Salary | 3=Edit | 4=Search | 5=Table | 6=Chart | 7=Exit",
         font=("Arial", 9, "italic"), fg="white", bg="black").pack(pady=5)

# Bind keyboard shortcuts
root.bind("<KeyPress-1>", register_employee) 
root.bind("<KeyPress-2>", set_salary) 
root.bind("<KeyPress-3>", edit_employee) 
root.bind("<KeyPress-4>", search_employee) 
root.bind("<KeyPress-5>", show_employee_table) 
root.bind("<KeyPress-6>", on_show_chart) 
root.bind("<KeyPress-7>", exit_program) 

# Start the application
root.mainloop()