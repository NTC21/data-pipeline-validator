 # first we want to run validate.py
import os
import pandas as pd
import csv
import sqlite3
from scripts import validate
from scripts import normalize_tables
# from scripts import load_to_db
from scripts import generate_summary
# from scripts import extract
from scripts.extract import CSVToDF
from scripts.load_to_db import load_to_db

# todo need to get the error_df inclduing all the erros in the csv file and the cleaned version 

def run_all():
    try:
        extractor = CSVToDF()
        df = extractor.create_df()
        print("✅ Data extraction complete.")
    except Exception as e:
        print("❌ Error during data extraction:", e)
        return

    try:
        valid_df, error_df = validate.run_all_validations(df)
        valid_df.to_csv("./webapp/output/cleaned_data.csv")
        error_df.to_csv("./webapp/output/error_report.csv")
        print("✅ Validation and error reporting complete.")
    except Exception as e:
        print("❌ Error during validation or saving cleaned/error files:", e)
        return

    try:
        summary_df, top5_countries_df, top5_products_df = generate_summary.generate_summary(valid_df)
        with pd.ExcelWriter("./webapp/output/summary_report.xlsx", engine="openpyxl") as writer:
            summary_df.to_excel(writer, sheet_name="Summary Overview", index=False)
            top5_countries_df.to_excel(writer, sheet_name="Top 5 Countries", index=False)
            top5_products_df.to_excel(writer, sheet_name="Top 5 Products", index=False)
        print("✅ Summary report generated.")
    except Exception as e:
        print("❌ Error generating summary report:", e)
        return

    try:
        orders_df = normalize_tables.normalize_orders(valid_df)
        orders_df.to_csv("./webapp/output/orders.csv")

        order_items_df = normalize_tables.normalize_order_items(valid_df)
        order_items_df.to_csv("./webapp/output/order_items.csv", index=False)

        products_df = normalize_tables.normalize_products(valid_df)
        products_df.to_csv("./webapp/output/products.csv")

        customers_df = normalize_tables.normalize_customers(valid_df)
        customers_df.to_csv("./webapp/output/customers.csv", index=False)

        print("✅ Normalized tables created and saved.")
    except Exception as e:
        print("❌ Error during normalization or saving tables:", e)
        return

    try:
        load_to_db()
        print("✅ Database loading complete.")
    except Exception as e:
        print("❌ Error loading data into DB:", e)
        return
if __name__ == "__main__": 
    run_all()
    pass