import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# read csv
df = pd.read_csv(
    r"C:\Users\Yogeendra\OneDrive\Documents\superstore_analysis_project\cleaned_superstore_data.csv"
)

# replace infinity values
df.replace([np.inf, -np.inf], 0, inplace=True)

# create customer_id
df['customer_id'] = (
    df['customer_name']
    .astype('category')
    .cat.codes
)

# -----------------------------
# CREATE TABLES
# -----------------------------

# customers table
customers = df[
    ['customer_id', 'customer_name', 'segment']
].drop_duplicates()

# products table
products = df[
    ['product_id', 'product_name', 'category', 'sub_category']
].drop_duplicates()

# orders table
orders = df[
    [
        'order_id',
        'order_date',
        'ship_date',
        'ship_mode',
        'customer_id',
        'country',
        'state',
        'market',
        'region',
        'order_priority'
    ]
].drop_duplicates(subset=['order_id'])



# sales table
sales = df[
    [
        'order_id',
        'product_id',
        'sales',
        'quantity',
        'discount',
        'profit'
    ]
]

# -----------------------------
# MYSQL CONNECTION
# -----------------------------

engine = create_engine(
    "mysql+pymysql://root:yogi%40sql@localhost/superstore_db"
)

# -----------------------------
# UPLOAD TABLES
# -----------------------------
df.to_sql(
    name='superstore_data',
    con=engine,
    if_exists='replace',
    index=False
)


customers.to_sql(
    'customers',
    con=engine,
    if_exists='replace',
    index=False
)

products.to_sql(
    'products',
    con=engine,
    if_exists='replace',
    index=False
)

orders.to_sql(
    'orders',
    con=engine,
    if_exists='replace',
    index=False
)

sales.to_sql(
    'sales',
    con=engine,
    if_exists='replace',
    index=False
)

print("All tables uploaded successfully!")