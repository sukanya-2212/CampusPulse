WITH internship_details AS (
    SELECT
        s.department_id,
        i.internship_id,
        i.student_id,
        i.organization,
        i.internship_status,
        i.start_date,
        i.end_date,
        CASE
            WHEN i.start_date IS NOT NULL
             AND i.end_date IS NOT NULL
             AND i.end_date >= i.start_date
            THEN DATE_DIFF(
                'day',
                i.start_date,
                i.end_date
            ) + 1
            ELSE NULL
        END AS internship_duration_days
    FROM internships AS i
    LEFT JOIN students AS s
        ON i.student_id = s.student_id
)
SELECT
    department_id,
    COUNT(*) AS total_internship_records,
    COUNT(DISTINCT student_id) AS students_with_internships,
    COUNT(DISTINCT organization) AS distinct_organizations,

    SUM(
        CASE WHEN internship_status = 'Completed'
        THEN 1 ELSE 0 END
    ) AS completed_internships,

    SUM(
        CASE WHEN internship_status = 'Ongoing'
        THEN 1 ELSE 0 END
    ) AS ongoing_internships,

    SUM(
        CASE WHEN internship_status = 'Withdrawn'
        THEN 1 ELSE 0 END
    ) AS withdrawn_internships,

    ROUND(
        AVG(internship_duration_days),
        2
    ) AS avg_internship_duration_days

FROM internship_details
GROUP BY department_id
ORDER BY total_internship_records DESC;