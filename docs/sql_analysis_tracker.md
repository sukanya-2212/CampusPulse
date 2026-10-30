
# CampusPulse — SQL Business Analysis Tracker

## Project Overview

Goal: Analyze college student data and generate business insights
using SQL and DuckDB.

## KPI Register

| KPI ID | Business Question | KPI / Metric | SQL File | Result File | Status |
|---|---|---|---|---|---|
| KPI-01 | How many students are in each department? | Student count by department | 01_student_count_by_department.sql | student_count_by_department.csv | Completed |
| KPI-02 | What is the attendance rate by department? | Attendance rate (%) | 02_attendance_rate_by_department.sql | attendance_rate_by_department.csv | Completed |
| KPI-03 | What is the average exam score by department? | Average exam score (%) | 03_average_exam_score_by_department.sql | average_exam_score_by_department.csv | Completed |
| KPI-04 | How are fee records distributed by type and payment status? | Fee record count and recorded amount by status | 04_fee_payment_analysis.sql | fee_payment_analysis.csv | Completed |

## Key Findings

### KPI-01: Student Count by Department
- Highest student count: Mechanical (217)
- Lowest student count: Electronics (167)
- Total valid student records: 998

### KPI-02: Attendance Rate by Department
- Highest rate: Electronics (76.51%)
- Lowest rate: Computer Science (75.66%)
- Difference: 0.85 percentage points

### KPI-03: Average Exam Score by Department
- Highest average score: Electronics (68.82%)
- Lowest average score: Mechanical (67.10%)
- Difference: 1.72 percentage points
- Metric: Average of individual exam-record percentages
### KPI-04: Fee Payment Analysis
- Total fee records analyzed: 2,993
- Payment statuses: Paid, Pending, Partially Paid
- Fee types: Exam, Hostel, Library, Tuition
- Highest Pending record count: Exam and Tuition (145 each)
- Lowest Pending record count: Library (118)
- Metric limitation: Recorded amounts are grouped by payment status. The dataset has not yet established whether `amount` represents the original fee, amount paid, or outstanding balance.


### KPI-05: Assignment Performance by Department

**Business question:** How do assignment submission patterns and average assignment scores differ across departments?

**SQL file:** `sql/05_assignment_performance_by_department.sql`

**Output file:** `data/reports/sql_results/assignment_performance_by_department.csv`

**Metrics calculated:**
- Total assignment records
- Submitted, late, and missing assignment counts
- Submission-status rate
- Average assignment score percentage

**Key findings:**
1. D02 has the highest submission-status rate at 79.80%, while D03 has the lowest at 76.89%.
2. D03 has the highest average assignment score at 74.66%, while D02 has the lowest at 74.04%.
3. D03 has the largest number of assignment records, with 2,164.
4. D04 has the highest number of late assignment records, with 330.

**Data-quality observation:** Assignment records marked `Missing` contain non-null scores. These records are excluded from the average assignment score calculation but retained in the source data. The underlying data-generation logic should be reviewed to establish whether this behavior is intentional.

**Limitations:** The submission-status rate measures the proportion of records marked `Submitted`; it should not be interpreted as an on-time submission rate unless the status definition supports that interpretation. Average assignment scores are calculated across eligible assignment records rather than equally weighting each student.

**Execution status:** SQL execution succeeded and the CSV report was generated. Final validation remains pending.

### KPI-06: Student Leave Analysis

**Business question:** How are student leave records distributed across departments, and how do leave approval outcomes and leave categories differ?

**SQL file:** `sql/06_student_leave_analysis.sql`

**Output file:** `data/reports/sql_results/student_leave_analysis.csv`

**Metrics calculated:**
- Total leave records by department
- Number of distinct students with leave records
- Approved, pending, and rejected leave counts
- Leave counts by category: Medical, Personal, Family, and Other
- Average duration of approved leave in days

**Key findings:**
1. D03 has the highest number of leave records, with 649.
2. D02 has the lowest number of leave records, with 492.
3. A total of 2,155 leave records were approved, 557 were pending, and 282 were rejected.
4. The overall leave approval rate is 71.98% (2,155 out of 2,994 records).
5. D01 has the highest number of pending leave records, with 118.
6. The dataset contains 2,994 validated leave records and 2,994 unique leave IDs.

**Data-quality observation:** Initial validation found no missing leave IDs, student IDs, or dates, and no invalid leave date ranges. However, the relationship between leave records and the `students` table has not yet been confirmed. Allowed leave-status and leave-category values also require validation.

