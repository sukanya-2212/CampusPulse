# CampusPulse — Campus Data Analytics

An end-to-end data analytics portfolio project that explores synthetic university data using Python, Pandas, DuckDB, and SQL.

## Overview

CampusPulse is designed to demonstrate how raw institutional data can be transformed into validated datasets, stored in an analytical database, and used to answer business questions about campus operations.

The project currently includes synthetic data generation, data-quality validation, DuckDB warehouse loading, relationship checks, and SQL-based KPI analysis.

**Data notice:** All datasets are synthetic and intended for demonstration and learning. They do not represent actual students or a real educational institution.

## Business Questions

CampusPulse explores questions such as:

- How many students are represented in each department?
- How does attendance vary by department?
- How do average examination scores compare across departments?
- What do fee-payment records show by fee type and payment status?
- How do assignment submission statuses and scores vary by department?
- What patterns appear in student leave requests?
- How are internships distributed by department and status?
- What do placement records show about outcomes and recorded salary packages?

## Technology Stack

- **Python** — data generation, validation, and workflow automation
- **Pandas** — tabular data processing
- **DuckDB** — analytical database
- **SQL** — KPI queries and aggregations
- **CSV** — input datasets and exported analysis results
- **Git and GitHub** — version control and project hosting

## Project Workflow

1. Generate synthetic institutional datasets.
2. Validate records and identify data-quality issues.
3. Preserve rejected records in quarantine files with validation reasons.
4. Load validated datasets into DuckDB.
5. Check relationships between dependent tables.
6. Execute SQL queries for business analysis.
7. Export query results as CSV reports.

Raw input files are preserved separately from validated data. Generated validation outputs and the local DuckDB database are excluded from version control because they can be recreated.

## Current Analyses

| Analysis | Business focus |
|---|---|
| Student count by department | Department-level student distribution |
| Attendance rate by department | Comparison of attendance |
| Average exam score by department | Academic performance |
| Fee payment analysis | Fee type and payment status |
| Assignment performance by department | Submission statuses and scores |
| Student leave analysis | Leave status, type, and duration |
| Internship analysis | Internship status and duration |
| Placement analysis | Recorded placement outcomes and package statistics |

Results are available in `data/reports/sql_results/`.

## Initial Findings

The current synthetic dataset contains approximately:

- **998** valid student records
- **29,934** valid attendance records
- **4,998** valid examination records
- **9,983** valid assignment records
- **2,993** valid fee records
- **2,994** valid leave records
- **499** valid internship records
- **993** placement records

These figures describe the current generated dataset and may change when the data-generation or validation workflow is rerun.

### Interpretation Caveats

- The dataset is synthetic; findings are not evidence about a real institution.
- Fee amounts should not be interpreted as outstanding balances until their precise meaning is confirmed.
- Assignment submission statuses and scores require careful interpretation, particularly for records marked Missing.
- Students may have multiple placement records, so placement-record counts are not equivalent to unique students placed.
- Placement records with future dates require interpretation based on the intended data model.
- Department-level comparisons should account for differences in group sizes and relevant denominators.

## Repository Structure

```text
CampusPulse/
├── data/
│   ├── raw/
│   └── reports/
│       └── sql_results/
├── docs/
│   └── sql_analysis_tracker.md
├── phase_1/
│   └── task_1_data_ingestion_validation/
│       └── validate_data.py
├── scripts/
│   ├── generate_synthetic_data.py
│   ├── load_to_duckdb.py
│   ├── run_analysis.py
│   ├── explore_database.py
│   ├── check_relationships.py
│   ├── investigate_unmatched_students.py
│   └── verify_database.py
├── sql/
│   ├── 01_student_count_by_department.sql
│   ├── 02_attendance_rate_by_department.sql
│   ├── 03_average_exam_score_by_department.sql
│   ├── 04_fee_payment_analysis.sql
│   ├── 05_assignment_performance_by_department.sql
│   ├── 06_student_leave_analysis.sql
│   ├── 07_internship_analysis.sql
│   └── 08_placement_analysis.sql
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

### Prerequisites

- Python installed on your computer
- Git
- PowerShell on Windows, or an equivalent terminal

### 1. Clone the repository

```bash
git clone https://github.com/sukanya-2212/CampusPulse.git
cd CampusPulse
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the analysis

The repository contains saved SQL queries and a Python runner that executes them and exports results.

```powershell
python .\scripts\run_analysis.py
```

The analysis runner expects the DuckDB database to exist and contain the required tables. If you are setting up from scratch, first generate the data, validate it, and load it into DuckDB using the project's scripts.

Run scripts from the repository root. Refer to each script and its configuration for the exact execution order and required inputs.

## Data and Reproducibility

- Raw CSV files are stored in `data/raw/`.
- Analysis outputs are stored in `data/reports/`.
- Validated and quarantined datasets are generated by the validation workflow and are excluded from Git.
- The local DuckDB database is excluded from Git and must be rebuilt locally.
- All analysis results depend on the current synthetic dataset and query definitions.

## Roadmap

- [x] Synthetic dataset generation
- [x] Data-quality validation and quarantine
- [x] DuckDB loading
- [x] Relationship checks
- [x] Eight SQL-based analyses
- [ ] Document and test a complete clean-install workflow
- [ ] Build an interactive Streamlit dashboard
- [ ] Add advanced student-risk analysis with appropriate validation
- [ ] Improve automated data-quality reporting
- [ ] Produce a final project report

## Author

**Sukanya**

GitHub: [@sukanya-2212](https://github.com/sukanya-2212)

---

*CampusPulse is an educational analytics project built with synthetic data.*