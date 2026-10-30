
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "campuspulse.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    tables_to_check = [
        "attendance",
        "exam_results",
        "assignments",
        "fees",
        "student_leave",
        "internships",
        "placements",
    ]

    print("Unmatched student references:")
    print("-" * 45)

    for table_name in tables_to_check:
        query = f"""
            SELECT COUNT(*)
            FROM "{table_name}" AS records
            LEFT JOIN students AS s
                ON records.student_id = s.student_id
            WHERE s.student_id IS NULL
        """

        count = con.execute(query).fetchone()[0]
        print(f"{table_name}: {count:,}")

finally:
    con.close()
