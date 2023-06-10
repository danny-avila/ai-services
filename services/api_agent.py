# services\api_agent.py
from typing import Dict
from clients import get_openapi_agent
from .utils import handle_exception, logger_stream_handler

async def api_agent(input_text: str, envs: Dict[str, str]) -> str:
    try:
        api_agent = get_openapi_agent(api_key = envs["OPENAI_API_KEY"], model_name = "gpt-3.5-turbo", plugin_name = envs["plugin_name"])
        response = api_agent.run(input_text)
        logger_stream_handler(f"logger_stream_handler test: {response}")
        # logger.debug("api_agent: %s", response)
        return response
    except Exception as e:
        handle_exception(e, "api_agent")
