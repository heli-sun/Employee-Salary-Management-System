
# Employee Salary Management System 
A comprehensive desktop application built with Python and Tkinter for managing employee records and salaries with multi-currency support. Features a modern dark-themed interface with robust data management capabilities.

1. https://img.shields.io/badge/Python-3.8%252B-blue
2. https://img.shields.io/badge/GUI-Tkinter-green
3. https://img.shields.io/badge/License-MIT-lightgrey


# Features
Employee Management: Register, edit, and search employees with validation

Multi-Currency Support: 7 currencies with automatic USD conversion ($, €, £, ¥, ₽, ₹, ﷼)

Data Visualization: Beautiful bar charts with matplotlib showing salary distributions

Data Persistence: Automatic JSON storage that persists between sessions

Keyboard Shortcuts: Quick access to all functions (1-7 keys)

Modern UI: Dark theme with professional styling and responsive design


# Quick Start
Prerequisites:

Python 3.8+

pip package manager


# Installation
1. Clone the repository
git clone https://github.com/heli-sun/Employee-Salary-Management-System.git

2. Install dependencies
pip install -r requirements.txt

3. Run the application
python employee_system.py


# How to Use
Register Employees: Add new employees with details (Name, ID, Position)

Set Salaries: Assign salaries in different currencies with automatic USD conversion

Search & Edit: Find and modify employee records with intuitive search

View Data: See all employees in a formatted, sortable table

Visualize: Generate professional salary distribution charts


# Keyboard Shortcuts
Key	Function	Description:

1.	Register Employee	Add new employee to system
2.	Set Salary	Assign salary with currency
3.	Edit Employee	Modify existing employee data
4.	Search Employee	Find employee by ID
5.	Show Table	Display all employees in table format
6.	Show Chart	Generate salary visualization chart
7.	Exit Program	Safely close the application


# Built With
Python - Core programming language

Tkinter - GUI framework for desktop application

Pandas - Data manipulation and table display

Matplotlib - Data visualization and charting

NumPy - Numerical operations for calculations

JSON - Data storage and persistence


# Project Structure
text
employee-salary-system/
├── employee_system.py    # Main application logic

├── requirements.txt      # Python dependencies

├── README.md            # Project documentation

├── .gitignore           # Git ignore rules

└── images/              # Screenshots directory (add your own)

    ├── app-screenshot.png # App screenshots

    └── chart-screenshot.png #Chart screenshots


# How It Works
The application uses several key technologies:

Tkinter GUI: Creates a responsive desktop interface with custom styling

Data Validation: Ensures all inputs are properly formatted and validated

Currency Conversion: Real-time conversion using current exchange rates

JSON Storage: Automatic saving and loading of employee data

Matplotlib Integration: Professional data visualization within the application


# Customization
Add New Currencies
python
currency_rates = { 
    "$": 1.0, 
    "€": 1.08,
    "£": 1.27,
    # Add new currency:
    "CAD": 0.74,  # Canadian Dollar
    "AUD": 0.67,  # Australian Dollar
}


# Modify UI Colors
Change button colors:

bg='#659aff'  # Primary blue

bg='#3668c9'  # Darker blue

bg='#003190'  # Navy blue


# License
This project is licensed under the MIT License - see the LICENSE file for details.


# Troubleshooting
Common Issues:

Import errors: Ensure all dependencies are installed:


1. pip install -r requirements.txt
Matplotlib issues:


2. python -m pip install --upgrade matplotlib
Tkinter missing (Linux systems):


3. sudo apt-get install python3-tk
Application won't start: Check Python version (requires 3.8+)

# Data Persistence
The application automatically creates an employee_data.json file to store all information between sessions.