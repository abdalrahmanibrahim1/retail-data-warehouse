from src.load import get_connection


def get_total_revenue_and_profit():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT SUM(revenue), SUM(profit)
        FROM fact_sales
    """
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

def get_total_revenue_by_product_category():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT p.category, SUM(f.revenue)
        FROM fact_sales f
        JOIN dim_product p
        ON f.product_key = p.product_key
        GROUP BY p.category
        ORDER BY SUM(f.revenue) DESC
    """
    )
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_top_5_products_by_revenue():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT
            p.product_name,
            p.category,
            SUM(f.revenue) AS total_revenue,
            SUM(f.profit) AS total_profit,
            COUNT(f.sale_key) AS number_of_sales,
            SUM(f.revenue) / COUNT(f.sale_key) AS average_revenue_per_sale,
            (SUM(f.profit) / NULLIF(SUM(f.revenue), 0)) * 100 AS profit_margin_percentage
        FROM fact_sales f
        JOIN dim_product p
        ON f.product_key = p.product_key
        GROUP BY p.product_key, p.product_name, p.category
        ORDER BY total_revenue DESC
        LIMIT 5;
    """
    )
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_sales_by_store_city():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT s.store_city, SUM(f.revenue) AS total_revenue, SUM(f.profit) AS total_profit, COUNT(f.sale_key) AS number_of_sales
        FROM fact_sales f
        JOIN dim_store s
        ON f.store_key = s.store_key
        GROUP BY s.store_city
        ORDER BY total_revenue DESC
    """
    )
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
    
