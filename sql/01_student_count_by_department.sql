
-- KPI-01: Student Count by Department
-- Business question: How many students are in each department?

SELECT
    d.department_id,
    d.department_name,
    COUNT(s.student_id) AS total_students
FROM departments AS d
LEFT JOIN students AS s
    ON d.department_id = s.department_id
GROUP BY
    d.department_id,
    d.department_name
ORDER BY total_students DESC;
