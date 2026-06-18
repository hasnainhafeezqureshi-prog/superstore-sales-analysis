import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

store_df = pd.read_csv("Sample - Superstore.csv", encoding="windows-1252")

# DATA PREPROCESSING AND CLEANING

# print("Data Overview:")
# print(store_df.head())
# print(store_df.info())
# print(store_df.describe())

store_df["Order Date"] = pd.to_datetime(store_df["Order Date"])
store_df["Ship Date"] = pd.to_datetime(store_df["Ship Date"])

catgories = ["Ship Mode", "Region", "Category", "Sub-Category", "Segment"]
# Converted to category dtype so no need to store one value multiple times. Each category will be stored once then it will be referred to using numericals.
for each in catgories:
    store_df[each] = store_df[each].astype("category")

# print(store_df.isnull().sum())                          # NO NULL VALUES
# print(store_df.duplicated().sum())                          # NO DUPLICATE ROWS SO NOTHING TO DROP

delays = store_df['Ship Date'] - store_df['Order Date']
store_df['Shipping Delay'] = delays

# print(store_df['Shipping Delay'].describe())                       # TO KNOW THE MAX SHIPPING DELAY

mask = (store_df['Shipping Delay'] > pd.Timedelta(days=7)) | (store_df['Shipping Delay'] < pd.Timedelta(days=0))
# print(store_df[mask])                                       # PRINTS 'Empty Dataframe' WHICH MEANS NO DELAY IS NEGATIVE AND NO LARGE    
                                                            # DELAY AS EVERY SHIPPING IS UNDER ONE WEEK

# ANALYSIS

sales_profit_region = store_df.groupby('Region')[['Sales', 'Profit']].sum()
sales_profit_cat = store_df.groupby('Product Name')[['Sales', 'Profit']].sum()
ten_best_selling = sales_profit_cat.loc[:,'Sales'].nlargest(10)
best_selling_prods = ten_best_selling.index
print(best_selling_prods)

max_profit_segment = store_df.groupby('Segment')['Profit'].sum().idxmax()
print(max_profit_segment)

month = store_df['Order Date'].dt.month
year = store_df['Order Date'].dt.year

month_year_sales_trend = store_df.groupby([year, month])['Sales'].sum()
month_year_sales_trend.index.names = ['Year', 'Month']
month_year_sales_trend = month_year_sales_trend.reset_index()
month_year_sales_trend['Date'] = pd.to_datetime(
    month_year_sales_trend['Year'].astype(str) + '-' + month_year_sales_trend['Month'].astype(str) + '-01'
)
# print(month_year_sales_trend)

negative_profit = store_df[store_df['Profit'] < 0]
non_profit_percent = (len(negative_profit)/len(store_df)) * 100
print(non_profit_percent)

# PATTERN CAN BE SEEN WITH THE HELP OF THREE LINES BELOW. PRODUCTS WITH CATEGORY FURNITURE AND OFFICE SUPPLIES MAKE LESS PROFIT
print(negative_profit['Region'].value_counts())
print(negative_profit['Discount'].value_counts())
print(negative_profit['Sub-Category'].value_counts())
print(negative_profit['Category'].value_counts())

# RATE OF NEGATIVE PROFIT PER CATEGORY, NOT JUST RAW COUNT, SINCE CATEGORIES HAVE DIFFERENT TOTAL ORDER VOLUMES
negative_rate_category = (negative_profit['Category'].value_counts() / store_df['Category'].value_counts()) * 100
print(negative_rate_category)

negative_rate_subcat = (negative_profit['Sub-Category'].value_counts() / store_df['Sub-Category'].value_counts()) * 100
print(negative_rate_subcat)

groupby_customer = store_df.groupby(['Customer ID', 'Customer Name']).agg({'Order ID' : 'count', 'Sales' : 'sum', 'Order Date' : 'max'}).nlargest(10, 'Sales')
top10_customers = groupby_customer.index.map(lambda x:x[1])
print(top10_customers)

target_cols = ['Sales', 'Profit', 'Quantity', 'Discount']
corr_matrix = store_df[target_cols].corr()
print(corr_matrix)

# VISUALIZE

plt.figure(figsize=(8,6))
plt.title('Region-Wise Sales')
sns.barplot(data=sales_profit_region.reset_index(), x='Region', y='Sales', color='green')
plt.show()

profit_cat = store_df.groupby('Category')['Profit'].sum()
plt.figure(figsize=(8,6))
plt.title('Category-Wise Profit')
sns.barplot(data=profit_cat.reset_index(), x='Category', y='Profit', color='purple')
plt.show()

plt.figure(figsize=(14, 6))
sns.lineplot(data=month_year_sales_trend, x='Date', y='Sales')
plt.title('Sales Trend Over Time')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

sns.scatterplot(data=store_df, x='Discount', y='Profit', hue='Profit', palette='plasma')
plt.title('Discount vs Profit')
sns.despine()
plt.show()

sns.heatmap(data=corr_matrix, annot=True)
plt.title('Correlation Matrix Heatmap')
plt.show()

plt.figure(figsize=(12, 8))
sns.boxplot(
    data=store_df, 
    x='Profit', 
    y='Sub-Category', 
    palette='Set3',
    fliersize=3 # Shrinks the outlier dot sizes so they don't crowd the chart
)
plt.tight_layout()
plt.show()


print('East and West have the highest sales among all regions, while Central and South lag behind. Among categories, Technology generates the most profit while Furniture generates the least, based on profit_cat. Sales fluctuate month to month but show an overall upward trend from 2014 to 2018. Profit and Discount show a weak negative correlation (-0.219), and the relationship is non-linear: profit drops sharply around the 0.5 discount level specifically, then partially recovers at higher discounts, rather than declining steadily as discount increases. The Machines sub-category shows a wide profit spread in the boxplot, with profits ranging from notably negative to highly positive, indicating inconsistent profitability rather than higher or lower profit on average.')

print('If I were advising this business, I would recommend specifically restricting or reviewing the 0.5 discount tier, since it shows the steepest profit loss in the data, while smaller discounts under 0.2 do not show meaningful profit damage. I would also recommend reviewing pricing or cost structure for the Machines sub-category given its inconsistent profitability.')