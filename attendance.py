import json
import os
from datetime import datetime

ATTENDANCE_FILE = "attendance.json"


def load_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        return []

    try:
        with open(ATTENDANCE_FILE, "r") as file:
            return json.load(file)
    except:
        return []


def save_attendance(data):
    with open(ATTENDANCE_FILE, "w") as file:
        json.dump(data, file, indent=4)


def check_in(emp_id):

    attendance = load_attendance()

    today = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")

    for record in attendance:
        if record["emp_id"] == emp_id and record["date"] == today:
            print("Already Checked In")
            return

    attendance.append(
        {
            "emp_id": emp_id,
            "date": today,
            "check_in": time,
            "check_out": "",
            "hours": 0
        }
    )

    save_attendance(attendance)

    print("Check In Successful")


def check_out(emp_id):

    attendance = load_attendance()

    today = datetime.now().strftime("%Y-%m-%d")
    current = datetime.now()

    for record in attendance:

        if record["emp_id"] == emp_id and record["date"] == today:

            if record["check_out"] != "":
                print("Already Checked Out")
                return

            checkin = datetime.strptime(
                record["date"] + " " + record["check_in"],
                "%Y-%m-%d %H:%M:%S"
            )

            hours = (current - checkin).total_seconds() / 3600

            record["check_out"] = current.strftime("%H:%M:%S")
            record["hours"] = round(hours, 2)

            save_attendance(attendance)

            print("Check Out Successful")
            print("Hours Worked :", round(hours,2))
            return

    print("Check In First")


def attendance_history(emp_id):

    attendance = load_attendance()

    print("\nAttendance History\n")

    found = False

    for record in attendance:

        if record["emp_id"] == emp_id:

            found = True

            print("-----------------------------")
            print("Date :", record["date"])
            print("Check In :", record["check_in"])
            print("Check Out :", record["check_out"])
            print("Hours :", record["hours"])

    if not found:
        print("No Record Found")