# services/utils/exception_handler.py
import traceback
from fastapi import HTTPException
from logger import logger

def handle_exception(e: Exception, service_name: str) -> None:
    logger.error("%s Exception: %s", service_name, e)
    logger.error("Exception type: %s", type(e).__name__)
    logger.error("Traceback: %s", traceback.format_exc())
    error_message = f"An error of type {type(e).__name__} occurred. Arguments:\n{e.args}"
    raise HTTPException(status_code=500, detail=error_message)