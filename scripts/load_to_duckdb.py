
from pathlib import Path
import duckdb

# Find the main CampusPulse project folder
ROOT = Path(__file__).resolve().parent.parent

# Folder containing the validated CSV files
VALIDATED = ROOT / "data" / "validated"

# Location of the DuckDB database file
DB_PATH = ROOT / "campuspulse.duckdb"


def main():
    # Connect to the database (create it if it doesn't exist)
    con = duckdb.connect(str(DB_PATH))

    try:
        # Load each validated CSV file into a database table
        for csv_path in sorted(VALIDATED.glob("*.csv")):
            table_name = csv_path.stem

            con.execute(
                f"""
                CREATE OR REPLACE TABLE "{table_name}" AS
                SELECT *
                FROM read_csv_auto(?)
                """,
                [str(csv_path)]
            )

            row_count = con.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).fetchone()[0]

            print(f"Loaded {table_name}: {row_count:,} rows")

        print(f"\nDatabase created at: {DB_PATH}")

    finally:
        con.close()


if __name__ == "__main__":
    main()
