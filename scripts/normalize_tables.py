import pandas as pd

def normalize_orders(df):
    # Group and extract necessary values
    orders = df.groupby("InvoiceNo")["TotalAmount"].sum()
    countries = df.groupby("InvoiceNo")["Country"].first()
    invoice_dates = df.groupby("InvoiceNo")["InvoiceDate"].first()
    customer_ids = df.groupby("InvoiceNo")["CustomerID"].first()

    # Combine into one DataFrame side-by-side
    normalize_order_df = pd.concat([customer_ids, invoice_dates, countries, orders], axis=1)
    normalize_order_df.reset_index(inplace=True)

    return normalize_order_df

def normalize_order_items(df):
    # Convert columns to numeric to ensure math works
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    # Calculate line-level total (Quantity × UnitPrice)
    df["LineTotal"] = df["Quantity"] * df["UnitPrice"]

    # Keep only the relevant columns for order_items
    order_items_df = df[["InvoiceNo", "StockCode", "Quantity", "LineTotal"]].copy()

    return order_items_df

def normalize_products(df):
    products = df.groupby("StockCode")["Description"].first()

    UnitPrice = df.groupby("StockCode")["UnitPrice"].mean()
    normalize_products_df = pd.concat([products, UnitPrice], axis=1)
    normalize_products_df.reset_index(inplace=True)

    return normalize_products_df

def normalize_customers(df):
    # Drop rows where CustomerID is missing
    customers_df = df[["CustomerID", "Country"]].dropna()

    # Drop duplicates — keep one row per customer
    customers_df = customers_df.drop_duplicates()

    # Optional: sort for neatness
    customers_df['CustomerID'] = customers_df['CustomerID'].astype(float) # converting the strings to float so that we can sort by those values
    customers_df = customers_df.sort_values(by="CustomerID")

    return customers_df

