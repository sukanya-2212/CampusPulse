
-- KPI-02: Attendance Rate by Department
-- Business question: What percentage of attendance records
-- are marked Present in each department?

SELECT
    d.department_name,
    COUNT(*) AS total_attendance_records,
    SUM(
        CASE
            WHEN LOWER(a.status) = 'present' THEN 1
            ELSE 0
        END
    ) AS present_records,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN LOWER(a.status) = 'present' THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS attendance_rate_pct
FROM attendance AS a
JOIN students AS s
    ON a.student_id = s.student_id
JOIN departments AS d
    ON s.department_id = d.department_id
GROUP BY
    d.department_id,
    d.department_name
ORDER BY attendance_rate_pct DESC;
