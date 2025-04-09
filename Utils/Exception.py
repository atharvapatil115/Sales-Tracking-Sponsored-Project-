class DatabaseConnectionError(Exception):
    def __init__(self,message = "Failed to connect to the database"):
        self.message = message
        super().__init__(self.message)

class InsufficientStockError(Exception):
    def __init__(self,product_id,req_stock,avail_stock):
        self.product_id = product_id
        self.req_stock = req_stock
        self.avail_stock = avail_stock
        self.message = f"Insufficient Stock available for product id: {product_id}\nRequested Stock :{req_stock}\nAvailable Stock : {avail_stock}"
        super().__init__(self.message)
         
class ProductNotFound(Exception):
    def __init__(self,product_id,message = "product not found"):
        self.product_id = product_id
        self.message = f"{message} for product ID : {product_id}"
        super().__init__(self.message)

# Database Initlization error class yet to be created 