WITH cleaned_data AS (
    SELECT
        id,
        CASE WHEN case_type IS NULL THEN 'Unknown' ELSE case_type END AS case_type,
        priority,
        status,
        created_date,
        closed_date,
        is_escalated,
        customer_region,
        customer_satisfaction_score,
        first_contact_resolution,
        -- Calculate resolution time in hours
        EXTRACT(EPOCH FROM (closed_date - created_date)) / 3600 AS resolution_time
    FROM {{ source('my_source', 'case_raw') }}  -- Use 'my_source' here
)
SELECT * FROM cleaned_data
