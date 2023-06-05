# logger.py
import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Configure the logger
c_handler = logging.StreamHandler()
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

# Set level of logger
logger.setLevel(logging.INFO)
