"""
CampusPulse Task 1 — Ingestion and validation
Reads raw CSV files without modifying them, standardizes column names,
writes valid records to data/validated, invalid records to data/quarantine,
and writes data/reports/validation_summary.csv.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
VALIDATED = ROOT / "data" / "validated"
QUARANTINE = ROOT / "data" / "quarantine"
REPORTS = ROOT / "data" / "reports"

STUDENT_TABLES = {
    "attendance", "exam_results", "assignments", "fees",
    "student_leave", "placements", "internships"
}
VALID_PLACEMENT_STATUS = {"Placed", "Not Placed", "In Progress", "Offer Declined"}
VALID_ATTENDANCE_STATUS = {"Present", "Absent", "Late", "On Leave"}

def standardize_columns(df):
    df = df.copy()
    df.columns = (
        df.columns.astype(str).str.strip().str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    return df

def as_number(series):
    return pd.to_numeric(series, errors="coerce")

def validate_table(name, df, known_student_ids, known_department_ids, known_course_ids):
    df = standardize_columns(df)
    reasons = pd.Series("", index=df.index, dtype="object")

    def flag(mask, message):
        mask = pd.Series(mask, index=df.index).fillna(False)
        reasons.loc[mask] = reasons.loc[mask].apply(
            lambda old: f"{old}; {message}".strip("; ") if old else message
        )

    # Basic missing-value checks: key fields must be present.
    required = {
        "students": ["student_id", "department_id"],
        "departments": ["department_id"],
        "courses": ["course_id", "department_id"],
        "faculty": ["faculty_id", "department_id"],
        "attendance": ["attendance_id", "student_id", "course_id", "attendance_date"],
        "exam_results": ["exam_result_id", "student_id", "course_id", "marks_obtained"],
        "assignments": ["assignment_id", "student_id", "course_id", "score"],
        "fees": ["fee_payment_id", "student_id", "amount"],
        "student_leave": ["leave_id", "student_id", "leave_start_date", "leave_end_date"],
        "placements": ["placement_id", "student_id", "placement_status"],
        "internships": ["internship_id", "student_id", "start_date", "end_date"],
    }.get(name, [])
    for col in required:
        if col in df.columns:
            flag(df[col].isna() | df[col].astype(str).str.strip().eq(""), f"missing_{col}")

    # Duplicate primary keys.
    pk = {
        "students": "student_id", "departments": "department_id",
        "courses": "course_id", "faculty": "faculty_id",
        "attendance": "attendance_id", "exam_results": "exam_result_id",
        "assignments": "assignment_id", "fees": "fee_payment_id",
        "student_leave": "leave_id", "placements": "placement_id",
        "internships": "internship_id"
    }.get(name)
    if pk and pk in df.columns:
        flag(df[pk].duplicated(keep="first"), f"duplicate_{pk}")

    # Referential checks. For the students table, check department IDs.
    if "department_id" in df.columns and name != "departments":
        flag(~df["department_id"].isin(known_department_ids), "invalid_department_id")
    if name == "students" and "semester" in df.columns:
        sem = as_number(df["semester"])
        flag(~sem.between(1, 8), "invalid_semester")
    if name in STUDENT_TABLES and "student_id" in df.columns:
        flag(~df["student_id"].isin(known_student_ids), "orphan_student_id")
    if name in {"attendance", "exam_results", "assignments"} and "course_id" in df.columns:
        flag(~df["course_id"].isin(known_course_ids), "orphan_course_id")

    if name == "attendance":
        if "attendance_percentage" in df.columns:
            pct = as_number(df["attendance_percentage"])
            flag(~pct.between(0, 100), "invalid_attendance_percentage")
        if "semester" in df.columns:
            sem = as_number(df["semester"])
            flag(~sem.between(1, 8), "invalid_semester")
        if "attendance_date" in df.columns:
            dates = pd.to_datetime(df["attendance_date"], errors="coerce")
            flag(dates.isna(), "invalid_attendance_date")
            flag(dates > pd.Timestamp.today().normalize(), "future_attendance_date")
        if {"student_id", "course_id", "attendance_date"}.issubset(df.columns):
            natural_dup = df.duplicated(["student_id", "course_id", "attendance_date"], keep="first")
            flag(natural_dup, "duplicate_student_course_date")
        if "status" in df.columns:
            flag(~df["status"].isin(VALID_ATTENDANCE_STATUS), "invalid_attendance_status")

    if name == "exam_results":
        if "marks_obtained" in df.columns:
            marks = as_number(df["marks_obtained"])
            max_marks = as_number(df["max_marks"]) if "max_marks" in df.columns else 100
            flag(marks.isna() | (marks < 0) | (marks > max_marks), "invalid_marks")
        if "semester" in df.columns:
            flag(~as_number(df["semester"]).between(1, 8), "invalid_semester")

    if name == "assignments":
        if "score" in df.columns:
            score = as_number(df["score"])
            max_score = as_number(df["max_score"]) if "max_score" in df.columns else 100
            flag(score.isna() | (score < 0) | (score > max_score), "invalid_assignment_score")

    if name == "fees" and "amount" in df.columns:
        flag(as_number(df["amount"]).isna() | (as_number(df["amount"]) < 0), "invalid_fee_amount")

    if name == "student_leave":
        if {"leave_start_date", "leave_end_date"}.issubset(df.columns):
            start = pd.to_datetime(df["leave_start_date"], errors="coerce")
            end = pd.to_datetime(df["leave_end_date"], errors="coerce")
            flag(start.isna() | end.isna(), "invalid_leave_date")
            flag(end < start, "leave_end_before_start")

    if name == "placements" and "placement_status" in df.columns:
        flag(~df["placement_status"].isin(VALID_PLACEMENT_STATUS), "invalid_placement_status")

    if name == "internships" and {"start_date", "end_date"}.issubset(df.columns):
        start = pd.to_datetime(df["start_date"], errors="coerce")
        end = pd.to_datetime(df["end_date"], errors="coerce")
        flag(start.isna() | end.isna(), "invalid_internship_date")
        flag(end < start, "internship_end_before_start")

    df["validation_issues"] = reasons
    valid = df.loc[reasons.eq("")].drop(columns=["validation_issues"]).copy()
    quarantine = df.loc[~reasons.eq("")].copy()
    return valid, quarantine


def main():
    if not RAW.exists():
        raise FileNotFoundError(
            f"Raw data folder not found: {RAW}. "
            "Run scripts/generate_synthetic_data.py first."
        )

    VALIDATED.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    files = sorted(RAW.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {RAW}.")

    raw_tables = {}
    for path in files:
        raw_tables[path.stem] = standardize_columns(
            pd.read_csv(path)
        )

    summary = []

    def process_table(
        name,
        known_student_ids,
        known_department_ids,
        known_course_ids,
    ):
        if name not in raw_tables:
            return pd.DataFrame()

        raw_df = raw_tables[name]

        valid, quarantine = validate_table(
            name,
            raw_df,
            known_student_ids,
            known_department_ids,
            known_course_ids,
        )

        valid.to_csv(
            VALIDATED / f"{name}.csv",
            index=False,
        )
        quarantine.to_csv(
            QUARANTINE / f"{name}_quarantine.csv",
            index=False,
        )

        raw_rows = len(raw_df)
        valid_rows = len(valid)
        quarantine_rows = len(quarantine)

        status = "PASS" if quarantine_rows == 0 else "WARN"

        summary.append({
            "table_name": name,
            "raw_rows": raw_rows,
            "valid_rows": valid_rows,
            "quarantined_rows": quarantine_rows,
            "status": status,
        })

        print(
            f"{name:18} raw={raw_rows:>7,} "
            f"valid={valid_rows:>7,} "
            f"quarantined={quarantine_rows:>6,} "
            f"[{status}]"
        )

        return valid

    # 1. Validate departments first.
    valid_departments = process_table(
        "departments", set(), set(), set()
    )
    known_department_ids = (
        set(valid_departments["department_id"].dropna())
        if "department_id" in valid_departments.columns
        else set()
    )

    # 2. Validate courses and faculty against valid departments.
    valid_courses = process_table(
        "courses", set(), known_department_ids, set()
    )
    process_table(
        "faculty", set(), known_department_ids, set()
    )

    known_course_ids = (
        set(valid_courses["course_id"].dropna())
        if "course_id" in valid_courses.columns
        else set()
    )

    # 3. Validate students against valid departments.
    valid_students = process_table(
        "students", set(), known_department_ids, known_course_ids
    )
    known_student_ids = (
        set(valid_students["student_id"].dropna())
        if "student_id" in valid_students.columns
        else set()
    )

    # 4. Validate dependent tables against valid student IDs.
    dependent_tables = [
        "attendance",
        "exam_results",
        "assignments",
        "fees",
        "student_leave",
        "placements",
        "internships",
    ]

    for name in dependent_tables:
        process_table(
            name,
            known_student_ids,
            known_department_ids,
            known_course_ids,
        )

    report = pd.DataFrame(summary).sort_values("table_name")
    report.to_csv(
        REPORTS / "validation_summary.csv",
        index=False,
    )

    print(
        f"\nValidation summary saved to: "
        f"{REPORTS / 'validation_summary.csv'}"
    )
    print(
        "Raw files were not modified. "
        "Review quarantine CSVs for validation_issues."
    )


if __name__ == "__main__":
    main()

