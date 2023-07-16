# services\nla_agent.py
from typing import Dict
from clients import get_nla_agent
from .utils import handle_exception, logger_stream_handler

async def nla_agent(input_text: str, envs: Dict[str, str]) -> str:
    try:
        # Check if the API key exists in the environment variables
        plugin_api_key = envs["PLUGIN_API_KEY"] if "PLUGIN_API_KEY" in envs else None

        nla_agent, _tools = get_nla_agent(
            openai_api_key=envs["OPENAI_API_KEY"], 
            model_name="gpt-3.5-turbo", 
            plugin_name=envs["plugin_name"], 
            plugin_api_key=plugin_api_key
        )
        response = nla_agent.run(input_text)
        logger_stream_handler(f"logger_stream_handler test: {response}")
        # logger.debug("nla_agent: %s", response)
        return response
    except Exception as e:
        handle_exception(e, "nla_agent")
        return ""

