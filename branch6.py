import sqlite3
import random
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

# Define the days of the week
days = ['monday', 'tuesday', 'wednsday', 'thursday', 'friday', 'saturday', 'sunday']

# Function to fetch the schedule from the database
def fetch_schedule():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM schedule')
    schedule_data = cursor.fetchall()
    conn.close()
    print("Schedule Data:", schedule_data)  # Debugging output
    return schedule_data

# Function to fetch employees from the database, excluding 'control'
def fetch_employees():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, rating, hours, skills FROM employees WHERE name != "control"')
    employees = cursor.fetchall()
    conn.close()
    print("Employees Data:", employees)  # Debugging output
    return employees

# Function to fetch all employees including 'control' (for internal use only)
def fetch_all_employees():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, rating, hours, skills FROM employees')
    employees = cursor.fetchall()
    conn.close()
    return employees

# Function to fetch roles from the database
def fetch_roles():
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM roles')
    roles = cursor.fetchall()
    conn.close()
    return roles

# Function to add a new employee to the database
def add_employee(name, rating, skills):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO employees (name, rating, hours, skills) VALUES (?, ?, ?, ?)', (name, rating, 0, skills))
    conn.commit()
    conn.close()

# Function to update an employee's skills
def update_employee_skills(name, skills):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE employees SET skills = ? WHERE name = ?', (skills, name))
    conn.commit()
    conn.close()

# Function to remove an employee from the database
def remove_employee(name):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE name = ?', (name,))
    conn.commit()
    conn.close()

# Function to update a shift in the schedule
def update_shift(day, role, employee):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE schedule SET employee = ? WHERE day = ? AND role = ?', (employee, day, role))
    conn.commit()
    conn.close()

# Function to insert an empty shift into the schedule
def insert_empty_shift(day, role):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO schedule (day, role) VALUES (?, ?)', (day, role))
    conn.commit()
    conn.close()
    print(f"Inserted empty shift for {day} - {role}")  # Debugging output

# Function to view and edit the current schedule in a grid format
def view_schedule(view_frame):
    for widget in view_frame.winfo_children():
        widget.destroy()
        
    schedule_data = fetch_schedule()
    employees = fetch_employees()

    # Create the header row with the days of the week
    for col, day in enumerate(days, start=1):
        tk.Label(view_frame, text=day.capitalize(), borderwidth=1, relief="solid", width=15).grid(row=0, column=col)

    # Create the first column with employee names
    for row, employee in enumerate(employees, start=1):
        tk.Label(view_frame, text=employee[0], borderwidth=1, relief="solid", width=15).grid(row=row, column=0)

    # Fill in the schedule
    for day, role, employee in schedule_data:
        if employee and employee != 'control':  # Only add non-empty shifts
            row = [e[0] for e in employees].index(employee) + 1
            col = days.index(day) + 1
            tk.Label(view_frame, text=role, borderwidth=1, relief="solid", width=15).grid(row=row, column=col)

    # Add Refresh button at the bottom of the grid
    tk.Button(view_frame, text="Refresh Schedule", command=lambda: view_schedule(view_frame), font=('Helvetica', 12), width=20, height=2).grid(row=len(employees) + 1, column=0, columnspan=len(days) + 1, pady=10)

# Function to open a window to add a new employee
def add_employee_form(add_frame):
    for widget in add_frame.winfo_children():
        widget.destroy()

    def submit_add_employee():
        name = name_entry.get()
        rating = rating_var.get()
        skills = ', '.join(selected_skills)
        add_employee(name, rating, skills)
        messagebox.showinfo("Success", "Employee added successfully")

    tk.Label(add_frame, text="Name:", font=('Helvetica', 12)).grid(row=0, column=0, pady=5, sticky='e')
    tk.Label(add_frame, text="Rating:", font=('Helvetica', 12)).grid(row=1, column=0, pady=5, sticky='e')
    tk.Label(add_frame, text="Skills:", font=('Helvetica', 12)).grid(row=2, column=0, pady=5, sticky='e')

    name_entry = tk.Entry(add_frame, font=('Helvetica', 12), width=30)
    name_entry.grid(row=0, column=1, pady=5)

    rating_var = tk.StringVar()
    rating_dropdown = ttk.Combobox(add_frame, textvariable=rating_var, font=('Helvetica', 12), width=28)
    rating_dropdown['values'] = ('A', 'B', 'C')
    rating_dropdown.grid(row=1, column=1, pady=5)

    selected_skills = []

    def select_skills():
        skills_window = tk.Toplevel(add_frame)
        skills_window.title("Select Skills")

        skills_vars = []
        skill_names = [role[0] for role in fetch_roles()]

        for i, skill in enumerate(skill_names):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(skills_window, text=skill, variable=var, font=('Helvetica', 12))
            chk.grid(row=i, column=0, sticky='w')
            skills_vars.append((skill, var))

        def save_skills():
            selected_skills.clear()
            for skill, var in skills_vars:
                if var.get():
                    selected_skills.append(skill)
            skills_window.destroy()

        tk.Button(skills_window, text="Save", command=save_skills, font=('Helvetica', 12), width=15).grid(row=len(skill_names), column=0, pady=10)

    tk.Button(add_frame, text="Select Skills", command=select_skills, font=('Helvetica', 12), width=15).grid(row=2, column=1, pady=5, sticky='w')
    tk.Button(add_frame, text="Add Employee", command=submit_add_employee, font=('Helvetica', 12), width=15).grid(row=3, column=0, columnspan=2, pady=10)

