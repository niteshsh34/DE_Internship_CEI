 
-- Query 9 : LAG and LEAD Analysis
 
WITH
    monthly_revenue AS (
        SELECT
            strftime ('%Y-%m', o.order_date) AS month,
            ROUND(
                SUM(
                    oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)
                ),
                2
            ) AS revenue
        FROM
            orders o
            JOIN order_items oi ON o.order_id = oi.order_id
        WHERE
            oi.quantity > 0
        GROUP BY
            month
    )
SELECT
    month,
    revenue,
    LAG (revenue) OVER (
        ORDER BY
            month
    ) AS previous_month,
    LEAD (revenue) OVER (
        ORDER BY
            month
    ) AS next_month
FROM
    monthly_revenue;

 
-- Query 10 : Multiple Level CTE
 
WITH
    monthly_revenue AS (
        SELECT
            strftime ('%Y-%m', o.order_date) AS month,
            ROUND(
                SUM(
                    oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)
                ),
                2
            ) AS revenue
        FROM
            orders o
            JOIN order_items oi ON o.order_id = oi.order_id
        WHERE
            oi.quantity > 0
        GROUP BY
            month
    ),
    ranked_months AS (
        SELECT
            month,
            revenue,
            DENSE_RANK() OVER (
                ORDER BY
                    revenue DESC
            ) AS revenue_rank
        FROM
            monthly_revenue
    )
SELECT
    *
FROM
    ranked_months
WHERE
    revenue_rank <= 5
ORDER BY
    revenue_rank;

 
-- Query 11 : Customer Segmentation using NTILE
 
WITH
    customer_spending AS (
        SELECT
            c.customer_id,
            c.name,
            ROUND(
                SUM(
                    oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)
                ),
                2
            ) AS total_spent
        FROM
            customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
        WHERE
            oi.quantity > 0
        GROUP BY
            c.customer_id,
            c.name
    )
SELECT
    customer_id,
    name,
    total_spent,
    NTILE (4) OVER (
        ORDER BY
            total_spent DESC
    ) AS customer_segment
FROM
    customer_spending;

 
-- Query 12 : Year-over-Year Comparison
 
WITH
    yearly_revenue AS (
        SELECT
            strftime ('%Y', o.order_date) AS year,
            ROUND(
                SUM(
                    oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)
                ),
                2
            ) AS revenue
        FROM
            orders o
            JOIN order_items oi ON o.order_id = oi.order_id
        WHERE
            oi.quantity > 0
        GROUP BY
            year
    )
SELECT
    year,
    revenue,
    LAG (revenue) OVER (
        ORDER BY
            year
    ) AS previous_year_revenue,
    ROUND(
        (
            revenue - LAG (revenue) OVER (
                ORDER BY
                    year
            )
        ) * 100.0 / LAG (revenue) OVER (
            ORDER BY
                year
        ),
        2
    ) AS growth_percent
FROM
    yearly_revenue;

 
-- Query 13 : FIRST_VALUE and LAST_VALUE
 
SELECT DISTINCT
    customer_id,
    FIRST_VALUE (order_date) OVER (
        PARTITION BY
            customer_id
        ORDER BY
            order_date
    ) AS first_order,
    LAST_VALUE (order_date) OVER (
        PARTITION BY
            customer_id
        ORDER BY
            order_date ROWS BETWEEN UNBOUNDED PRECEDING
            AND UNBOUNDED FOLLOWING
    ) AS last_order
FROM
    orders
WHERE
    customer_id != -1
ORDER BY
    customer_id;

 
-- Query 14 : Cumulative Distribution
 
WITH
    customer_spending AS (
        SELECT
            c.customer_id,
            c.name,
            ROUND(
                SUM(
                    oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)
                ),
                2
            ) AS total_spent
        FROM
            customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
        WHERE
            oi.quantity > 0
        GROUP BY
            c.customer_id,
            c.name
    )
SELECT
    customer_id,
    name,
    total_spent,
    ROUND(
        CUME_DIST() OVER (
            ORDER BY
                total_spent DESC
        ),
        2
    ) AS cumulative_distribution
FROM
    customer_spending;

 
-- Query 15 : Cohort Analysis
 
WITH
    first_orders AS (
        SELECT
            customer_id,
            MIN(order_date) AS first_order_date
        FROM
            orders
        WHERE
            customer_id != -1
        GROUP BY
            customer_id
    )
SELECT
    strftime ('%Y-%m', first_order_date) AS cohort_month,
    COUNT(customer_id) AS total_customers
FROM
    first_orders
GROUP BY
    cohort_month
ORDER BY
    cohort_month;

 
-- Query 16 : Previous Order Analysis
 
SELECT
    customer_id,
    order_id,
    order_date,
    LAG (order_date) OVER (
        PARTITION BY
            customer_id
        ORDER BY
            order_date
    ) AS previous_order_date,
    ROUND(
        julianday (order_date) - julianday (
            LAG (order_date) OVER (
                PARTITION BY
                    customer_id
                ORDER BY
                    order_date
            )
        ),
        0
    ) AS days_between_orders
FROM
    orders
WHERE
    customer_id != -1
ORDER BY
    customer_id,
    order_date;