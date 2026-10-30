
-- KPI-03: Average Exam Score by Department
-- Business question: What is the average exam score percentage
-- for each department?

SELECT
    d.department_name,
    COUNT(*) AS total_exam_records,
    ROUND(
        AVG(
            100.0 * e.marks_obtained / NULLIF(e.max_marks, 0)
        ),
        2
    ) AS avg_exam_score_pct
FROM exam_results AS e
JOIN students AS s
    ON e.student_id = s.student_id
JOIN departments AS d
    ON s.department_id = d.department_id
GROUP BY
    d.department_id,
    d.department_name
ORDER BY avg_exam_score_pct DESC;
