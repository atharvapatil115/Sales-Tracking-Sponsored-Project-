from Utils.Exception import InsufficientStockError, DatabaseConnectionError, ProductNotFound
from Utils.data_logger import log_info, log_error, log_warning
from Database.database_connection import Create_connection
from Reports.Report_generator import generate_report, generate_report_update_sales
import pandas as pd
from datetime import datetime

import os


today = datetime.now().strftime("%Y-%m-%d")

def validate_category(category):
    valid_categories = ["Snacks", "Liquor", "ColdDrinks"]
    if category not in valid_categories:
        log_warning(f"Invalid Category: {category}")
        raise ValueError(f"Invalid Category: {category}")

def add_product(category, product_id, Brand_name, price, opening_balance):
    validate_category(category)
    conn = Create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"""INSERT INTO {category} 
                        (ID, Brand_name, Price, Opening_Balance, Closing_Balance, Added, Total_Sale)
                        VALUES (?, ?, ?, ?, ?, 0, 0)""",
                        (product_id, Brand_name, price, opening_balance, opening_balance))
        conn.commit()
        log_info(f"Product {Brand_name} Successfully Added")
    except Exception as e:
        log_error(f"Error inserting Product {Brand_name}: {e}")
        print(f"Error: {e}")
    finally:
        conn.close()

def add_stock(product_id, category, quantity):
    validate_category(category)
    conn = Create_connection()
    try:
        cursor = conn.cursor()
        
        # Fetch Opening Balance (OB)
        cursor.execute(f"SELECT Opening_Balance FROM {category} WHERE ID = ?", (product_id,))
        OB_row = cursor.fetchone()

        if OB_row is None:
            log_error(f"Product ID {product_id} not found in category {category}")
            raise ProductNotFound(f"Product ID {product_id} not found in category {category}")

        OB = OB_row[0]  # Extract integer value

        # Update Closing_Balance and Added
        cursor.execute(f"""UPDATE {category} 
                        SET Closing_Balance = Closing_Balance + ?, 
                            Added = Added + ?, 
                            Total = Opening_Balance + Added 
                        WHERE ID = ?""",
                        (quantity, quantity, product_id))
        
        conn.commit()
        log_info(f"Stock Added Successfully for {product_id}")

    except Exception as e:
        log_error(f"Unable to add Stock: {e}")
        raise ProductNotFound(f"Product not found: {e}")

    finally:
        conn.close()
        generate_report_update_sales(product_id, category, quantity)

def update_sales(category, product_id, quantity_sold):
    validate_category(category)
    conn = Create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT Price, Closing_Balance FROM {category} WHERE ID = ?", (product_id,))
        result = cursor.fetchone()
        if result:
            price, closing_balance = result
            new_balance = closing_balance - quantity_sold
            total_amount = quantity_sold * price
            print(total_amount)
            if new_balance < 0:
                log_error("Insufficient Stock")
                raise InsufficientStockError("Insufficient stock error", quantity_sold, new_balance)

            cursor.execute(f"UPDATE {category} SET Closing_Balance = ?, Total_Sale = Total_Sale + ? WHERE ID = ?", 
                           (new_balance, total_amount, product_id))
            conn.commit()
            log_info(f"Sales Updated Successfully for product: {product_id}")
            return total_amount
        else:
            log_error(f"Failed to update stock for {product_id}")
            return None
    except Exception as e:
        log_error(f"Error updating sales: {e}")
        return None
    finally:
        conn.close()
        generate_report(category, product_id, quantity_sold)

def fetchProduct(category, product_id):
    validate_category(category)
    conn = Create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {category} WHERE ID = ?", (product_id,))
        detail = cursor.fetchone()
        log_info(f"Detail fetched: {detail}")
        return detail
    except Exception as e:
        log_error(f"Cannot fetch product details {e}")
        raise ProductNotFound(f"Product not found: {e}")
    finally:
        conn.close()

def Fetch_today():
    try:
        data = pd.DataFrame(pd.read_csv(f"Reports/Reports_daily/report_{today}.csv"))
        print(data.to_string(index=False))
        log_info("Fetched today's sales")
    except Exception as e:
        log_error(f"Error fetching today's sales: {e}")
    return data

        
def Fetch_all_items(category):
    validate_category(category)
    conn = Create_connection()
    try:
        cursor = conn.cursor()
        query = f"""
            SELECT ID, Brand_name, Price, Opening_Balance, Added, 
                   (Opening_Balance + Added) AS Total, 
                   Closing_Balance, Total_Sale
            FROM {category}
        """
        cursor.execute(query)
        information = cursor.fetchall()

        allData = pd.DataFrame(information, 
                               columns=["ID", "Brand", "Price", "OB", "Added", "Total", "CB", "Total Sale"])

        log_info(f"Fetched all items from {category} successfully.")
        
        # print(f"\n{allData.to_string(index=False)}")

        return allData.values.tolist()
    except Exception as e:
        log_error(f"Error fetching items from {category}: {e}")
        raise DatabaseConnectionError
    finally:
        conn.close()

def create_tracking_table():
    conn = Create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS LastUpdate (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            last_date TEXT)""")
        
        cursor.execute("SELECT COUNT(*) FROM LastUpdate")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO LastUpdate (last_date) VALUES (?)", ("2025-01-01",))  # Set an old date initially
        
        conn.commit()
    except Exception as e:
        log_error(f"Error creating tracking table: {e}")
    finally:
        conn.close()

def initialize_daily_balance():
    conn = Create_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT last_date FROM LastUpdate")
        row = cursor.fetchone()
        last_date = row[0] if row else "2025-01-01"

        today = datetime.now().strftime("%Y-%m-%d")

        if last_date == today:
            log_info("OB already initialized for today.")
            return  

        for category in ["Snacks", "Liquor", "ColdDrinks"]:
            cursor.execute(f"""UPDATE {category} 
                               SET Opening_Balance = Closing_Balance,
                                   Added = 0""")  # Reset Added for new day

        cursor.execute("UPDATE LastUpdate SET last_date = ?", (today,))
        
        conn.commit()
        log_info("Opening Balance updated for all categories with previous CB values")
    except Exception as e:
        log_error(f"Error updating Opening Balance: {e}")
    finally:
        conn.close()


def view_date():
    conn = Create_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LastUpdate")
        date = cursor.fetchall()
        print(date)
    except Exception as e:
        log_error(f"Error fetching last update date: {e}")
    finally:
        conn.close()







def update_price(product_id,price,category):
    print(f"Category : {category}, updating price:{price},product_id : {product_id}")
    conn = Create_connection()
    print("Connection of database has been successfull for updating the price")
    try: 
        cursor = conn.cursor()
        cursor.execute(f"""Select Price from {category} where ID  = ?""",(product_id,))
        fetched_price = cursor.fetchone()
        print(f"Fetched price : {fetched_price}")
        fetched_price = price
        cursor.execute(f""" Update {category} Set Price = ? where ID  =?""",(fetched_price,product_id))
        log_info(f"Updated price for product ID : {product_id}")
        print(f"Updated price for product ID : {product_id}")
        conn.commit()
    
    except Exception as e:
        print(e)
        log_error(f"Unable to update the price : {e}")
        raise DatabaseConnectionError(f"Unable to update price: {e}")
    finally:
        conn.close()