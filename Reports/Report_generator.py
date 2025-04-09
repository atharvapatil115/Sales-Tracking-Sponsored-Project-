import pandas as pd
import os
from datetime import datetime
from Database.database_connection import Create_connection
from Utils.data_logger import log_info

def get_file():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"Reports/Reports_daily/report_{today}.csv"

def update_total_sales(df):
    """ Remove old total row, calculate new total, and add it at the bottom. """
    df = df[df["Product ID"] != "Total Sales"]  # Remove existing total row if present
    total_amount = df["Total Amount"].sum()  # Calculate total sales

    # Create and append total row
    total_row = pd.DataFrame([{
        "Date": "", "Product ID": "Total Sales", "Category": "", "Brand Name": "",
        "Opening Balance": "", "Quantity Added": "", "Total": "", 
        "Sale": "", "Closing Balance": "", "Price": "", "Total Amount": total_amount
    }])
    df = pd.concat([df, total_row], ignore_index=True)

    return df

def generate_report(category, product_id, quantity_sold):
    file_path = get_file()
    
    columns = ["Date", "Product ID", "Category", "Brand Name", "Opening Balance", "Quantity Added", 
               "Total", "Sale", "Closing Balance", "Price", "Total Amount"]

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=columns)

    conn = Create_connection()
    cursor = conn.cursor()
    query = f"SELECT Brand_name, Opening_Balance, Closing_Balance, Price, Added, Total_Sale FROM {category} WHERE ID = ?"
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()
    
    if product is None:
        print(f"Product with ID {product_id} not found in category {category}.")
        return
    
    Brand_name, Opening_Balance, Closing_Balance, Price, quantity_added, total_sales = product

    existing_index = df[df["Product ID"] == product_id].index

    if not existing_index.empty:
        df.loc[existing_index, "Sale"] += quantity_sold
        df.loc[existing_index, "Closing Balance"] -= quantity_sold
        df.loc[existing_index, "Total Amount"] = df.loc[existing_index, "Sale"] * df.loc[existing_index, "Price"]
        print(f"Updated sales for product ID {product_id}.")
    else:
        new_data = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Product ID": product_id,
            "Category": category,
            "Brand Name": Brand_name,
            "Opening Balance": Opening_Balance,
            "Quantity Added": quantity_added,
            "Total": Opening_Balance + quantity_added,
            "Sale": quantity_sold,
            "Closing Balance": Closing_Balance - quantity_sold,
            "Price": Price,
            "Total Amount": quantity_sold * Price
        }])
        df = pd.concat([df, new_data], ignore_index=True)

    # Ensure total sales row is updated and at the bottom
    df = update_total_sales(df)

    df.to_csv(file_path, index=False)
    log_info(f"Sales report updated for {product_id} on {datetime.now().strftime('%Y-%m-%d')}")

def generate_report_update_sales(product_id, category, quantity_added):
    file_path = get_file()

    columns = ["Date", "Product ID", "Category", "Brand Name", "Opening Balance", "Quantity Added", 
               "Total", "Sale", "Closing Balance", "Price", "Total Amount"]

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=columns)

    conn = Create_connection()
    cursor = conn.cursor()
    query = f"SELECT Brand_name, Opening_Balance, Closing_Balance, Price, Added, Total_Sale FROM {category} WHERE ID = ?"
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()

    if product is None:
        print(f"Product with ID {product_id} not found in category {category}.")
        return

    Brand_name, Opening_Balance, Closing_Balance, Price, prev_quantity_added, total_sales = product

    existing_index = df[df["Product ID"] == product_id].index

    if not existing_index.empty:
        df.loc[existing_index, "Quantity Added"] += quantity_added
        df.loc[existing_index, "Total"] = df.loc[existing_index, "Opening Balance"] + df.loc[existing_index, "Quantity Added"]
        df.loc[existing_index, "Closing Balance"] += quantity_added
        print(f"Updated stock for product ID {product_id}.")
    else:
        new_data = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Product ID": product_id,
            "Category": category,
            "Brand Name": Brand_name,
            "Opening Balance": Opening_Balance,
            "Quantity Added": quantity_added,
            "Total": Opening_Balance + quantity_added,
            "Sale": total_sales,
            "Closing Balance": (quantity_added+Opening_Balance) - total_sales,
            "Price": Price,
            "Total Amount": total_sales * Price
        }])
        df = pd.concat([df, new_data], ignore_index=True)

    # Ensure total sales row is updated and at the bottom
    df = update_total_sales(df)

    df.to_csv(file_path, index=False)
    log_info(f"Stock report updated for {product_id} on {datetime.now().strftime('%Y-%m-%d')}")

def Combine(start_date,end_date):
    # Get user input for date range
    # start_date = input("Enter start date (YYYY-MM-DD): ")
    # end_date = input("Enter end date (YYYY-MM-DD): ")
    path = f"Reports/Reports_combined/Report_({start_date}to{end_date}).csv"

    # Convert to datetime for comparison
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Folder containing reports
    folder_path = r"C:\Users\patil\Desktop\Mini_Project\Sales_tracking\Stock_management\Reports\Reports_daily"  # Change this to your actual folder path

    # Get all CSV files in the folder
    report_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    # Combine reports
    combined_data = pd.DataFrame()

    for file in report_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        
        # Ensure 'Date' column is in datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  

        # Filter data within the given date range
        df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        
        # Append filtered data to combined dataframe
        combined_data = pd.concat([combined_data, df_filtered], ignore_index=True)

    # Save the combined report
    # output_file = f""
    combined_data.to_csv(path, index=False)
    print(f"Combined report saved as {path}")
    return combined_data