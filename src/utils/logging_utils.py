import logging
import os
from datetime import datetime
import threading

def setup_logger(name, log_file, level=logging.INFO):
       formatter = logging.Formatter('%(asctime)s %(levelname)s [Thread-%(thread)d] %(message)s')
       
       handler = logging.FileHandler(log_file)        
       handler.setFormatter(formatter)

       logger = logging.getLogger(name)
       logger.setLevel(level)
       logger.addHandler(handler)

       return logger

# Create a logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Setup the main logger
main_logger = setup_logger('main_logger', f'logs/graph_db_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

def log_operation(operation, *args):
    """Log an operation with its arguments"""
    main_logger.info(f"Operation: {operation}, Args: {args}")

def log_result(operation, result):
    """Log the result of an operation"""
    main_logger.info(f"Operation: {operation}, Result: {result}")

def log_error(operation, error):
    """Log an error that occurred during an operation"""
    main_logger.error(f"Operation: {operation}, Error: {error}")