**Limitations:** Leave-record counts do not represent unique students because a student may have multiple leave records. Department-level counts alone do not establish which department has the highest leave rate; department student populations must also be considered. The approval rate represents the proportion of all recorded leave requests marked Approved, not necessarily the approval rate among only finalized requests.

**Execution status:** SQL execution succeeded and the CSV report was generated. Final data-quality validation remains pending.


### KPI-07: Internship Analysis

**Business question:** How are student internship records distributed across departments, and what are the completion, ongoing, and withdrawal patterns?

**SQL file:** `sql/07_internship_analysis.sql`

**Output file:** `data/reports/sql_results/internship_analysis.csv`

**Metrics calculated:**
- Total internship records by department
- Number of distinct students with internships
- Number of distinct organizations represented in each department
- Completed, ongoing, and withdrawn internship counts
- Average internship duration in days for records with valid start and end dates

**Key findings:**
1. The dataset contains 499 validated internship records with 499 unique internship IDs.
2. D04 has the highest number of internship records, with 118.
3. D02 has the lowest number of internship records, with 84.
4. D05 has the highest number of completed internships, with 39.
5. D04 has the highest number of ongoing internships, with 41.
6. The overall internship-status distribution is 167 Completed, 166 Ongoing, and 166 Withdrawn.
7. Each department has four distinct organizations represented in the current dataset.

**Data-quality observation:** Initial validation found no missing student IDs or dates, no invalid date ranges, and no unexpected internship-status values. All 499 internship IDs are unique, and the student-reference check found zero internship records linked to nonexistent students.

**Limitations:** Internship counts represent records, not necessarily unique students, because a student may have multiple internships. The presence of four distinct organizations in each department does not establish that the same organizations appear in every department. Internship counts alone do not establish internship participation rates; department-level student populations should also be considered. Average duration should be interpreted carefully for ongoing internships because their end dates may be unavailable.

**Execution status:** SQL execution succeeded and the CSV report was generated. The initial record-integrity, date-quality, status-value, and student-reference checks passed. Further checks, including organization-name completeness, remain possible.


## KPI-08: Placement Analysis

**Business question:** How do placement outcomes and recorded package values vary across departments?

**SQL file:** `sql/08_placement_analysis.sql`

**Output file:** `data/reports/sql_results/placement_analysis.csv`

**Metrics calculated:**
- Total placement records by department
- Distinct students with placement records
- Distinct companies represented
- Counts of `Placed`, `In Progress`, `Offer Declined`, and `Not Placed` records
- Distinct students with at least one `Placed` record
- Average, median, and highest package among records marked `Placed`

### Key findings

1. The dataset contains 993 placement records associated with 650 distinct students.
2. Of the 993 records, 254 are marked `Placed`, 260 `In Progress`, 243 `Offer Declined`, and 236 `Not Placed`.
3. Across all departments, 224 distinct students have at least one record marked `Placed`.
4. D05 has the highest number of students with at least one `Placed` record (56), while D02 has the lowest (26).
5. D04 has the highest average package among `Placed` records at ₹13.79 LPA.
6. D03 has the lowest average package among `Placed` records at ₹12.91 LPA.
7. The highest recorded package among `Placed` records is ₹23.99 LPA in D04.
8. Department-level totals reconcile with the overall record counts and distinct-student counts.

### Data-quality observations

- All 993 placement records have unique placement IDs.
- No missing placement IDs, student IDs, company names, packages, or placement dates were found in the initial validation.
- No negative package values or unexpected placement statuses were found.
- No unmatched student references were found.
- 58 placement records have dates later than October 30, 2026. These require review to determine whether future dates are valid scheduled events or data-quality issues.
- Package values exist for all four placement statuses, including `Not Placed` and `Offer Declined`. Their business meaning must be confirmed before interpreting them as actual salaries.

### Limitations

- Multiple placement records exist for individual students, and some students have records across multiple statuses. The final outcome for each student cannot be determined from the current status combinations alone.
- The 224 students with at least one `Placed` record do not establish a final placement count or placement rate.
- The number of students eligible for placement has not yet been established. Therefore, a defensible student placement rate cannot currently be calculated.
- Package statistics are calculated at the placement-record level, not the unique-student level.
- Department comparisons describe recorded placement activity and packages; they do not establish which department has the best placement rate.

**Execution status:** SQL executed, output generated, and aggregate totals reconciled. Business interpretation and eligibility-based placement-rate analysis remain subject to the limitations above.