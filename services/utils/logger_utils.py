# utils\logger_utils.py
from logger import logger

def logger_stream_handler(message: str) -> None:
    logger.debug(message)