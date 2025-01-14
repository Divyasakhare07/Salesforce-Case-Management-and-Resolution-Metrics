{{ config(
    materialized='view',
    schema='public',
    alias='transformed_case'
) }}

SELECT
    id,
    case_type,
    priority,
    status,
    created_date,
    closed_date,
    is_escalated,
    customer_region,
    customer_satisfaction_score,
    first_contact_resolution,
    resolution_time
FROM {{ ref('staging_case') }}
WHERE priority != 'Unknown'
