import json
import os
from attendance import load_attendance
from datetime import datetime

EMPLOYEE_FILE = "employees.json"


def load_employees():
    if not os.path.exists(EMPLOYEE_FILE):
        return []

    with open(EMPLOYEE_FILE, "r") as file:
        return json.load(file)


def calculate_salary(emp_id):

    employees = load_employees()
    attendance = load_attendance()

    employee = None

    for emp in employees:
        if emp["emp_id"] == emp_id:
            employee = emp
            break

    if employee is None:
        print("Employee Not Found")
        return

    total_hours = 0
    overtime = 0

    current_month = datetime.now().strftime("%Y-%m")

    for record in attendance:

        if record["emp_id"] == emp_id:

            if record["date"].startswith(current_month):

                total_hours += record["hours"]

                if record["hours"] > 8:
                    overtime += record["hours"] - 8

    overtime_pay = overtime * employee["hourly_rate"]

    total_salary = employee["basic_salary"] + overtime_pay

    print("\n========= Payroll =========")
    print("Employee :", employee["name"])
    print("Designation :", employee["designation"])
    print("Basic Salary :", employee["basic_salary"])
    print("Total Hours :", round(total_hours, 2))
    print("Overtime Hours :", round(overtime, 2))
    print("Overtime Pay :", round(overtime_pay, 2))
    print("Net Salary :", round(total_salary, 2))

    return {
        "Employee": employee["name"],
        "Designation": employee["designation"],
        "Basic Salary": employee["basic_salary"],
        "Hours": total_hours,
        "Overtime": overtime,
        "Overtime Pay": overtime_pay,
        "Net Salary": total_salary
    }


def payroll_report():

    employees = load_employees()

    print("\n========== Monthly Payroll ==========\n")

    for emp in employees:

        data = calculate_salary(emp["emp_id"])

        print("-------------------------------------")