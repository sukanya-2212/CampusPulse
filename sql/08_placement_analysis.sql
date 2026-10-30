WITH placement_details AS (
    SELECT
        p.placement_id,
        p.student_id,
        s.department_id,
        p.company_name,
        p.placement_status,
        p.package_lpa,
        p.placement_date
    FROM placements AS p
    LEFT JOIN students AS s
        ON p.student_id = s.student_id
)

SELECT
    department_id,

    COUNT(*) AS total_placement_records,

    COUNT(DISTINCT student_id)
        AS students_with_placement_records,

    COUNT(DISTINCT company_name)
        AS distinct_companies,

    SUM(
        CASE
            WHEN placement_status = 'Placed'
            THEN 1 ELSE 0
        END
    ) AS placed_records,

    COUNT(
        DISTINCT CASE
            WHEN placement_status = 'Placed'
            THEN student_id
        END
    ) AS students_with_placed_records,

    SUM(
        CASE
            WHEN placement_status = 'In Progress'
            THEN 1 ELSE 0
        END
    ) AS in_progress_records,

    SUM(
        CASE
            WHEN placement_status = 'Offer Declined'
            THEN 1 ELSE 0
        END
    ) AS offer_declined_records,

    SUM(
        CASE
            WHEN placement_status = 'Not Placed'
            THEN 1 ELSE 0
        END
    ) AS not_placed_records,

    ROUND(
        AVG(
            CASE
                WHEN placement_status = 'Placed'
                THEN package_lpa
            END
        ),
        2
    ) AS avg_placed_package_lpa,

    ROUND(
        MEDIAN(
            CASE
                WHEN placement_status = 'Placed'
                THEN package_lpa
            END
        ),
        2
    ) AS median_placed_package_lpa,

    ROUND(
        MAX(
            CASE
                WHEN placement_status = 'Placed'
                THEN package_lpa
            END
        ),
        2
    ) AS highest_placed_package_lpa

FROM placement_details

GROUP BY department_id

ORDER BY students_with_placed_records DESC;