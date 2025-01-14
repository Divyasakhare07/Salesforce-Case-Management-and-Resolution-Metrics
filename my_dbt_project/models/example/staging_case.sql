WITH cleaned_data AS (
    SELECT
        id,
        CASE WHEN case_type IS NULL THEN 'Unknown' ELSE case_type END AS case_type,
        priority,
        status,
        opened_date,  -- Use 'opened_date' directly
        closed_date,
        FALSE AS is_escalated,  -- Assuming a default value of FALSE
        customer_region,
        customer_satisfaction_score,
        FALSE AS first_contact_resolution,  -- Assuming a default value of FALSE
        -- Calculate resolution time in hours
        EXTRACT(EPOCH FROM (closed_date - opened_date)) / 3600 AS resolution_time
    FROM {{ source('my_source', 'case_raw') }}  -- Use 'my_source' here
)
SELECT * FROM cleaned_data
