import pandas as pd

# Load cleaned data
# df = pd.read_csv("./output/cleaned_data.csv", encoding='ISO-8859-1')

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

# ---TESTING---
# if __name__ == "__main__":
#     summary_df, top5_countries_df, top5_products_df = generate_summary(df)

#     with pd.ExcelWriter("./output/summary_report.xlsx", engine="openpyxl") as writer:
#         summary_df.to_excel(writer, sheet_name="Summary Overview", index=False)
#         top5_countries_df.to_excel(writer, sheet_name="Top 5 Countries", index=False)
#         top5_products_df.to_excel(writer, sheet_name="Top 5 Products", index=False)

#     print("Summary files written to /output")
