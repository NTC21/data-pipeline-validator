import pandas as pd
import numpy as np
# from scripts.extract import CSVToDF

# extractor = CSVToDF()     # Create an instance
# df = extractor.create_df()  # Call the method on that instance

# --- VALIDATION FUNCTIONS ---

def check_invoice_no(df):
    # Check if InvoiceNo is a string and not null
    mask_invalid_type = ~df["InvoiceNo"].apply(lambda x: isinstance(x, str))
    mask_null = df["InvoiceNo"].isnull() # check if any entry is empty
    mask_empty = df["InvoiceNo"].astype(str).str.strip() == "" # check if entered with whitespace

    # Combine all invalid conditions
    full_mask = mask_invalid_type | mask_null | mask_empty
    invalid_df = df[full_mask].copy()
    invalid_df["error_reason"] = "Invalid InvoiceNo (not string, null, or empty)"
    return invalid_df

# check if the quantity is a number
def check_quantity(df):
    # Convert Quantity to numeric (invalid values become NaN)
    quantity_numeric = pd.to_numeric(df["Quantity"], errors="coerce")

    mask_invalid = quantity_numeric.isna()

    invalid_df = df[mask_invalid].copy()
    invalid_df["error_reason"] = "Invalid Quantity (not numeric or <= 0)"
    return invalid_df

def check_unit_price(df):
    quantity_numeric = pd.to_numeric(df["UnitPrice"], errors="coerce")
    
    mask_invalid = quantity_numeric.isna() | (quantity_numeric < 0)
    invalid_df = df[mask_invalid].copy()
    invalid_df["error_reason"] = "invalid unit price or < 0"
    return invalid_df

# * only flag if missing when quantity >0
def check_description(df):
    mask_invalid = ~df["Description"].apply(lambda x: isinstance(x, str))
    mask_null = df["Description"].isnull()
    mask_empty = df["Description"].astype(str).str.strip() == ""

    bad_desc_mask = mask_invalid | mask_null | mask_empty

    quantity_numeric = pd.to_numeric(df["Quantity"], errors="coerce")
    mask_quantity_positive = quantity_numeric.notna() & (quantity_numeric > 0)

    full_mask = bad_desc_mask & mask_quantity_positive

    invalid_df = df[full_mask].copy()
    invalid_df["error_reason"] = "Invalid Description (missing for Quantity > 0)"
    return invalid_df

def check_invoice_date(df):
    quantity_datetime = pd.to_datetime(df["InvoiceDate"], errors="coerce")

    mask_invalid = quantity_datetime.isna()
    invalid_df = df[mask_invalid].copy()
    invalid_df["error_reason"] = "Date time is invalid "
    return invalid_df
    

def check_customer_id(df):
    mask_invalid = ~(df["CustomerID"].isna() | pd.to_numeric(df["CustomerID"], errors="coerce").notna())

    invalid_df = df[mask_invalid].copy()
    invalid_df["error_reason"] = "invalid customerID"
    return invalid_df


def check_country(df):
    mask_invalid = df["Country"].isna() | ~df["Country"].apply(lambda x: isinstance(x, str))
    invalid_df = df[mask_invalid].copy()

    invalid_df["error_reason"] = "invalid Country"

    return invalid_df

# --- VALIDATION RUNNER ---

def run_all_validations(df):
    error_rows = [] # this will store the error with the reason

    # Add checks here

    invoice_issues = check_invoice_no(df)
    error_rows.append(invoice_issues)

    quantity_issues = check_quantity(df)
    error_rows.append(quantity_issues)

    unit_price_issues = check_unit_price(df)
    error_rows.append(unit_price_issues)

    description_issues = check_description(df)
    error_rows.append(description_issues)

    datetime_issues = check_invoice_date(df)
    error_rows.append(datetime_issues)

    customerID_issues = check_customer_id(df)
    error_rows.append(customerID_issues)

    country_issues = check_country(df)
    error_rows.append(country_issues)

    # Combine all invalids
    error_df = pd.concat(error_rows) # combines multiple dataframes that are in the lits into one dataframe
    valid_df = df[~df.index.isin(error_df.index)].copy()


    valid_df["Quantity"] = pd.to_numeric(valid_df["Quantity"], errors="coerce")
    valid_df["UnitPrice"] = pd.to_numeric(valid_df["UnitPrice"], errors="coerce")
    valid_df["TotalAmount"] = valid_df["Quantity"] * valid_df["UnitPrice"]
    
    return valid_df, error_df

