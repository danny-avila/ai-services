# services\api_chain.py
from typing import Dict
from clients import get_openapi_chain
from .utils import handle_exception, logger_stream_handler

async def api_chain(input_text: str, envs: Dict[str, str]) -> str:
    try:
        api_chain = get_openapi_chain(api_key = envs["OPENAI_API_KEY"], model_name = "gpt-3.5-turbo")
        response = api_chain(input_text)
        logger_stream_handler(f"logger_stream_handler test: {response}")
        # logger.debug("api_chain: %s", response)
        return response
    except Exception as e:
        handle_exception(e, "api_chain")
        return "" # return empty string if an exception is caught
