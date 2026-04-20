SELECT
  Issue_Number,
  Title,
  State,
  Author,
  Is_Pull_Request,
  
  -- 1. Convert text strings to official Timestamps
  CAST(Created_At AS TIMESTAMP) AS created_timestamp,
  CAST(Closed_At AS TIMESTAMP) AS closed_timestamp,

  -- 2. Create a Cohort Month for trend analysis
  DATE_TRUNC(CAST(Created_At AS DATE), MONTH) AS cohort_month,

  -- 3. Calculate Resolution Time in decimal days (e.g., 3.5 days)
  -- Using HOURS/24 is more accurate than DAY for P90 calculations
  TIMESTAMP_DIFF(CAST(Closed_At AS TIMESTAMP), CAST(Created_At AS TIMESTAMP), HOUR) / 24.0 AS resolution_days,

  -- 4. Tag the SLAs (Assuming a 14-day SLA target)
  CASE 
    WHEN CAST(Closed_At AS TIMESTAMP) IS NULL THEN 'Still Open'
    WHEN TIMESTAMP_DIFF(CAST(Closed_At AS TIMESTAMP), CAST(Created_At AS TIMESTAMP), HOUR) / 24.0 <= 14.0 THEN 'Met SLA'
    ELSE 'Breached SLA' 
  END AS sla_status

FROM
  `full-stack-analytics-01.github_fullstack.github_pm_raw_data`
WHERE 
  -- Filter out junk records if any API pulls failed
  Created_At IS NOT NULL