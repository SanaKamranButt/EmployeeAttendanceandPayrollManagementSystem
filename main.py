import json
import os
from attendance import check_in, check_out, attendance_history
from payroll import calculate_salary, payroll_report
from report import export_csv, export_pdf
from getpass import getpass

EMPLOYEE_FILE = "employees.json"


# ----------------------------
# Employee Class
# ----------------------------
class Employee:
    def __init__(self, emp_id, name, password, designation,
                 basic_salary, hourly_rate):
        self.emp_id = emp_id
        self.name = name
        self.password = password
        self.designation = designation
        self.basic_salary = basic_salary
        self.hourly_rate = hourly_rate

    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "password": self.password,
            "designation": self.designation,
            "basic_salary": self.basic_salary,
            "hourly_rate": self.hourly_rate
        }


# ----------------------------
# Database Functions
# ----------------------------

def load_employees():

    if not os.path.exists(EMPLOYEE_FILE):
        return []

    try:
        with open(EMPLOYEE_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
            return []


def save_employees(data):

    with open(EMPLOYEE_FILE, "w") as file:
        json.dump(data, file, indent=4)


# ----------------------------
# Employee Functions
# ----------------------------

def add_employee():



    employees = load_employees()
    emp_id = f"EMP{len(employees) + 1:03d}"
    print("Generated Employee ID:", emp_id)

    for emp in employees:
        if emp["emp_id"] == emp_id:
            print("Employee already exists.")
            return

    name = input("Employee Name : ")
    password = input("Password : ")
    designation = input("Designation : ")

    try:
        basic_salary = float(input("Basic Salary : "))
        hourly_rate = float(input("Hourly Rate : "))
    except ValueError:
        print("Please enter valid numeric values.")
        return

    employee = Employee(
        emp_id,
        name,
        password,
        designation,
        basic_salary,
        hourly_rate
    )

    employees.append(employee.to_dict())

    save_employees(employees)

    print("\nEmployee Added Successfully.")
    print(f"Employee ID: {emp_id}\n")


def view_employees():

    employees = load_employees()

    if len(employees) == 0:
        print("No Employee Found.")
        return

    print("\n------ Employee List ------\n")

    for emp in employees:

        print("ID :", emp["emp_id"])
        print("Name :", emp["name"])
        print("Designation :", emp["designation"])
        print("Salary :", emp["basic_salary"])
        print("-" * 30)


def search_employee():

    employees = load_employees()

    keyword = input("Enter Employee ID or Name: ").strip().lower()

    for emp in employees:

        if (emp["emp_id"].lower() == keyword or
                emp["name"].lower() == keyword):

            print("\nEmployee Found\n")
            print("ID :", emp["emp_id"])
            print("Name :", emp["name"])
            print("Designation :", emp["designation"])
            print("Salary :", emp["basic_salary"])
            return

    print("Employee Not Found.")


# ----------------------------
# Login
# ----------------------------

def login():

    employees = load_employees()

    emp_id = input("Employee ID : ")
    password = input("Password : ")

    for emp in employees:

        if emp["emp_id"] == emp_id and emp["password"] == password:

            print(f"\nWelcome {emp['name']}!")
            employee_dashboard(emp["emp_id"])
            return

    print("Invalid Login")

def employee_dashboard(emp_id):

    while True:

        print("\n========== Employee Dashboard ==========")
        print("1. Check In")
        print("2. Check Out")
        print("3. View Attendance")
        print("4. Calculate Salary")
        print("5. Logout")

        choice = input("Enter Choice : ")

        if choice == "1":
            check_in(emp_id)

        elif choice == "2":
            check_out(emp_id)

        elif choice == "3":
            attendance_history(emp_id)

        elif choice == "4":
            calculate_salary(emp_id)

        elif choice == "5":
            print("Logged Out Successfully.")
            break

        else:
            print("Invalid Choice.")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
def admin_login():


    username = input("Admin Username : ")
    password = input("Password : ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        while True:

            print("\n========== ADMIN PANEL ==========")
            print("1. Add Employee")
            print("2. View Employees")
            print("3. Search Employee")
            print("4. Payroll Report")
            print("5. Export CSV")
            print("6. Export PDF")
            print("7. Logout")

            choice = input("Choice : ")

            if choice == "1":
                add_employee()

            elif choice == "2":
                view_employees()

            elif choice == "3":
                search_employee()

            elif choice == "4":
                payroll_report()

            elif choice == "5":
                export_csv()

            elif choice == "6":
                export_pdf()

            elif choice == "7":
                break

            else:
                print("Invalid Choice.")

    else:

        print("Invalid Admin Credentials.")

# ----------------------------
# Main Menu
# ----------------------------

if __name__ == "__main__":
    while True:
        try:
            print("\n===============================")
            print(" Employee Attendance & Payroll ")
            print("===============================")
            print("1. Admin Login")
            print("2. Employee Login")
            print("3. Exit")

            choice = input("Enter Choice : ")

            if choice == "1":
                admin_login()

            elif choice == "2":
                login()

            elif choice == "3":
                print("Thank You")
                break

            else:
                print("Invalid Choice")

        except Exception as e:
            print("Error:", e)