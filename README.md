# SLA & Velocity Analysis
End-to-end ELT data pipeline analyzing engineering velocity, SLA breaches, and workflow bottlenecks using Python, BigQuery, and Power BI.

## Project Overview
This project is an end-to-end **ELT (Extract, Load, Transform)** pipeline designed to analyze engineering velocity and bottleneck metrics for a major open-source repository. Transitioning beyond basic volume metrics, this project focuses on process efficiency, Service Level Agreement (SLA) breaches, and identifying Key Person Dependencies in the pull request review cycle.

## Architecture & Tech Stack
This project mimics a modern modern data stack workflow:
1. **Extract (Python):** Utilized the `requests` and `pandas` libraries to ping the GitHub REST API. Handled API pagination to extract thousands of nested JSON records representing closed issues and pull requests, flattening them into a raw tabular format.
2. **Load (Google BigQuery):** Loaded the raw data into a cloud data warehouse (BigQuery Sandbox) to act as the single source of truth.
3. **Transform (SQL):** Engineered business logic entirely within the data warehouse. Wrote SQL views to cast text to timestamps, calculate precise `resolution_days`, generate `cohort_month` tags for trend analysis, and flag `sla_status` based on a target 14-day resolution window.
4. **Visualize (Power BI):** Connected directly to the cleaned SQL view via Import mode. Utilized DAX to calculate dynamic P90 resolution times and built an interactive dashboard tailored for an Engineering Manager.

## Key Business Metrics Engineered
* **P90 Resolution Time:** Calculated the 90th percentile (26.9 days) to identify the true upper limit of bug-fix SLAs, exposing a massive operational bottleneck that the Average Resolution Time (9.6 days) completely hid.
* **Workload Split:** Segmented the resolution pipeline between standard bugs and code reviews (Pull Requests) to monitor resource allocation.
* **Key Person Dependency:** Grouped resolution metrics by Assignee/Author to flag specific bottlenecks in the queue, allowing management to reallocate senior developer resources efficiently.

## Key Insights Discovered
* **The "Average" Illusion:** While the average resolution time looks healthy at under 10 days, the P90 metric proves that the slowest 10% of tickets are taking nearly a month to resolve, indicating severe blockers on complex issues.
* **Improving Velocity:** The SLA Breach trend line shows a massive operational improvement from November to February, dropping from a 60% breach rate down to nearly 0%. 

## Repository Contents
* `extract_github_data.py`: The Python script used to interact with the GitHub API.
* `transform_metrics.sql`: The BigQuery SQL script used to clean timestamps and engineer SLA logic.
* `Engineering_Ops_Dashboard.pbix`: The final Power BI dashboard file.
* `dashboard`: Contains screenshots of the final dashboard for quick viewing.
