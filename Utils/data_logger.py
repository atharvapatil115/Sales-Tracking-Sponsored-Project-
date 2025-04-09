import logging 
import logging.config
import os 
from datetime import datetime

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

file_name  = f"logs\{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    level = logging.INFO,
    format  = '%(asctime)s - %(levelname)s - %(message)s',
    handlers =[
        logging.FileHandler(file_name),
        logging.StreamHandler()
    ],
    force=True
)

def log_info(message):
    logging.info(message)

def log_warning(message):
    logging.warning(message)

def log_error(message):
    logging.error(message)