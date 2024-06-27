# Schedule Management Application

This application is designed to manage employee schedules, including adding and updating employee information, assigning shifts, and exporting schedules to Excel.

## Features

- **View Current Schedule**: Display the current schedule in a grid format with employee names on the left and days of the week on top.
- **Add New Employee**: Add a new employee to the database, including selecting their skills.
- **Update Employee Skills**: Update the skills of existing employees.
- **Edit Specific Shift**: Edit an assigned shift, selecting a new employee for the shift.
- **Fill Empty Shifts**: Manually fill out empty shifts.
- **Generate Schedule**: Automatically generate a new schedule based on employee availability and skills.
- **Remove Employee**: Remove an employee from the database.
- **Export Schedule to Excel**: Export the current schedule to an Excel file.

## Requirements

- Python 3.x
- SQLite3
- Tkinter
- Pandas
- Openpyxl

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/jeremiahwarinner/Schedule-Manager.git
    cd schedule-management
    ```

2. **Install the required packages**:
    ```sh
    pip install pandas openpyxl
    ```

3. **Create the SQLite database**:
    - You need to create an SQLite database named `schedule.db` with the appropriate tables:
    ```sql
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        rating TEXT NOT NULL,
        hours INTEGER NOT NULL,
        skills TEXT NOT NULL
    );

    CREATE TABLE roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    CREATE TABLE schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT NOT NULL,
        role TEXT NOT NULL,
        employee TEXT
    );
    ```

## Usage

1. **Run the application**:
    ```sh
    python branch6.py
    ```

2. **Use the tabs** to navigate between different functionalities:
    - **View Schedule**: View the current schedule and refresh it as needed.
    - **Add Employee**: Add a new employee by entering their name, rating, and selecting their skills.
    - **Update Skills**: Update the skills of existing employees by selecting their name and modifying their skills.
    - **Edit Shift**: Edit specific shifts by selecting the current shift and choosing a new employee.
    - **Fill Shifts**: Manually fill out empty shifts by selecting the shift and assigning an available employee.
    - **Generate Schedule**: Automatically generate a new schedule based on employee availability and skills.
    - **Remove Employee**: Remove an employee from the database.
    - **Export Schedule**: Export the current schedule to an Excel file.

## Screenshots

**Schedule Viewer**
<img width="659" alt="scheduletab" src="https://github.com/jeremiahwarinner/Schedule-Manager/assets/158241209/50fe9b23-c28a-42e4-afb7-3fa8efe99867">

**Edit Shifts**
<img width="659" alt="editshifts" src="https://github.com/jeremiahwarinner/Schedule-Manager/assets/158241209/ba2f1d4d-a452-489d-9792-227eb95b4767">

**Add Employee**
<img width="659" alt="addemployeetab" src="https://github.com/jeremiahwarinner/Schedule-Manager/assets/158241209/8d37b30f-beeb-4483-a5f9-43dac5f8bbe5">

**Manually Fill Empty Shifts**
<img width="659" alt="fillemptyshifts" src="https://github.com/jeremiahwarinner/Schedule-Manager/assets/158241209/e9bab541-7a86-480b-a710-b5c6bccab0f2">

**Remove Employee**
<img width="659" alt="removeemployee" src="https://github.com/jeremiahwarinner/Schedule-Manager/assets/158241209/265caab2-bb3b-4a60-8095-927dc3296aba">

**Update Skills**
<img width="659" alt="updateskillstab" src="https://github.com/jeremiahwarinner/Schedule-Manager/assets/158241209/a16773b4-4e3d-4884-8d07-f205078e5c97">




## Contributing

1. **Fork the repository**.
2. **Create a new branch**: `git checkout -b my-feature-branch`.
3. **Commit your changes**: `git commit -m 'Add some feature'`.
4. **Push to the branch**: `git push origin my-feature-branch`.
5. **Create a pull request**.
