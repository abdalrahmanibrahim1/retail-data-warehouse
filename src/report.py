from src.load import get_connection
import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"

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

def format_text(value):
    if value is None:
        return "N/A"

    return str(value).replace("|", "\\|")

def format_money(value):
    if value is None:
        return "N/A"

    return f"{value:,.0f}"

def format_int(value):
    if value is None:
        return "N/A"
        
    return f"{value:,}"

def format_percent(value):
    if value is None:
        return "N/A"

    return f"{value:.2f}%"

def csv_value(value):
    if value is None:
        return ""

    return value

def save_csv_report(filename, headers, rows):
    REPORTS_DIR.mkdir(exist_ok=True)

    output_path = REPORTS_DIR / filename

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for row in rows:
            writer.writerow([csv_value(value) for value in row])

def add_markdown_table(lines, title, headers, rows, formatters, max_rows=None):
    lines.append("")
    lines.append(f"## {title}")
    lines.append("")

    if not rows:
        lines.append("_No data available._")
        return

    display_rows = rows if max_rows is None else rows[:max_rows]

    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for row in display_rows:
        formatted_values = []

        for value, formatter in zip(row, formatters):
            formatted_values.append(formatter(value))

        lines.append("| " + " | ".join(formatted_values) + " |")

    if max_rows is not None and len(rows) > max_rows:
        lines.append("")
        lines.append(f"_Showing first {max_rows} rows. Full report available in CSV output._")


