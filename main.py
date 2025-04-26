 # first we want to run validate.py
import os
import boto3.s3
import pandas as pd
import csv
import sqlite3
from scripts import validate
from scripts import normalize_tables
from scripts import generate_summary
from scripts.load_to_db import load_to_db
import boto3
import io
from webapp.config import S3_BUCKET_NAME


os.makedirs("webapp/output", exist_ok=True)
os.makedirs("webapp/output/db", exist_ok=True)
# todo need to get the error_df inclduing all the erros in the csv file and the cleaned version 

def run_all():
    try:
        # extractor = CSVToDF()
        # df = extractor.create_df()
        s3_client = boto3.client('s3')
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key='uploads/data.csv')
        body = response['Body']
        # io.BytesIO turns the streaming data in a 'fake file' so that pandas can properly work on it
        df = pd.read_csv(io.BytesIO(body.read()), encoding='ISO-8859-1')

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