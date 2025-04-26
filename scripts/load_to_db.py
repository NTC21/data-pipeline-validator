import sqlite3
import pandas as pd
import os

def load_to_db():
    # Ensure the database directory exists
    os.makedirs("./webapp/output/db", exist_ok=True)

    # Connect to the SQLite database 
    conn = sqlite3.connect("./webapp/output/db/ecommerce.db")
    cursor = conn.cursor()

    # List of CSVs to load
    tables = {
        "orders": "./webapp/output/orders.csv",
        "order_items": "./webapp/output/order_items.csv",
        "products": "./webapp/output/products.csv",
        "customers": "./webapp/output/customers.csv"
    }

    for table_name, file_path in tables.items():
        print(f"Loading {file_path} into '{table_name}' table...")
        
        # Load CSV into DataFrame
        df = pd.read_csv(file_path)
        
        #  DataFrame to SQL table
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        

    # Close the connection
    conn.close()
    return
