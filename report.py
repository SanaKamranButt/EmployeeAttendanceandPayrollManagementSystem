import csv
import os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from payroll import load_employees, calculate_salary

REPORT_FOLDER = "reports"

if not os.path.exists(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)


def export_csv():

    employees = load_employees()

    filename = os.path.join(REPORT_FOLDER, "payroll.csv")

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Employee ID",
            "Employee Name",
            "Designation",
            "Basic Salary",
            "Hours Worked",
            "Overtime Hours",
            "Overtime Pay",
            "Net Salary"
        ])

        for emp in employees:

            payroll = calculate_salary(emp["emp_id"])

            if payroll:

                writer.writerow([
                    emp["emp_id"],
                    payroll["Employee"],
                    payroll["Designation"],
                    payroll["Basic Salary"],
                    payroll["Hours"],
                    payroll["Overtime"],
                    payroll["Overtime Pay"],
                    payroll["Net Salary"]
                ])

    print("\nCSV Report Exported Successfully.")
    print(filename)


def export_pdf():

    employees = load_employees()

    filename = os.path.join(REPORT_FOLDER, "payroll.pdf")

    document = SimpleDocTemplate(filename)

    table_data = [[
        "ID",
        "Name",
        "Designation",
        "Basic",
        "Hours",
        "OT",
        "OT Pay",
        "Net Salary"
    ]]

    for emp in employees:

        payroll = calculate_salary(emp["emp_id"])

        if payroll:

            table_data.append([
                emp["emp_id"],
                payroll["Employee"],
                payroll["Designation"],
                payroll["Basic Salary"],
                payroll["Hours"],
                payroll["Overtime"],
                payroll["Overtime Pay"],
                payroll["Net Salary"]
            ])

    table = Table(table_data)

    table.setStyle(TableStyle([

        ('BACKGROUND',(0,0),(-1,0),colors.darkblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.white),

        ('GRID',(0,0),(-1,-1),1,colors.black),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),

        ('BOTTOMPADDING',(0,0),(-1,0),12),

        ('BACKGROUND',(0,1),(-1,-1),colors.beige)

    ]))

    document.build([table])

    print("\nPDF Report Exported Successfully.")
    print(filename)