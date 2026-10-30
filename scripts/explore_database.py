from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "campuspulse.duckdb"

connection = duckdb.connect(str(DB_PATH), read_only=True)

try:
    # 1. Validate internship-to-student relationships
    internship_query = """
    SELECT
        COUNT(*) AS unmatched_student_records
    FROM internships AS i
    LEFT JOIN students AS s
        ON i.student_id = s.student_id
    WHERE s.student_id IS NULL;
    """

    print("\n--- INTERNSHIP STUDENT-REFERENCE VALIDATION ---")
    result = connection.execute(internship_query).fetchdf()
    print(result.to_string(index=False))

    # 2. Inspect the placements table structure
    print("\n--- PLACEMENTS TABLE STRUCTURE ---")
    print(
        connection.execute("DESCRIBE placements")
        .fetchdf()
        .to_string(index=False)
    )

    # 3. Inspect placement-status distribution
    print("\n--- PLACEMENT STATUS DISTRIBUTION ---")
    status_query = """
    SELECT
        placement_status,
        COUNT(*) AS placement_count
    FROM placements
    GROUP BY placement_status
    ORDER BY placement_count DESC;
    """

    print(
        connection.execute(status_query)
        .fetchdf()
        .to_string(index=False)
    )
        # 4. Validate placement data quality
    print("\n--- PLACEMENT DATA QUALITY VALIDATION ---")

    quality_query = """
    SELECT
        COUNT(*) AS total_records,

        COUNT(DISTINCT placement_id)
            AS unique_placement_ids,

        SUM(
            CASE
                WHEN placement_id IS NULL
                  OR TRIM(placement_id) = ''
                THEN 1 ELSE 0
            END
        ) AS missing_placement_ids,

        SUM(
            CASE
                WHEN student_id IS NULL
                  OR TRIM(student_id) = ''
                THEN 1 ELSE 0
            END
        ) AS missing_student_ids,

        SUM(
            CASE
                WHEN company_name IS NULL
                  OR TRIM(company_name) = ''
                THEN 1 ELSE 0
            END
        ) AS missing_company_names,

        SUM(
            CASE
                WHEN placement_status IS NULL
                  OR TRIM(placement_status) = ''
                  OR placement_status NOT IN (
                      'In Progress',
                      'Placed',
                      'Offer Declined',
                      'Not Placed'
                  )
                THEN 1 ELSE 0
            END
        ) AS unexpected_status_records,

        SUM(
            CASE
                WHEN package_lpa IS NULL
                THEN 1 ELSE 0
            END
        ) AS missing_packages,

        SUM(
            CASE
                WHEN package_lpa < 0
                THEN 1 ELSE 0
            END
        ) AS negative_packages,

        SUM(
            CASE
                WHEN placement_date IS NULL
                THEN 1 ELSE 0
            END
        ) AS missing_placement_dates

    FROM placements;
    """

    print(
        connection.execute(quality_query)
        .fetchdf()
        .to_string(index=False)
    )

    # 5. Validate placement-to-student relationships
    print("\n--- PLACEMENT STUDENT-REFERENCE VALIDATION ---")

    unmatched_query = """
    SELECT
        COUNT(*) AS unmatched_student_records

    FROM placements AS p

    LEFT JOIN students AS s
        ON p.student_id = s.student_id

    WHERE p.student_id IS NOT NULL
      AND s.student_id IS NULL;
    """

    print(
        connection.execute(unmatched_query)
        .fetchdf()
        .to_string(index=False)
    )
        # 6. Identify students with multiple placement records
    print("\n--- STUDENTS WITH MULTIPLE PLACEMENT RECORDS ---")

    multiple_placements_query = """
    SELECT
        student_id,
        COUNT(*) AS placement_record_count,
        COUNT(DISTINCT placement_status) AS distinct_status_count

    FROM placements

    WHERE student_id IS NOT NULL
      AND TRIM(student_id) <> ''

    GROUP BY student_id

    HAVING COUNT(*) > 1

    ORDER BY placement_record_count DESC, student_id;
    """

    print(
        connection.execute(multiple_placements_query)
        .fetchdf()
        .to_string(index=False)
    )
        # 7. Summarize placement records at student level
    print("\n--- PLACEMENT RECORDS SUMMARY BY STUDENT ---")

    student_summary_query = """
    WITH student_counts AS (
        SELECT
            student_id,
            COUNT(*) AS placement_record_count
        FROM placements
        GROUP BY student_id
    )
    SELECT
        SUM(placement_record_count) AS total_placement_records,
        COUNT(*) AS unique_students_with_placements,

        SUM(
            CASE
                WHEN placement_record_count = 1
                THEN 1 ELSE 0
            END
        ) AS students_with_one_record,

        SUM(
            CASE
                WHEN placement_record_count > 1
                THEN 1 ELSE 0
            END
        ) AS students_with_multiple_records

    FROM student_counts;
    """

    print(
        connection.execute(student_summary_query)
        .fetchdf()
        .to_string(index=False)
    )

    # 8. Count placement records and distinct students by status
    print("\n--- PLACEMENT STATUS: RECORDS VS UNIQUE STUDENTS ---")

    status_summary_query = """
    SELECT
        placement_status,
        COUNT(*) AS placement_records,
        COUNT(DISTINCT student_id) AS distinct_students

    FROM placements

    GROUP BY placement_status

    ORDER BY placement_records DESC;
    """

    print(
        connection.execute(status_summary_query)
        .fetchdf()
        .to_string(index=False)
    )
        # 9. Analyze combinations of placement statuses per student
    print("\n--- PLACEMENT STATUS COMBINATIONS BY STUDENT ---")

    status_combinations_query = """
    WITH student_statuses AS (
        SELECT
            student_id,
            COUNT(*) AS placement_record_count,
            COUNT(DISTINCT placement_status) AS distinct_status_count,
            STRING_AGG(
                DISTINCT placement_status,
                ', ' ORDER BY placement_status
            ) AS status_combination,
            COUNT(DISTINCT company_name) AS distinct_companies

        FROM placements

        WHERE student_id IS NOT NULL
          AND TRIM(student_id) <> ''

        GROUP BY student_id
    )

    SELECT
        status_combination,
        COUNT(*) AS student_count,
        SUM(placement_record_count) AS total_placement_records,
        ROUND(AVG(placement_record_count), 2)
            AS avg_records_per_student

    FROM student_statuses

    GROUP BY status_combination

    ORDER BY student_count DESC;
    """

    print(
        connection.execute(status_combinations_query)
        .fetchdf()
        .to_string(index=False)
    )
        # 10. Inspect placement records for students with multiple statuses
    print("\n--- DETAILED PLACEMENT RECORDS FOR MULTI-STATUS STUDENTS ---")

    placement_history_query = """
    WITH multi_status_students AS (
        SELECT student_id
        FROM placements
        WHERE student_id IS NOT NULL
          AND TRIM(student_id) <> ''
        GROUP BY student_id
        HAVING COUNT(DISTINCT placement_status) > 1
    )
    SELECT
        p.student_id,
        p.placement_id,
        p.company_name,
        p.placement_status,
        p.package_lpa,
        p.placement_date
    FROM placements AS p
    INNER JOIN multi_status_students AS m
        ON p.student_id = m.student_id
    ORDER BY
        p.student_id,
        p.placement_date,
        p.company_name
    LIMIT 50;
    """

    print(
        connection.execute(placement_history_query)
        .fetchdf()
        .to_string(index=False)
    )
        # 11. Check future placement dates
    print("\n--- FUTURE PLACEMENT DATE VALIDATION ---")

    future_dates_query = """
    SELECT
        COUNT(*) AS future_dated_records,
        MIN(placement_date) AS earliest_future_date,
        MAX(placement_date) AS latest_future_date
    FROM placements
    WHERE placement_date > CURRENT_DATE;
    """

    print(
        connection.execute(future_dates_query)
        .fetchdf()
        .to_string(index=False)
    )
        # 12. Analyze package values by placement status
    print("\n--- PACKAGE ANALYSIS BY PLACEMENT STATUS ---")

    package_query = """
    SELECT
        placement_status,
        COUNT(*) AS total_records,
        COUNT(package_lpa) AS records_with_package,
        COUNT(DISTINCT student_id) AS distinct_students,
        ROUND(MIN(package_lpa), 2) AS min_package_lpa,
        ROUND(AVG(package_lpa), 2) AS avg_package_lpa,
        ROUND(MEDIAN(package_lpa), 2) AS median_package_lpa,
        ROUND(MAX(package_lpa), 2) AS max_package_lpa
    FROM placements
    GROUP BY placement_status
    ORDER BY total_records DESC;
    """

    print(
        connection.execute(package_query)
        .fetchdf()
        .to_string(index=False)
    )

finally:
    connection.close()



