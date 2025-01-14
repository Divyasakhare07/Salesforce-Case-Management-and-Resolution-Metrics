{{ config(
    materialized='view',
    schema='public',
    alias='transformed_case'
) }}

SELECT
    id,
    CASE WHEN case_type IS NULL THEN 'Unknown' ELSE case_type END AS case_type,
    priority,
    status,
    opened_date,  -- Make sure this is being correctly sourced from 'staging_case'
    closed_date,
    FALSE AS is_escalated,  -- Assuming a default value of FALSE
    customer_region,
    customer_satisfaction_score,
    FALSE AS first_contact_resolution,  -- Assuming a default value of FALSE
    EXTRACT(EPOCH FROM (closed_date - opened_date)) / 3600 AS resolution_time  -- Calculate resolution time in hours
FROM {{ ref('staging_case') }}
WHERE priority != 'Unknown'
