# Superstore Sales & Profitability Analysis

A complete exploratory data analysis of the Superstore retail dataset using Python, Pandas, NumPy, Matplotlib, and Seaborn — covering data cleaning, business-focused analysis, and visualization.

## Dataset

[Superstore Sales Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) — order-level retail data including sales, profit, discount, customer, product, and shipping information across 2014-2018.

## Objective

Analyze regional and category-level sales performance, identify profitability patterns, evaluate the impact of discounting, and surface actionable business recommendations.

## Approach

**1. Data Cleaning**
- Converted `Order Date` and `Ship Date` to proper datetime format
- Cast categorical columns (`Region`, `Category`, `Sub-Category`, `Segment`, `Ship Mode`) to `category` dtype for memory efficiency
- Engineered a `Shipping Delay` feature and validated it for data integrity (no negative or abnormal delays found)
- Verified no missing values or duplicate rows

**2. Analysis**
- Sales and profit breakdown by Region, Category, and Sub-Category
- Top 10 best-selling products (by sales) and top 10 customers (by spend)
- Identified the most profitable customer segment
- Quantified the rate of unprofitable orders by category and sub-category (not just raw counts, to account for differing order volumes)
- Built a correlation matrix across Sales, Profit, Quantity, and Discount
- Investigated the Discount-Profit relationship in depth, revealing a non-linear pattern that a simple correlation coefficient alone fails to capture

**3. Visualization**
- Bar charts: Sales by Region, Profit by Category
- Line chart: Monthly sales trend (2014-2018)
- Scatter plot: Discount vs Profit
- Heatmap: Correlation matrix
- Box plot: Profit distribution by Sub-Category

## Key Findings

- East and West regions generate the highest sales, while Central and South lag behind
- Profit and Discount show only a weak linear correlation (-0.219) — but the actual relationship is non-linear, with profit cratering sharply around the 0.5 discount tier specifically rather than declining steadily as discount increases
- The Machines sub-category shows highly inconsistent profitability, with a wide spread between loss-making and high-profit orders
- Overall sales trend upward from 2014 to 2018, with month-to-month fluctuation likely tied to seasonality

## Recommendations

- Restrict or review pricing at the 0.5 discount tier specifically, since it shows the steepest profit loss in the data, while discounts under 0.2 show minimal profit impact
- Review pricing or cost structure for the Machines sub-category given its inconsistent profit performance

## Tools Used

Python, Pandas, NumPy, Matplotlib, Seaborn

## Author

Hasnain Qureshi — [GitHub](https://github.com/hasnainhafeezqureshi-prog)