def generate_report(category_for_growth="Electronics"):
    REPORTS_DIR.mkdir(exist_ok=True)

    total_revenue, total_profit = get_total_revenue_and_profit()

    revenue_by_category = get_total_revenue_by_product_category()
    top_products = get_top_5_products_by_revenue()
    sales_by_city = get_sales_by_store_city()
    customer_segment_revenue = get_revenue_by_customer_segment()
    monthly_revenue_trend = get_monthly_revenue_trend()
    category_city_segment = get_category_city_segment_performance()
    category_margin_ranking = get_category_profit_margin_ranking()
    customer_segment_avg_sale = get_customer_segment_average_sale_ranking()
    monthly_revenue_growth = get_monthly_revenue_growth()
    monthly_category_trend = get_monthly_category_revenue_trend()
    monthly_category_growth = get_monthly_category_revenue_growth(category_for_growth)

    save_csv_report(
        "warehouse_summary.csv",
        ["metric", "value"],
        [
            ("total_revenue", total_revenue),
            ("total_profit", total_profit),
        ],
    )

    save_csv_report(
        "revenue_by_product_category.csv",
        ["category", "total_revenue"],
        revenue_by_category,
    )

    save_csv_report(
        "top_5_products_by_revenue.csv",
        [
            "product_name",
            "category",
            "total_revenue",
            "total_profit",
            "number_of_sales",
            "average_revenue_per_sale",
            "profit_margin_percentage",
        ],
        top_products,
    )

    save_csv_report(
        "sales_by_store_city.csv",
        [
            "store_city",
            "total_revenue",
            "total_profit",
            "number_of_sales",
        ],
        sales_by_city,
    )

    save_csv_report(
        "revenue_by_customer_segment.csv",
        [
            "customer_segment",
            "total_revenue",
            "total_profit",
            "number_of_sales",
            "average_revenue_per_sale",
            "profit_margin_percentage",
        ],
        customer_segment_revenue,
    )

    save_csv_report(
        "monthly_revenue_trend.csv",
        [
            "year",
            "month",
            "total_revenue",
            "total_profit",
            "number_of_sales",
            "average_revenue_per_sale",
            "profit_margin_percentage",
        ],
        monthly_revenue_trend,
    )

    save_csv_report(
        "category_city_segment_performance.csv",
        [
            "store_city",
            "customer_segment",
            "category",
            "total_revenue",
            "total_profit",
            "number_of_sales",
            "average_revenue_per_sale",
            "profit_margin_percentage",
        ],
        category_city_segment,
    )

    save_csv_report(
        "category_profit_margin_ranking.csv",
        [
            "category",
            "total_revenue",
            "total_profit",
            "number_of_sales",
            "average_revenue_per_sale",
            "profit_margin_percentage",
        ],
        category_margin_ranking,
    )

    save_csv_report(
        "customer_segment_average_sale_ranking.csv",
        [
            "customer_segment",
            "total_revenue",
            "total_profit",
            "number_of_sales",
            "average_revenue_per_sale",
            "profit_margin_percentage",
        ],
        customer_segment_avg_sale,
    )

    save_csv_report(
        "monthly_revenue_growth.csv",
        [
            "year",
            "month",
            "total_revenue",
            "previous_month_revenue",
            "growth_amount",
            "growth_percentage",
        ],
        monthly_revenue_growth,
    )

    save_csv_report(
        "monthly_category_revenue_trend.csv",
        [
            "year",
            "month",
            "category",
            "total_revenue",
            "total_profit",
            "number_of_sales",
            "average_revenue_per_sale",
            "profit_margin_percentage",
        ],
        monthly_category_trend,
    )

    save_csv_report(
        f"{category_for_growth.lower()}_monthly_revenue_growth.csv",
        [
            "year",
            "month",
            "category",
            "total_revenue",
            "previous_month_revenue",
            "growth_amount",
            "growth_percentage",
        ],
        monthly_category_growth,
    )

    lines = []

    lines.append("# Retail Data Warehouse Report")
    lines.append("")
    lines.append("This report was generated from the PostgreSQL star-schema warehouse.")
    lines.append("")
    lines.append("## Overall Warehouse Summary")
    lines.append("")
    lines.append(f"- **Total revenue:** {format_money(total_revenue)}")
    lines.append(f"- **Total profit:** {format_money(total_profit)}")

    add_markdown_table(
        lines,
        "Revenue by Product Category",
        ["Category", "Revenue"],
        revenue_by_category,
        [format_text, format_money],
    )

    add_markdown_table(
        lines,
        "Top 5 Products by Revenue",
        ["Product", "Category", "Revenue", "Profit", "Sales", "Avg/Sale", "Margin %"],
        top_products,
        [format_text, format_text, format_money, format_money, format_int, format_money, format_percent],
    )

    add_markdown_table(
        lines,
        "Sales by Store City",
        ["Store City", "Revenue", "Profit", "Sales"],
        sales_by_city,
        [format_text, format_money, format_money, format_int],
    )

    add_markdown_table(
        lines,
        "Revenue by Customer Segment",
        ["Segment", "Revenue", "Profit", "Sales", "Avg/Sale", "Margin %"],
        customer_segment_revenue,
        [format_text, format_money, format_money, format_int, format_money, format_percent],
    )

    add_markdown_table(
        lines,
        "Monthly Revenue Trend",
        ["Year", "Month", "Revenue", "Profit", "Sales", "Avg/Sale", "Margin %"],
        monthly_revenue_trend,
        [format_int, format_int, format_money, format_money, format_int, format_money, format_percent],
    )

    add_markdown_table(
        lines,
        "Category Performance by City and Customer Segment",
        ["City", "Segment", "Category", "Revenue", "Profit", "Sales", "Avg/Sale", "Margin %"],
        category_city_segment,
        [format_text, format_text, format_text, format_money, format_money, format_int, format_money, format_percent],
        max_rows=20,
    )

    add_markdown_table(
        lines,
        "Category Profit Margin Ranking",
        ["Category", "Revenue", "Profit", "Sales", "Avg/Sale", "Margin %"],
        category_margin_ranking,
        [format_text, format_money, format_money, format_int, format_money, format_percent],
    )

    add_markdown_table(
        lines,
        "Customer Segment Average Sale Ranking",
        ["Segment", "Revenue", "Profit", "Sales", "Avg/Sale", "Margin %"],
        customer_segment_avg_sale,
        [format_text, format_money, format_money, format_int, format_money, format_percent],
    )

    add_markdown_table(
        lines,
        "Monthly Revenue Growth",
        ["Year", "Month", "Revenue", "Previous Revenue", "Growth", "Growth %"],
        monthly_revenue_growth,
        [format_int, format_int, format_money, format_money, format_money, format_percent],
    )

    add_markdown_table(
        lines,
        "Monthly Category Revenue Trend",
        ["Year", "Month", "Category", "Revenue", "Profit", "Sales", "Avg/Sale", "Margin %"],
        monthly_category_trend,
        [format_int, format_int, format_text, format_money, format_money, format_int, format_money, format_percent],
        max_rows=30,
    )

    add_markdown_table(
        lines,
        f"Monthly Revenue Growth for Category: {category_for_growth}",
        ["Year", "Month", "Category", "Revenue", "Previous Revenue", "Growth", "Growth %"],
        monthly_category_growth,
        [format_int, format_int, format_text, format_money, format_money, format_money, format_percent],
    )

    markdown_report_path = REPORTS_DIR / "warehouse_report.md"

    with open(markdown_report_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    print(f"Reports generated successfully in {REPORTS_DIR}/")


if __name__ == "__main__":
    generate_report()