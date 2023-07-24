# services\code_interpreter.py
import pprint
from typing import Dict
from codeinterpreterapi import CodeInterpreterSession
from .utils import handle_exception, logger_stream_handler

async def code_interpreter(input_text: str, envs: Dict[str, str]) -> str:
    try:
        # Check if the API key exists in the environment variables
        openai_api_key = envs["OPENAI_API_KEY"]

        session = CodeInterpreterSession(openai_api_key=openai_api_key)
        await session.astart()

        # generate a response based on user input
        response = await session.generate_response(input_text)

        # ouput the response (text + image)
        # print("AI: ", response.content)
        pprint.pprint(response)
        # for file in response.files:
        #     file.show_image()

        # terminate the session
        await session.astop()
        logger_stream_handler(f"logger_stream_handler test: {response}")
        # logger.debug("code_interpreter: %s", response)
        return response.content
    except Exception as e:
        handle_exception(e, "code_interpreter")
        return ""

