from Database.database_connection import Initilize_database
from Utils.data_logger import log_info, log_error, log_warning
from Database.database_handler import add_product, fetchProduct,update_sales,add_stock,Fetch_today,Fetch_all_items

from Reports import Report_generator
from Reports.Report_generator import Combine
from Database.Insert_database import insert_items


# Initilize_database()
# print("init success")
# insert_items()
# print("insert success!!")
# Fetch_all_items("Liquor")
# Fetch_all_items("Snacks")
# Fetch_all_items("ColdDrinks")

# vie_date()

def Category():
     print("1)Liquor\n2)Snacks\n3)ColdDrink")
     ch = int(input("Select the category of the product\t"))
     if ch == 1:
            category = 'Liquor'
     elif ch == 2:
            category = 'Snacks'
     else:
           category = 'ColdDrinks'
     return category
# category = Category()




if __name__ == "__main__":
        while True:
            print("\n1) Add product \n2) Update Sales \n3) fetch product\n4) Add Stock\n5) Todays Sales \n6) View all items7) Combine Reports")
            choice = int(input("Enter your choice\t"))

            match choice:
                case 1:
                    # add_product(category, product_id, Brand_name, price, opening_balance):
                    category = Category()
                    product_id = input("Enter the product id for the product\t")
                    Brand_name = input("Enter the Brand_name  for the product\t")
                    price = int(input("Enter the price  for the product\t"))
                    Opening_balance = int(input("Enter the Opening balance  for the product\t"))
                    add_product(category,product_id,Brand_name,price,Opening_balance)
                    print(f"product {Brand_name} successfully added in {category} category!")
                    log_info(f"product {Brand_name} successfully added in {category} category!")
                case 2:
                    #update_sales(category, product_id, quantity_sold):
                    category = Category()
                    product_id = input("Enter the product if of the product\t")
                    quantity_sold= int(input("Enter the quantity of the items sold\t"))
                    update_sales(category,product_id,quantity_sold)
                    print(f"Sales for product id {product_id} updated successfully!")
                    log_info(f"Sold {quantity_sold}  items of product id {product_id}!")

                case 3 :
                    #fetchProduct(category,product_id):
                    category = Category()
                    product_id = input("Enter the product id of the product \t")
                    Id, brandName, price, added, opening_balance ,closing_balance, Total_sale  = fetchProduct(category,product_id)
                    print(f"Product_id : {Id}\nBrand Name : {brandName}\nPrice : {price}\nAdded Quantity: {added}\nOpening Balance : {opening_balance}\nClosing Balance :{closing_balance}\nTotal Sale : {Total_sale}") 
                    log_info(f"Product information for product id : {product_id}, Brand Name : {brandName} fetched successfully!")       

                case 4:
                    #add_stock(product_id, category, quantity):
                    category = Category()
                    ID = input("Enter the product ID \t")
                    quantity = int(input("Enter the quantity of product to be added \t"))
                    add_stock(ID,category,quantity)
                    log_info(f"{quantity} items added of {category} in stock")
                case 5:
                      Fetch_today()
                case 6:
                      category = Category()
                      Fetch_all_items(category)
                case 7:
                      Combine()