def get_revenue_by_customer_segment():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT
            c.customer_segment,
            SUM(f.revenue) AS total_revenue,
            SUM(f.profit) AS total_profit,
            COUNT(f.sale_key) AS number_of_sales,
            SUM(f.revenue) / COUNT(f.sale_key) AS average_revenue_per_sale,
            (SUM(f.profit) / NULLIF(SUM(f.revenue), 0)) * 100 AS profit_margin_percentage
        FROM fact_sales f
        JOIN dim_customer c
        ON f.customer_key = c.customer_key
        GROUP BY c.customer_segment
        ORDER BY total_revenue DESC;
    """
    )
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_monthly_revenue_trend():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT
            d.year,
            d.month,
            SUM(f.revenue) AS total_revenue,
            SUM(f.profit) AS total_profit,
            COUNT(f.sale_key) AS number_of_sales,
            SUM(f.revenue) / COUNT(f.sale_key) AS average_revenue_per_sale,
            (SUM(f.profit) / NULLIF(SUM(f.revenue), 0)) * 100 AS profit_margin_percentage
        FROM fact_sales f
        JOIN dim_date d
        ON f.date_key = d.date_key
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month;
    """
    )
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_category_city_segment_performance():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT
            s.store_city,
            c.customer_segment,
            p.category,
            SUM(f.revenue) AS total_revenue,
            SUM(f.profit) AS total_profit,
            COUNT(f.sale_key) AS number_of_sales,
            SUM(f.revenue) / COUNT(f.sale_key) AS average_revenue_per_sale,
            (SUM(f.profit) / NULLIF(SUM(f.revenue), 0)) * 100 AS profit_margin_percentage
        FROM fact_sales f
        JOIN dim_store s 
            ON f.store_key = s.store_key
        JOIN dim_customer c
            ON f.customer_key = c.customer_key
        JOIN dim_product p
            ON f.product_key = p.product_key
        GROUP BY s.store_city, c.customer_segment, p.category
        ORDER BY total_revenue DESC, total_profit DESC;
    """
    )
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_category_profit_margin_ranking():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT 
            p.category,
            SUM(f.revenue) AS total_revenue,
            SUM(f.profit) AS total_profit,
            COUNT(f.sale_key) AS number_of_sales,
            SUM(f.revenue) / COUNT(f.sale_key) AS average_revenue_per_sale,
            (SUM(f.profit) / NULLIF(SUM(f.revenue), 0)) * 100 AS profit_margin_percentage
        FROM fact_sales f
        JOIN dim_product p
        ON f.product_key = p.product_key
        GROUP BY p.category
        ORDER BY profit_margin_percentage DESC
    """
    )
    
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_customer_segment_average_sale_ranking():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT 
            c.customer_segment,
            SUM(f.revenue) AS total_revenue,
            SUM(f.profit) AS total_profit,
            COUNT(f.sale_key) AS number_of_sales,
            SUM(f.revenue) / COUNT(f.sale_key) AS average_revenue_per_sale,
            (SUM(f.profit) / NULLIF(SUM(f.revenue), 0)) * 100 AS profit_margin_percentage
        FROM fact_sales f
        JOIN dim_customer c
        ON f.customer_key = c.customer_key
        GROUP BY c.customer_segment
        ORDER BY average_revenue_per_sale DESC 
    """
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_monthly_revenue_growth():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    WITH monthly_revenue AS(
        SELECT 
            d.year,
            d.month,
            SUM(f.revenue) AS total_revenue
        FROM fact_sales f
        JOIN dim_date d
        ON f.date_key = d.date_key
        GROUP BY d.year, d.month
    ),
    monthly_with_previous AS(
        SELECT
            year,
            month,
            total_revenue,
            LAG(total_revenue) OVER (ORDER BY year, month) AS previous_month_revenue
        FROM monthly_revenue
    )
    SELECT
        year,
        month,
        total_revenue,
        previous_month_revenue,
        total_revenue - previous_month_revenue AS growth_amount,
        (total_revenue - previous_month_revenue) / NULLIF(previous_month_revenue, 0) * 100 AS growth_percentage
    FROM monthly_with_previous
    ORDER BY year, month;
    """
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
def get_monthly_category_revenue_trend():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT 
            d.year,
            d.month,
            p.category,
            SUM(f.revenue) AS total_revenue,
            SUM(f.profit) AS total_profit,
            COUNT(f.sale_key) AS number_of_sales,
            SUM(f.revenue) / COUNT(f.sale_key) AS average_revenue_per_sale,
            (SUM(f.profit) / NULLIF(SUM(f.revenue),0)) * 100 AS profit_margin_percentage
        FROM fact_sales f
        JOIN dim_product p
            ON f.product_key = p.product_key
        JOIN dim_date d
            ON f.date_key = d.date_key
        GROUP BY p.category, d.year, d.month
        ORDER BY d.year, d.month, p.category
    """
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result

def get_monthly_category_revenue_growth(category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    WITH monthly_category_revenue AS
    (
        SELECT 
            d.year,
            d.month,
            p.category,
            SUM(f.revenue) AS total_revenue
        FROM fact_sales f
        JOIN dim_product p
            ON f.product_key = p.product_key
        JOIN dim_date d
            ON f.date_key = d.date_key
        WHERE p.category = %s
        GROUP BY p.category, d.year, d.month
    ),
    monthly_category_revenue_previous AS
    ( 
        SELECT 
            year,
            month,
            category,
            total_revenue,
            LAG(total_revenue) OVER (ORDER BY year, month) AS previous_month_revenue
        FROM monthly_category_revenue
    )
    SELECT
        year,
        month,
        category,
        total_revenue,
        previous_month_revenue,
        total_revenue - previous_month_revenue AS growth,
        ((total_revenue - previous_month_revenue) / NULLIF(previous_month_revenue, 0)) * 100 AS growth_percentage
    FROM monthly_category_revenue_previous
    ORDER BY year, month;
    """, 
    (category,)
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
if __name__ == "__main__":
    revenue, profit = get_total_revenue_and_profit()

    print("")
    print("Overall Warehouse Summary")
    print("-" * 40)
    print(f"Total revenue: {revenue:,.0f}")
    print(f"Total profit: {profit:,.0f}")

    print("")
    print("Revenue by Product Category")
    print(
        f"{'Category':<20} | "
        f"{'Revenue':>15}"
    )
    print("-" * 40)

    for row in get_total_revenue_by_product_category():
        category, revenue = row
        print(f"{category:<20} | {revenue:>15,.0f}")

    print("")
    print("Top 5 Products by Revenue")
    print(
        f"{'Product':<25} | "
        f"{'Category':<15} | "
        f"{'Revenue':>15} | "
        f"{'Profit':>15} | "
        f"{'Sales':>8} | "
        f"{'Avg/Sale':>15} | "
        f"{'Margin %':>10}"
    )
    print("-" * 120)

    for row in get_top_5_products_by_revenue():
        product, category, revenue, profit, num_of_sales, avg_revenue_per_sale, profit_margin = row

        print(
            f"{product:<25} | "
            f"{category:<15} | "
            f"{revenue:>15,.0f} | "
            f"{profit:>15,.0f} | "
            f"{num_of_sales:>8} | "
            f"{avg_revenue_per_sale:>15,.0f} | "
            f"{profit_margin:>9.2f}%"
        )

    print("")
    print("Sales by Store City")
    print(
        f"{'Store City':<15} | "
        f"{'Revenue':>15} | "
        f"{'Profit':>15} | "
        f"{'Sales':>10}"
    )
    print("-" * 65)

    for row in get_sales_by_store_city():
        city, revenue, profit, num_of_sales = row

        print(
            f"{city:<15} | "
            f"{revenue:>15,.0f} | "
            f"{profit:>15,.0f} | "
            f"{num_of_sales:>10}"
        )

    print("")
    print("Revenue by Customer Segment")
    print(
        f"{'Customer Segment':<18} | "
        f"{'Revenue':>15} | "
        f"{'Profit':>15} | "
        f"{'Sales':>10} | "
        f"{'Avg/Sale':>15} | "
        f"{'Margin %':>10}"
    )
    print("-" * 105)

    for row in get_revenue_by_customer_segment():
        segment, revenue, profit, num_of_sales, avg_revenue_per_sale, profit_margin = row

        print(
            f"{segment:<18} | "
            f"{revenue:>15,.0f} | "
            f"{profit:>15,.0f} | "
            f"{num_of_sales:>10} | "
            f"{avg_revenue_per_sale:>15,.0f} | "
            f"{profit_margin:>9.2f}%"
        )

    print("")
    print("Monthly Revenue Trend")
    print(
        f"{'Year':<6} | "
        f"{'Month':<6} | "
        f"{'Revenue':>15} | "
        f"{'Profit':>15} | "
        f"{'Sales':>10} | "
        f"{'Avg/Sale':>15} | "
        f"{'Margin %':>10}"
    )
    print("-" * 105)

    for row in get_monthly_revenue_trend():
        year, month, revenue, profit, num_of_sales, avg_revenue_per_sale, profit_margin = row

        print(
            f"{year:<6} | "
            f"{month:<6} | "
            f"{revenue:>15,.0f} | "
            f"{profit:>15,.0f} | "
            f"{num_of_sales:>10} | "
            f"{avg_revenue_per_sale:>15,.0f} | "
            f"{profit_margin:>9.2f}%"
        )


    print("")
    print("Category Performance by City and Customer Segment")
    print(
        f"{'City':<15} | "
        f"{'Segment':<18} | "
        f"{'Category':<15} | "
        f"{'Revenue':>15} | "
        f"{'Profit':>15} | "
        f"{'Sales':>8} | "
        f"{'Avg/Sale':>15} | "
        f"{'Margin %':>10}"
    )
    print("-" * 130)

    for row in get_category_city_segment_performance():
        city, segment, category, revenue, profit, num_of_sales, avg_revenue_per_sale, profit_margin = row

        print(
            f"{city:<15} | "
            f"{segment:<18} | "
            f"{category:<15} | "
            f"{revenue:>15,.0f} | "
            f"{profit:>15,.0f} | "
            f"{num_of_sales:>8} | "
            f"{avg_revenue_per_sale:>15,.0f} | "
            f"{profit_margin:>9.2f}%"
        )

    print("")
    print("Category Profit Margin Ranking")
    print(
        f"{'Category':<20} | "
        f"{'Revenue':>15} | "
        f"{'Profit':>15} | "
        f"{'Sales':>8} | "
        f"{'Avg/Sale':>15} | "
        f"{'Margin %':>10}"
    )
    print("-" * 100)

    for row in get_category_profit_margin_ranking():
        category, revenue, profit, num_of_sales, avg_revenue_per_sale, profit_margin = row

        print(
            f"{category:<20} | "
            f"{revenue:>15,.0f} | "
            f"{profit:>15,.0f} | "
            f"{num_of_sales:>8} | "
            f"{avg_revenue_per_sale:>15,.0f} | "
            f"{profit_margin:>9.2f}%"
        )

    print("")
    print("Customer Segment Average Sale Ranking")
    print(
        f"{'Customer Segment':<18} | "
        f"{'Revenue':>15} | "
        f"{'Profit':>15} | "
        f"{'Sales':>8} | "
        f"{'Avg/Sale':>15} | "
        f"{'Margin %':>10}"
    )
    print("-" * 105)

    for row in get_customer_segment_average_sale_ranking():
        segment, revenue, profit, num_of_sales, avg_revenue_per_sale, profit_margin = row

        print(
            f"{segment:<18} | "
            f"{revenue:>15,.0f} | "
            f"{profit:>15,.0f} | "
            f"{num_of_sales:>8} | "
            f"{avg_revenue_per_sale:>15,.0f} | "
            f"{profit_margin:>9.2f}%"
        )

    print("")
    print("Monthly Revenue Growth")
    print(
        f"{'Year':<6} | "
        f"{'Month':<6} | "
        f"{'Revenue':>15} | "
        f"{'Prev Revenue':>15} | "
        f"{'Growth':>15} | "
        f"{'Growth %':>10}"
    )
    print("-" * 95)

    for row in get_monthly_revenue_growth():
        year, month, revenue, previous_revenue, growth_amount, growth_percentage = row

        previous_revenue_display = "N/A" if previous_revenue is None else f"{previous_revenue:,.0f}"
        growth_amount_display = "N/A" if growth_amount is None else f"{growth_amount:,.0f}"
        growth_percentage_display = "N/A" if growth_percentage is None else f"{growth_percentage:.2f}%"

        print(
            f"{year:<6} | "
            f"{month:<6} | "
            f"{revenue:>15,.0f} | "
            f"{previous_revenue_display:>15} | "
            f"{growth_amount_display:>15} | "
            f"{growth_percentage_display:>10}"
        )

    print("")
    print("Monthly Category Revenue Trend")
    print(
        f"{'Year':<6} | "
        f"{'Month':<6} | "
        f"{'Category':<15} | "
        f"{'Revenue':>15} | "
        f"{'Profit':>15} | "
        f"{'Sales':>8} | "
        f"{'Avg/Sale':>15} | "
        f"{'Margin %':>10}"
    )
    print("-" * 125)

    for row in get_monthly_category_revenue_trend():
        year, month, category, revenue, profit, num_of_sales, avg_revenue_per_sale, profit_margin = row

        print(
            f"{year:<6} | "
            f"{month:<6} | "
            f"{category:<15} | "
            f"{revenue:>15,.0f} | "
            f"{profit:>15,.0f} | "
            f"{num_of_sales:>8} | "
            f"{avg_revenue_per_sale:>15,.0f} | "
            f"{profit_margin:>9.2f}%"
        )

    category = "Electronics"

    print("")
    print(f"Monthly Revenue Growth for Category: {category}")
    print(
        f"{'Year':<6} | "
        f"{'Month':<6} | "
        f"{'Category':<15} | "
        f"{'Revenue':>15} | "
        f"{'Prev Revenue':>15} | "
        f"{'Growth':>15} | "
        f"{'Growth %':>10}"
    )
    print("-" * 115)

    for row in get_monthly_category_revenue_growth(category):
        year, month, category_name, revenue, previous_revenue, growth_amount, growth_percentage = row

        previous_revenue_display = "N/A" if previous_revenue is None else f"{previous_revenue:,.0f}"
        growth_amount_display = "N/A" if growth_amount is None else f"{growth_amount:,.0f}"
        growth_percentage_display = "N/A" if growth_percentage is None else f"{growth_percentage:.2f}%"

        print(
            f"{year:<6} | "
            f"{month:<6} | "
            f"{category_name:<15} | "
            f"{revenue:>15,.0f} | "
            f"{previous_revenue_display:>15} | "
            f"{growth_amount_display:>15} | "
            f"{growth_percentage_display:>10}"
        )