# Function to update an employee's skills
def update_employee_skills_form(update_frame):
    for widget in update_frame.winfo_children():
        widget.destroy()

    def submit_update_skills():
        name = name_var.get()
        skills = ', '.join(selected_skills)
        update_employee_skills(name, skills)
        messagebox.showinfo("Success", "Employee skills updated successfully")

    tk.Label(update_frame, text="Name:", font=('Helvetica', 12)).grid(row=0, column=0, pady=5, sticky='e')
    tk.Label(update_frame, text="New Skills:", font=('Helvetica', 12)).grid(row=1, column=0, pady=5, sticky='e')

    name_var = tk.StringVar()
    name_dropdown = ttk.Combobox(update_frame, textvariable=name_var, font=('Helvetica', 12), width=28)
    name_dropdown['values'] = [employee[0] for employee in fetch_employees()]
    name_dropdown.grid(row=0, column=1, pady=5)

    selected_skills = []

    def select_skills():
        selected_employee = name_var.get()
        skills_window = tk.Toplevel(update_frame)
        skills_window.title("Select Skills")

        skills_vars = []
        skill_names = [role[0] for role in fetch_roles()]

        # Get current skills of the selected employee
        current_skills = []
        for employee in fetch_employees():
            if employee[0] == selected_employee:
                current_skills = employee[3].split(', ')

        for i, skill in enumerate(skill_names):
            var = tk.BooleanVar(value=skill in current_skills)
            chk = tk.Checkbutton(skills_window, text=skill, variable=var, font=('Helvetica', 12))
            chk.grid(row=i, column=0, sticky='w')
            skills_vars.append((skill, var))

        def save_skills():
            selected_skills.clear()
            for skill, var in skills_vars:
                if var.get():
                    selected_skills.append(skill)
            skills_window.destroy()

        tk.Button(skills_window, text="Save", command=save_skills, font=('Helvetica', 12), width=15).grid(row=len(skill_names), column=0, pady=10)

    tk.Button(update_frame, text="Select Skills", command=select_skills, font=('Helvetica', 12), width=15).grid(row=1, column=1, pady=5, sticky='w')
    tk.Button(update_frame, text="Update Skills", command=submit_update_skills, font=('Helvetica', 12), width=15).grid(row=2, column=0, columnspan=2, pady=10)

# Function to open a window to edit a specific shift
def edit_shift_form(edit_frame):
    for widget in edit_frame.winfo_children():
        widget.destroy()

    def submit_edit_shift():
        selected_shift = shift_var.get().split(' - ')
        day = selected_shift[0].lower()
        role = selected_shift[1].split(' (')[0]
        new_employee = employee_var.get()
        update_shift(day, role, new_employee)
        messagebox.showinfo("Success", "Shift updated successfully")

    tk.Label(edit_frame, text="Select Shift:", font=('Helvetica', 12)).grid(row=0, column=0, pady=5, sticky='e')
    tk.Label(edit_frame, text="New Employee:", font=('Helvetica', 12)).grid(row=1, column=0, pady=5, sticky='e')

    schedule_data = fetch_schedule()
    employees = [employee[0] for employee in fetch_employees()]

    shift_var = tk.StringVar()
    shift_dropdown = ttk.Combobox(edit_frame, textvariable=shift_var, font=('Helvetica', 12), width=28)
    shift_dropdown['values'] = [f"{day.capitalize()} - {role} (Current: {employee})" for day, role, employee in schedule_data]
    shift_dropdown.grid(row=0, column=1, pady=5)

    employee_var = tk.StringVar()
    employee_dropdown = ttk.Combobox(edit_frame, textvariable=employee_var, font=('Helvetica', 12), width=28)
    employee_dropdown['values'] = employees
    employee_dropdown.grid(row=1, column=1, pady=5)

    tk.Button(edit_frame, text="Update Shift", command=submit_edit_shift, font=('Helvetica', 12), width=15).grid(row=2, column=0, columnspan=2, pady=10)

