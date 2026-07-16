
 
-- Query 5 : Products with More Returns than Purchases
 
SELECT
    p.product_id,
    p.product_name,
    SUM(
        CASE
            WHEN oi.quantity > 0 THEN oi.quantity
            ELSE 0
        END
    ) AS purchased_quantity,
    ABS(
        SUM(
            CASE
                WHEN oi.quantity < 0 THEN oi.quantity
                ELSE 0
            END
        )
    ) AS returned_quantity
FROM
    products p
    JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY
    p.product_id,
    p.product_name
HAVING
    returned_quantity > purchased_quantity;

 
-- Query 6 : Return Rate per Category
 
SELECT
    p.category,
    SUM(
        CASE
            WHEN oi.quantity > 0 THEN oi.quantity
            ELSE 0
        END
    ) AS purchased_items,
    ABS(
        SUM(
            CASE
                WHEN oi.quantity < 0 THEN oi.quantity
                ELSE 0
            END
        )
    ) AS returned_items,
    ROUND(
        ABS(
            SUM(
                CASE
                    WHEN oi.quantity < 0 THEN oi.quantity
                    ELSE 0
                END
            )
        ) * 100.0 / SUM(
            CASE
                WHEN oi.quantity > 0 THEN oi.quantity
                ELSE 0
            END
        ),
        2
    ) AS return_rate
FROM
    products p
    JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY
    p.category;

 
-- Query 7 : Running Total Revenue by Month
 
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
    SUM(revenue) OVER (
        ORDER BY
            month
    ) AS running_total
FROM
    monthly_revenue;

 
-- Query 8 : Customer Ranking
 
SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)
        ),
        2
    ) AS total_spent,
    DENSE_RANK() OVER (
        ORDER BY
            SUM(
                oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)
            ) DESC
    ) AS customer_rank
FROM
    customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
WHERE
    oi.quantity > 0
GROUP BY
    c.customer_id,
    c.name;
