import sqlite3
import pandas as pd
import os

def load_to_db():
    # Ensure the database directory exists
    os.makedirs("./db", exist_ok=True)

    # Connect to the SQLite database 
    conn = sqlite3.connect("./db/ecommerce.db")
    cursor = conn.cursor()

    # List of CSVs to load
    tables = {
        "orders": "./output/orders.csv",
        "order_items": "./output/order_items.csv",
        "products": "./output/products.csv",
        "customers": "./output/customers.csv"
    }

    for table_name, file_path in tables.items():
        print(f"Loading {file_path} into '{table_name}' table...")
        
        # Load CSV into DataFrame
        df = pd.read_csv(file_path)
        
        #  DataFrame to SQL table
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        
        print(f"✅ Inserted {len(df)} rows into '{table_name}'")

    # Close the connection
    conn.close()
    # print("✅ Database write complete. DB located at: ./db/ecommerce.db")
    return
