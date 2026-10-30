WITH leave_details AS (
    SELECT
        s.department_id,
        l.leave_id,
        l.student_id,
        l.leave_type,
        l.leave_status,
        l.leave_start_date,
        l.leave_end_date,
        DATE_DIFF(
            'day',
            l.leave_start_date,
            l.leave_end_date
        ) + 1 AS leave_duration_days
    FROM student_leave AS l
    JOIN students AS s
        ON l.student_id = s.student_id
)
SELECT
    department_id,

    COUNT(*) AS total_leave_records,

    COUNT(DISTINCT student_id) AS students_with_leave,

    SUM(
        CASE WHEN leave_status = 'Approved'
             THEN 1 ELSE 0 END
    ) AS approved_leave_count,

    SUM(
        CASE WHEN leave_status = 'Pending'
             THEN 1 ELSE 0 END
    ) AS pending_leave_count,

    SUM(
        CASE WHEN leave_status = 'Rejected'
             THEN 1 ELSE 0 END
    ) AS rejected_leave_count,

    SUM(
        CASE WHEN leave_type = 'Medical'
             THEN 1 ELSE 0 END
    ) AS medical_leave_count,

    SUM(
        CASE WHEN leave_type = 'Personal'
             THEN 1 ELSE 0 END
    ) AS personal_leave_count,

    SUM(
        CASE WHEN leave_type = 'Family'
             THEN 1 ELSE 0 END
    ) AS family_leave_count,

    SUM(
        CASE WHEN leave_type = 'Other'
             THEN 1 ELSE 0 END
    ) AS other_leave_count,

    ROUND(
        AVG(
            CASE
                WHEN leave_status = 'Approved'
                THEN leave_duration_days
            END
        ),
        2
    ) AS avg_approved_leave_days

FROM leave_details
GROUP BY department_id
ORDER BY total_leave_records DESC;