WITH assignment_metrics AS (
    SELECT
        s.department_id,
        a.assignment_id,
        a.submission_status,
        CASE
            WHEN a.submission_status IN ('Submitted', 'Late')
             AND a.score IS NOT NULL
             AND a.max_score > 0
             AND a.score >= 0
             AND a.score <= a.max_score
            THEN 100.0 * a.score / a.max_score
            ELSE NULL
        END AS score_pct
    FROM assignments AS a
    JOIN students AS s
        ON a.student_id = s.student_id
)
SELECT
    department_id,
    COUNT(*) AS total_assignments,
    SUM(
        CASE WHEN submission_status = 'Submitted'
             THEN 1 ELSE 0 END
    ) AS submitted_count,
    SUM(
        CASE WHEN submission_status = 'Late'
             THEN 1 ELSE 0 END
    ) AS late_count,
    SUM(
        CASE WHEN submission_status = 'Missing'
             THEN 1 ELSE 0 END
    ) AS missing_count,
    ROUND(
        100.0 * SUM(
            CASE WHEN submission_status = 'Submitted'
                 THEN 1 ELSE 0 END
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS submission_status_rate_pct,
    ROUND(AVG(score_pct), 2) AS avg_assignment_score_pct
FROM assignment_metrics
GROUP BY department_id
ORDER BY avg_assignment_score_pct DESC;