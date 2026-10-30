
from pathlib import Path
import duckdb

# Locate the project folders and database
ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "campuspulse.duckdb"
SQL_DIR = ROOT / "sql"
REPORT_DIR = ROOT / "data" / "reports" / "sql_results"

# Create the results folder if it doesn't exist
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Map each saved SQL file to its output CSV filename
analyses = {
    "01_student_count_by_department.sql":
        "student_count_by_department.csv",
    "02_attendance_rate_by_department.sql":
        "attendance_rate_by_department.csv",
     "03_average_exam_score_by_department.sql":
        "average_exam_score_by_department.csv",
    "04_fee_payment_analysis.sql":
        "fee_payment_analysis.csv",
    "05_assignment_performance_by_department.sql":
        "assignment_performance_by_department.csv",
    "06_student_leave_analysis.sql":
        "student_leave_analysis.csv",
    "07_internship_analysis.sql": "internship_analysis.csv",
    "08_placement_analysis.sql": "placement_analysis.csv",
}

# Open the database in read-only mode
connection = duckdb.connect(str(DB_PATH), read_only=True)

try:
    for sql_file, csv_file in analyses.items():
        query_path = SQL_DIR / sql_file
        output_path = REPORT_DIR / csv_file

        # Read the SQL query from its file
        query = query_path.read_text(encoding="utf-8")

        # Execute the query and retrieve its result
        result = connection.execute(query).fetchdf()

        # Save the result as a CSV report
        result.to_csv(output_path, index=False)

        print(f"Analysis completed: {sql_file}")
        print(f"Rows returned: {len(result)}")
        print(f"Report saved: {output_path.relative_to(ROOT)}")
        print("-" * 50)

finally:
    connection.close()
