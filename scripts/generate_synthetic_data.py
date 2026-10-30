"""
CampusPulse Task 1 — Synthetic data generator
Creates reproducible, realistic synthetic college analytics CSV files.
Raw files are written to data/raw and are never modified by the validation script.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SEED = 42
rng = np.random.default_rng(SEED)

def save(df, name):
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"Created {path.relative_to(ROOT)}: {len(df):,} rows x {len(df.columns)} columns")

def main():
    departments = pd.DataFrame({
        "department_id": ["D01", "D02", "D03", "D04", "D05"],
        "department_name": ["Computer Science", "Electronics", "Mechanical", "Civil", "Electrical"]
    })
    courses = pd.DataFrame({
        "course_id": [f"C{i:03d}" for i in range(1, 16)],
        "course_name": [
            "Database Systems", "Python Programming", "Statistics", "Data Structures",
            "Operating Systems", "Computer Networks", "Digital Electronics",
            "Signals and Systems", "Microprocessors", "Thermodynamics",
            "Fluid Mechanics", "Structural Analysis", "Power Systems",
            "Control Systems", "Engineering Mathematics"
        ],
        "department_id": rng.choice(departments["department_id"], 15)
    })
    faculty = pd.DataFrame({
        "faculty_id": [f"F{i:03d}" for i in range(1, 61)],
        "faculty_name": [f"Faculty_{i:03d}" for i in range(1, 61)],
        "department_id": rng.choice(departments["department_id"], 60)
    })
    save(departments, "departments")
    save(courses, "courses")
    save(faculty, "faculty")

    n_students = 1000
    student_ids = np.array([f"S{i:05d}" for i in range(1, n_students + 1)])
    student_depts = rng.choice(departments["department_id"], n_students)
    students = pd.DataFrame({
        "student_id": student_ids,
        "student_name": [f"Student_{i:05d}" for i in range(1, n_students + 1)],
        "department_id": student_depts,
        "semester": rng.integers(1, 9, n_students),
        "admission_date": pd.to_datetime(rng.choice(pd.date_range("2022-07-01", "2026-08-31"), n_students)).strftime("%Y-%m-%d"),
        "academic_year": rng.choice(["2023-24", "2024-25", "2025-26"], n_students)
    })
    # Introduce a few intentional quality issues for the validation exercise.
    students.loc[4, "department_id"] = "D99"
    students.loc[8, "student_name"] = ""
    students.loc[12, "semester"] = 9
    students = pd.concat([students, students.iloc[[20]]], ignore_index=True)
    students.loc[len(students) - 1, "student_name"] = "Duplicate student record"
    save(students, "students")

    # Attendance: 30,000+ rows over three academic years.
    attendance_n = 30000
    att_student = rng.choice(student_ids, attendance_n)
    att_dates = pd.to_datetime(rng.choice(pd.date_range("2023-07-01", "2026-06-30"), attendance_n))
    attendance = pd.DataFrame({
        "attendance_id": [f"ATT{i:06d}" for i in range(1, attendance_n + 1)],
        "student_id": att_student,
        "course_id": rng.choice(courses["course_id"], attendance_n),
        "attendance_date": att_dates.strftime("%Y-%m-%d"),
        "status": rng.choice(["Present", "Absent", "Late", "On Leave"], attendance_n, p=[.76, .16, .05, .03]),
        "attendance_percentage": np.round(rng.uniform(55, 100, attendance_n), 2),
        "semester": rng.integers(1, 9, attendance_n)
    })
    attendance.loc[0, "attendance_percentage"] = 140
    attendance.loc[1, "student_id"] = "S99999"
    attendance.loc[2, "attendance_date"] = "2099-01-01"
    attendance.loc[3, "semester"] = 0
    # Duplicate attendance natural key.
    attendance.loc[4, ["student_id", "course_id", "attendance_date"]] = attendance.loc[5, ["student_id", "course_id", "attendance_date"]].values
    save(attendance, "attendance")

    exam_n = 5000
    exams = pd.DataFrame({
        "exam_result_id": [f"EXR{i:05d}" for i in range(1, exam_n + 1)],
        "student_id": rng.choice(student_ids, exam_n),
        "course_id": rng.choice(courses["course_id"], exam_n),
        "semester": rng.integers(1, 9, exam_n),
        "exam_type": rng.choice(["Midterm", "Final", "Practical"], exam_n),
        "marks_obtained": np.round(rng.normal(68, 16, exam_n).clip(0, 100), 2),
        "max_marks": 100
    })
    exams.loc[0, "marks_obtained"] = 125
    exams.loc[1, "student_id"] = "S88888"
    exams.loc[2, "semester"] = 10
    save(exams, "exam_results")

    assignment_n = 10000
    assignments = pd.DataFrame({
        "assignment_id": [f"ASM{i:05d}" for i in range(1, assignment_n + 1)],
        "student_id": rng.choice(student_ids, assignment_n),
        "course_id": rng.choice(courses["course_id"], assignment_n),
        "assignment_date": pd.to_datetime(rng.choice(pd.date_range("2023-07-01", "2026-06-30"), assignment_n)).strftime("%Y-%m-%d"),
        "score": np.round(rng.normal(75, 18, assignment_n).clip(0, 100), 2),
        "max_score": 100,
        "submission_status": rng.choice(["Submitted", "Late", "Missing"], assignment_n, p=[.78, .15, .07])
    })
    assignments.loc[0, "score"] = -5
    assignments.loc[1, "student_id"] = "S77777"
    save(assignments, "assignments")

    fees_n = 3000
    fees = pd.DataFrame({
        "fee_payment_id": [f"FEE{i:05d}" for i in range(1, fees_n + 1)],
        "student_id": rng.choice(student_ids, fees_n),
        "payment_date": pd.to_datetime(rng.choice(pd.date_range("2023-07-01", "2026-06-30"), fees_n)).strftime("%Y-%m-%d"),
        "fee_type": rng.choice(["Tuition", "Hostel", "Library", "Exam"], fees_n),
        "amount": np.round(rng.uniform(500, 80000, fees_n), 2),
        "payment_status": rng.choice(["Paid", "Pending", "Partially Paid"], fees_n, p=[.72, .20, .08])
    })
    fees.loc[0, "amount"] = -2500
    fees.loc[1, "student_id"] = "S66666"
    save(fees, "fees")

    leave_n = 3000
    leave_start = pd.to_datetime(rng.choice(pd.date_range("2023-07-01", "2026-06-30"), leave_n))
    leave_days = rng.integers(1, 8, leave_n)
    leaves = pd.DataFrame({
        "leave_id": [f"LVE{i:05d}" for i in range(1, leave_n + 1)],
        "student_id": rng.choice(student_ids, leave_n),
        "leave_start_date": leave_start.strftime("%Y-%m-%d"),
        "leave_end_date": (leave_start + pd.to_timedelta(leave_days, unit="D")).strftime("%Y-%m-%d"),
        "leave_type": rng.choice(["Medical", "Personal", "Family", "Other"], leave_n),
        "leave_status": rng.choice(["Approved", "Pending", "Rejected"], leave_n, p=[.7, .2, .1])
    })
    leaves.loc[0, "leave_end_date"] = "2020-01-01"  # End before start.
    leaves.loc[1, "student_id"] = "S55555"
    save(leaves, "student_leave")

    placement_n = 1000
    placements = pd.DataFrame({
        "placement_id": [f"PLC{i:05d}" for i in range(1, placement_n + 1)],
        "student_id": rng.choice(student_ids, placement_n),
        "company_name": rng.choice(["TechNova", "DataBridge", "CloudPeak", "InnoWorks", "Northstar"], placement_n),
        "placement_status": rng.choice(["Placed", "Not Placed", "In Progress", "Offer Declined"], placement_n),
        "package_lpa": np.round(rng.uniform(3, 24, placement_n), 2),
        "placement_date": pd.to_datetime(rng.choice(pd.date_range("2024-01-01", "2026-12-31"), placement_n)).strftime("%Y-%m-%d")
    })
    placements.loc[0, "placement_status"] = "Unknown"
    placements.loc[1, "student_id"] = "S44444"
    save(placements, "placements")

    
    internship_n = 500

    # Generate a start date first, then an end date on or after it.
    internship_start = pd.to_datetime(
        rng.choice(
            pd.date_range("2024-01-01", "2026-06-30"),
            internship_n
        )
    )

    # Each internship lasts between 30 and 180 days.
    internship_duration = rng.integers(30, 181, internship_n)
    internship_end = internship_start + pd.to_timedelta(
        internship_duration, unit="D"
    )

    internships = pd.DataFrame({
        "internship_id": [f"INT{i:05d}" for i in range(1, internship_n + 1)],
        "student_id": rng.choice(student_ids, internship_n),
        "organization": rng.choice(
            ["TechNova", "DataBridge", "CloudPeak", "Campus Lab"],
            internship_n
        ),
        "start_date": internship_start.strftime("%Y-%m-%d"),
        "end_date": internship_end.strftime("%Y-%m-%d"),
        "internship_status": rng.choice(
            ["Completed", "Ongoing", "Withdrawn"], internship_n
        )
    })

    # Keep one intentional issue for validation practice.
    internships.loc[0, "student_id"] = "S33333"

    save(internships, "internships")


    print("\nSynthetic data generation complete.")
    print("Raw data is in data/raw. Intentional quality issues are included for Task 1 validation practice.")

if __name__ == "__main__":
    main()
