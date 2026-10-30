
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "campuspulse.duckdb"

con = duckdb.connect(str(DB_PATH), read_only=True)

try:
    tables = con.execute("SHOW TABLES").fetchall()

    print("Tables in CampusPulse database:")
    for table in tables:
        print("-", table[0])

    print("\nRow counts:")
    for (table_name,) in tables:
        count = con.execute(
            f'SELECT COUNT(*) FROM "{table_name}"'
        ).fetchone()[0]

        print(f"{table_name}: {count:,} rows")

finally:
    con.close()
