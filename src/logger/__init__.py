import logging
import os
import sys
from datetime import datetime

LOG_DIR = "logs"
# here we are joining this LOG_DIR directory with main working directory
LOG_DIR = os.path.join(os.getcwd(), LOG_DIR)

# create log directory if it is not exist
os.makedirs(LOG_DIR, exist_ok=True)

# to set log file extension .log with current timestamp
Current_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
file_name = f"log_{Current_TIME_STAMP}.log"

log_file_path = os.path.join(LOG_DIR, file_name)

logging.basicConfig(
    filename=log_file_path,
    filemode="w",
    level=logging.INFO,
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    force=True
)