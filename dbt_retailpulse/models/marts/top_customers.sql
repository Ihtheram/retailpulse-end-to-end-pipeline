with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
)

select
    o.customer_id,
    count(o.order_id)       as total_orders,
    round(sum(o.amount), 2) as lifetime_value,
    c.name,
    c.city,
    c.country
from orders o
join customers c on o.customer_id = c.customer_id
group by o.customer_id, c.name, c.city, c.country
order by lifetime_value desc
