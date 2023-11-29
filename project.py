import os, sqlite3, validators
from pyfiglet import Figlet
from tabulate import tabulate
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        # Logo
        self.image("harvard.png", 10, 8, 20)
        # Arial bold 15
        self.set_font("helvetica", "B", 30)
        # Title
        self.cell(0, 10, "CS50P Employees Data", border=0, align="C")
        # Line break
        self.ln(20)


# Connect to the SQLite3 database
def connect_to_database():
    try:
        connection = sqlite3.connect("employees.db")
        cursor = connection.cursor()
        return connection, cursor
    except sqlite3.Error:
        print("Error connecting to the database")


# Create the employees table in the SQLite3 database
def create_employees_table(cursor):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT,
            salary REAL,
            phone_number TEXT,
            email TEXT
        )
    """
    )
    cursor.connection.commit()


# Consult a specific employee informations
def consult_employee(cursor):
    employee_name = input("Input employee name: ")

    cursor.execute("SELECT * FROM employees WHERE name = ?", [employee_name])
    employee = cursor.fetchone()
    if employee:
        print("\nEmployee Information:")
        print(f"ID: {employee[0]}")
        print(f"Name: {employee[1]}")
        print(f"Position: {employee[2]}")
        print(f"Salary: {employee[3]}")
        print(f"Phone: {employee[4]}")
        print(f"Email: {employee[5]}")
    else:
        print("Employee not found.")

    print("\nEmployee information displayed successfully.")


# List employees from the SQLite3 database
def list_employees(cursor):
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    print("\nListing employees...")
    print(
        tabulate(
            employees,
            headers=["ID", "Name", "Position", "Salary", "Phone Number", "E-mail"],
            tablefmt="rounded_outline",
        )
    )


# Add an employee to the SQLite3 database
def add_employee(cursor):
    email = ""
    name = input("\nEnter employee name: ")
    position = input("Enter employee position: ")

    while True:
        try:
            salary = float(input("Enter employee salary: ").replace(" ", ""))
            salary = "$" + f"{salary:.2f}"
            break
        except ValueError:
            print("Invalid Value. Input salary value again.")
            continue

    phone_number = input("Enter employee phone number: ")
    while True:
        email = input("Enter employee e-mail: ")
        if validators.email(email):
            break
        else:
            print("Please enter a valid e-mail")

    cursor.execute(
        "INSERT INTO employees (name, position, salary, phone_number, email) VALUES (?, ?, ?, ?, ?)",
        (name, position, salary, phone_number, email),
    )
    cursor.connection.commit()
    print("\nEmployee added successfully.")


# Update information for an employee in the SQLite3 database
def update_employee(cursor):
    email = ""
    employee_id = input("\nEnter the ID of the employee to update: ")
    name = input("Enter new employee name: ")
    position = input("Enter new employee position: ")

    while True:
        try:
            salary = float(input("Enter employee salary: ").replace(" ", ""))
            salary = "$" + f"{salary:.2f}"
            break
        except ValueError:
            print("Invalid Value. Input salary value again.")
            continue

    phone_number = input("Enter employee phone number: ")
    while not validators.email(email):
        email = input("Enter employee e-mail: ")
        print("Please enter a valid e-mail")

    cursor.execute(
        "UPDATE employees SET name=?, position=?, salary=?, phone_number=?, email=? WHERE id=?",
        (name, position, salary, phone_number, email, employee_id),
    )
    cursor.connection.commit()
    print("\nEmployee information updated successfully.")


# Remove an employee from the SQLite3 database
def remove_employee(cursor):
    employee_id = input("Enter the ID of the employee to remove: ")
    cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
    cursor.connection.commit()
    print("\nEmployee removed successfully.")


# Create a PDF report with employee data
def create_pdf(cursor):
    pdf = PDF(orientation="L", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Times", "", 12)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    pdf.ln(10)

    columns = ["Id", "Name", "Position", "Salary", "Phone", "Email"]
    col_widths = [30, 50, 50, 30, 30, 80]

    for col, width in zip(columns, col_widths):
        pdf.cell(width, 10, col, 1)
    pdf.ln()

    for employee in employees:
        for value, width in zip(employee, col_widths):
            pdf.cell(width, 10, str(value), 1)
        pdf.ln()

    pdf.output("employees_data.pdf")
    print("\nPDF file created.")


# Close the connection to the SQLite3 database
def close_database(connection):
    connection.close()


# Main program
def main():
    connection, cursor = connect_to_database()
    create_employees_table(cursor)

    os.system("clear")
    figlet = Figlet()
    figlet.setFont(font="small")
    print(figlet.renderText("CS50P Employee Management"))

    while True:
        show_menu()
        choice = input("Choose an option (1-7): ")

        if choice == "1":
            consult_employee(cursor)
        elif choice == "2":
            list_employees(cursor)
        elif choice == "3":
            add_employee(cursor)
        elif choice == "4":
            update_employee(cursor)
        elif choice == "5":
            remove_employee(cursor)
        elif choice == "6":
            create_pdf(cursor)
        elif choice == "7":
            print("\nExiting the program. Goodbye!\n")
            close_database(connection)
            break
        else:
            input("\nInvalid option. Press Enter to continue...")


# Function to display the menu options
def show_menu():
    options = [
        {"Option": 1, "Description": "Consult Employee info"},
        {"Option": 2, "Description": "List Employees"},
        {"Option": 3, "Description": "Add Employee"},
        {"Option": 4, "Description": "Update Employee Info"},
        {"Option": 5, "Description": "Remove Employee"},
        {"Option": 6, "Description": "Create PDF with Employees Data"},
        {"Option": 7, "Description": "Exit"},
    ]
    print()
    print(tabulate(options, tablefmt="rounded_outline"))


# Entry point of the script
if __name__ == "__main__":
    main()
