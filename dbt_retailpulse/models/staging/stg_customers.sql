with source as (
  select * from {{ source('retailpulse_silver', 'customers') }}
)
 
select
  customer_id,
  name,
  city,
  country,
  signup_date
from source
