import pandas as pd

def generate_summary(df):
    total_orders = df["InvoiceNo"].nunique()
    total_revenue = df["TotalAmount"].sum()
    average_order_value = df.groupby("InvoiceNo")["TotalAmount"].sum().mean()
    total_unique_products = df["StockCode"].nunique()

    # Top 5 countries by revenue
    top5_countries_df = df.groupby("Country")["TotalAmount"].sum().sort_values(ascending=False).head(5).reset_index()
    top5_countries_df.columns = ["Country", "Total Revenue"]

    # Top 5 products by quantity sold
    top5_products_df = df.groupby("Description")["Quantity"].sum().sort_values(ascending=False).head(5).reset_index()
    top5_products_df.columns = ["Product Description", "Total Quantity Sold"]

    # Main summary
    summary_df = pd.DataFrame({
        "Metric": [
            "Total Orders",
            "Total Revenue",
            "Average Order Value",
            "Total Unique Products"
        ],
        "Value": [
            total_orders,
            total_revenue,
            average_order_value,
            total_unique_products
        ]
    })

    return summary_df, top5_countries_df, top5_products_df