# Function to manually fill out empty shifts
def fill_empty_shifts_form(fill_frame):
    for widget in fill_frame.winfo_children():
        widget.destroy()

    def submit_fill_shift():
        selected_shift = empty_shift_var.get().split(' - ')
        day = selected_shift[0].lower()
        role = selected_shift[1]
        new_employee = employee_var.get()
        if new_employee:
            update_shift(day, role, new_employee)
            messagebox.showinfo("Success", "Shift filled successfully")
        else:
            messagebox.showerror("Error", "Please select an employee")

    tk.Label(fill_frame, text="Select Shift and Day:", font=('Helvetica', 12)).grid(row=0, column=0, pady=5, sticky='e')
    tk.Label(fill_frame, text="Select Employee:", font=('Helvetica', 12)).grid(row=1, column=0, pady=5, sticky='e')

    schedule_data = fetch_schedule()
    employees_data = fetch_employees()

    # Create a list of shifts that are empty
    empty_shifts = [f"{day.capitalize()} - {role}" for day, role, employee in schedule_data if not employee or employee == 'control']
    print("Empty Shifts:", empty_shifts)  # Debugging output

    # Create a dropdown for empty shifts
    empty_shift_var = tk.StringVar()
    empty_shift_dropdown = ttk.Combobox(fill_frame, textvariable=empty_shift_var, font=('Helvetica', 12), width=28)
    empty_shift_dropdown['values'] = empty_shifts
    empty_shift_dropdown.grid(row=0, column=1, pady=5)

    # Create a dropdown for employees
    employee_var = tk.StringVar()
    employee_dropdown = ttk.Combobox(fill_frame, textvariable=employee_var, font=('Helvetica', 12), width=28)
    employee_dropdown.grid(row=1, column=1, pady=5)

    # Function to update the employee dropdown based on the selected shift
    def update_employee_dropdown(*args):
        selected_shift = empty_shift_var.get().split(' - ')
        day = selected_shift[0].lower()
        assigned_employees = [e[2] for e in schedule_data if e[0] == day]
        available_employees = [e[0] for e in employees_data if e[0] not in assigned_employees]
        print("Available Employees for day", day, ":", available_employees)  # Debugging output
        employee_dropdown['values'] = available_employees

    empty_shift_var.trace('w', update_employee_dropdown)

    tk.Button(fill_frame, text="Fill Shift", command=submit_fill_shift, font=('Helvetica', 12), width=15).grid(row=2, column=0, columnspan=2, pady=10)

# Function to open a window to remove an employee
def remove_employee_form(remove_frame):
    for widget in remove_frame.winfo_children():
        widget.destroy()

    def submit_remove_employee():
        name = name_var.get()
        if name:
            remove_employee(name)
            messagebox.showinfo("Success", f"Employee {name} removed successfully")
        else:
            messagebox.showerror("Error", "Please select an employee")

    tk.Label(remove_frame, text="Select Employee:", font=('Helvetica', 12)).grid(row=0, column=0, pady=5, sticky='e')

    name_var = tk.StringVar()
    name_dropdown = ttk.Combobox(remove_frame, textvariable=name_var, font=('Helvetica', 12), width=28)
    name_dropdown['values'] = [employee[0] for employee in fetch_employees()]
    name_dropdown.grid(row=0, column=1, pady=5)

    tk.Button(remove_frame, text="Remove Employee", command=submit_remove_employee, font=('Helvetica', 12), width=15).grid(row=1, column=0, columnspan=2, pady=10)

