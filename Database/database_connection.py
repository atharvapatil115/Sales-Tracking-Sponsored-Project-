import sqlite3 as sql 
from Utils.Exception import DatabaseConnectionError
from Utils.data_logger import log_error, log_info,log_warning
import os

database_name = r'C:\Users\patil\Desktop\Mini_Project\Sales_tracking\Stock_management\Database\database.db'

def Create_connection():
    try:
        conn = sql.connect(database_name)
        log_info("Database Connection Successfully!")
        return conn
    except sql.Error as e:
        log_error(f"Database Connection Unsuccessfull:  {e}")
        raise DatabaseConnectionError(f"Database Connection Unsuccessfully: {e}")

def Initilize_database():

    # if not os.path.exists("Database_schema.sql"):
    #      log_error(f"Database schema file '{"Database_schema.sql"}' not found!")
    #      raise FileNotFoundError(f"Database schema file '{"Database_schema.sql"}' not found!")
    print("Current Working Directory:", os.getcwd())
    conn = Create_connection()
    if conn:
        try:
            with open("Database/Database_schema.sql",'r') as f:
                conn.executescript(f.read())
            conn.commit()
            log_info("Database Initlized Successfully")
        except Exception as e:
            log_error(f"Database initilization unsuccessful : {e}")
            # raise DatabaseConnectionError(e)  
            print("database Initlization error")