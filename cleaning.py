import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r"C:\Users\Yogeendra\Downloads\SuperStoreOrders.csv\SuperStoreOrders.csv")
print(df.head(5))
print(df.tail(5))

print(df.shape)
print(df.columns)
print(df.info())

#cleanig 
print(df.drop_duplicates())
print(df.duplicated().sum())

print(df.isnull().sum())
df.fillna(0, inplace=True)
print(df.dropna())


#converting date columns
df['order_date'] = pd.to_datetime(df['order_date'], dayfirst=True)
df['ship_date'] = pd.to_datetime(df['ship_date'], dayfirst=True)

df['delivery_days']=(df['ship_date']-df['order_date']).dt.days
print(df['delivery_days'].head(5))

df['profit']=pd.to_numeric(df['profit'], errors='coerce')
df['sales']=pd.to_numeric(df['sales'], errors='coerce')
df['profit_margin'] = (df['profit']/df['sales'])*100
print(df['profit_margin'].head(5))

df['order_year']=df['order_date'].dt.year
print(df['order_year'].head(5))

df['order_month']=df['order_date'].dt.month_name()
print(df['order_month'].head(5))

df['quarter']=df['order_date'].dt.quarter
print(df['quarter'].head(5))

df.describe()

#EDA
total_sales=df['sales'].sum()
print(total_sales)

total_profit=df['profit'].sum()
print(total_profit)

category_sales=df.groupby('category')['sales'].sum()
print(category_sales)

region_profit=df.groupby('region')['profit'].sum()
print(region_profit)

top_customers=(df.groupby('customer_name')['sales'].sum().sort_values(ascending=False).head(10))
print(top_customers)

monthly_sales=df.groupby('order_month')['sales'].sum()
print(monthly_sales)

#data visualization

#sales by category
plt.figure(figsize=(8,5))
sns.barplot(x=category_sales.index,
            y=category_sales.values,
            palette='viridis')
plt.title('Sales by Category')
plt.xlabel('category')
plt.ylabel('total sales')
plt.show()

#profit by region

plt.figure(figsize=(8,5))
sns.barplot(x=region_profit.index,
            y=region_profit.values,
            palette='viridis')
plt.title('Profit by Region')
plt.xlabel('Region')
plt.ylabel('Total Profit')
plt.xticks(rotation=45)
plt.show()

#monthly sales trend

plt.figure(figsize=(12,5))

monthly_sales.plot(kind='line',marker='o')
plt.title("monthly sales trend")
plt.show()

#correlation heatmap

plt.figure(figsize=(10,6))

sns.heatmap(df[['sales','profit','discount','quantity']].corr(),annot=True)
plt.show()

df.to_csv("cleaned_superstore_data.csv", index=False)