# Function to generate a new schedule
def generate_schedule():
    class Employee:
        instances = []
        def __init__(self, name, rating, hours, skills):
            self.name = name
            self.rating = rating
            self.hours = hours
            self.skills = skills.split(', ') if isinstance(skills, str) else []
            Employee.instances.append(self)

        @classmethod
        def get_instances(cls):
            return cls.instances

    employee_data = fetch_all_employees()
    for data in employee_data:
        name, rating, hours, skills = data
        Employee(name, rating, hours, skills)

    roles = [role[0] for role in fetch_roles()]

    def select_random(listname):
        return listname[random.randint(0, len(listname) - 1)]

    class Day:
        def __init__(self, role_list, employee_list):
            self.role_list = role_list.copy()
            self.employee_list = employee_list.copy()

    sunday = Day(roles, Employee.get_instances())
    monday = Day(roles, Employee.get_instances())
    tuesday = Day(roles, Employee.get_instances())
    wednsday = Day(roles, Employee.get_instances())
    thursday = Day(roles, Employee.get_instances())
    friday = Day(roles, Employee.get_instances())
    saturday = Day(roles, Employee.get_instances())

    day_list = [sunday, monday, tuesday, wednsday, thursday, friday, saturday]
    employee_A = [e for e in Employee.get_instances() if e.rating == 'A']
    employee_B = [e for e in Employee.get_instances() if e.rating == 'B']
    employee_C = [e for e in Employee.get_instances() if e.rating == 'C']

    def find_employee_for_role(role, day, employee_A, employee_B, employee_C, schedule):
        for emp_list in [employee_A, employee_B, employee_C]:
            eligible_employees = [emp for emp in emp_list if role in emp.skills and emp.hours < 40 and emp.name not in schedule.get_employees_scheduled(day)]
            if eligible_employees:
                return select_random(eligible_employees)
        return None

    class Schedule:
        def __init__(self):
            self.schedule = {day: [] for day in days}

        def add_assignment(self, day, role, employee):
            self.schedule[day].append((role, employee))
            if employee.name != 'control':
                employee.hours += 8  # Assuming each role adds 8 hours to the employee's total hours

        def get_employees_scheduled(self, day):
            return [assignment[1].name for assignment in self.schedule[day]]

        def save_to_db(self):
            conn = sqlite3.connect('schedule.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM schedule')
            for day, assignments in self.schedule.items():
                for role, employee in assignments:
                    cursor.execute('INSERT INTO schedule (day, role, employee) VALUES (?, ?, ?)', (day, role, employee.name))
            conn.commit()
            conn.close()

    # Initialize schedule
    schedule = Schedule()
    employee_list = Employee.get_instances()
    # Assign employees to roles and store in schedule
    for day_selected in day_list:
        while day_selected.role_list:
            position_selected = select_random(day_selected.role_list)
            day_name = days[day_list.index(day_selected)]
            selected_employee = find_employee_for_role(position_selected, day_name, employee_A, employee_B, employee_C, schedule)
            if selected_employee:
                schedule.add_assignment(day_name, position_selected, selected_employee)
                day_selected.role_list.remove(position_selected)
            else:
                print(f"No eligible employee found for role: {position_selected}")
                schedule.add_assignment(day_name, position_selected, employee_list[0])  # Insert empty shift into the database
                day_selected.role_list.remove(position_selected)  # Remove role if no employee is found

    # Save the schedule to the database
    schedule.save_to_db()
    messagebox.showinfo("Success", "Schedule generated successfully")

# Function to export the current schedule to an Excel file
def export_schedule():
    schedule_data = fetch_schedule()
    employees = fetch_employees()

    # Create a dictionary to hold the schedule
    schedule_dict = {day: [''] * len(employees) for day in days}
    employee_names = [employee[0] for employee in employees]

    # Populate the schedule dictionary with data
    for day, role, employee in schedule_data:
        if employee and employee != 'control':  # Only add non-empty shifts
            row = employee_names.index(employee)
            schedule_dict[day][row] = role

    # Create a DataFrame from the schedule dictionary
    df = pd.DataFrame(schedule_dict, index=employee_names)

    # Save the DataFrame to an Excel file
    df.to_excel("schedule.xlsx")

    messagebox.showinfo("Success", "Schedule exported to schedule.xlsx")

# Main window
root = tk.Tk()
root.title("Schedule Management")

# Create a notebook for tabbed interface
notebook = ttk.Notebook(root)

# Create frames for each tab
view_schedule_frame = ttk.Frame(notebook)
add_employee_frame = ttk.Frame(notebook)
update_employee_skills_frame = ttk.Frame(notebook)
edit_shift_frame = ttk.Frame(notebook)
fill_empty_shifts_frame = ttk.Frame(notebook)
generate_schedule_frame = ttk.Frame(notebook)
remove_employee_frame = ttk.Frame(notebook)
export_schedule_frame = ttk.Frame(notebook)

# Add frames to the notebook
notebook.add(view_schedule_frame, text="View Schedule")
notebook.add(add_employee_frame, text="Add Employee")
notebook.add(update_employee_skills_frame, text="Update Skills")
notebook.add(edit_shift_frame, text="Edit Shift")
notebook.add(fill_empty_shifts_frame, text="Fill Shifts")
notebook.add(generate_schedule_frame, text="Generate Schedule")
notebook.add(remove_employee_frame, text="Remove Employee")
notebook.add(export_schedule_frame, text="Export Schedule")

notebook.pack(expand=1, fill='both')

# Call the functions to populate the tabs
view_schedule(view_schedule_frame)
add_employee_form(add_employee_frame)
update_employee_skills_form(update_employee_skills_frame)
edit_shift_form(edit_shift_frame)
fill_empty_shifts_form(fill_empty_shifts_frame)
remove_employee_form(remove_employee_frame)

# Add Generate Schedule button in the generate_schedule_frame
tk.Button(generate_schedule_frame, text="Generate Schedule", command=generate_schedule, font=('Helvetica', 12), width=20, height=2).pack(pady=20)

# Add Export Schedule button in the export_schedule_frame
tk.Button(export_schedule_frame, text="Export Schedule to Excel", command=export_schedule, font=('Helvetica', 12), width=25, height=2).pack(pady=20)

root.mainloop()
