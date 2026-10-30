
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "campuspulse.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    query = """
        SELECT student_id, validation_issues
        FROM read_csv_auto(?)
        WHERE student_id IN (
            SELECT DISTINCT a.student_id
            FROM attendance a
            LEFT JOIN students s
                ON a.student_id = s.student_id
            WHERE s.student_id IS NULL

            UNION

            SELECT DISTINCT e.student_id
            FROM exam_results e
            LEFT JOIN students s
                ON e.student_id = s.student_id
            WHERE s.student_id IS NULL

            UNION

            SELECT DISTINCT a.student_id
            FROM assignments a
            LEFT JOIN students s
                ON a.student_id = s.student_id
            WHERE s.student_id IS NULL

            UNION

            SELECT DISTINCT f.student_id
            FROM fees f
            LEFT JOIN students s
                ON f.student_id = s.student_id
            WHERE s.student_id IS NULL

            UNION

            SELECT DISTINCT l.student_id
            FROM student_leave l
            LEFT JOIN students s
                ON l.student_id = s.student_id
            WHERE s.student_id IS NULL

            UNION

            SELECT DISTINCT p.student_id
            FROM placements p
            LEFT JOIN students s
                ON p.student_id = s.student_id
            WHERE s.student_id IS NULL
        )
        ORDER BY student_id
    """

    quarantine_path = str(
        ROOT / "data" / "quarantine" / "students_quarantine.csv"
    )

    results = con.execute(query, [quarantine_path]).fetchall()

    print("Quarantined students linked to unmatched records:")
    for student_id, reason in results:
        print(f"{student_id}: {reason}")

    print(f"\nNumber of affected student IDs: {len(results)}")

finally:
    con.close()
