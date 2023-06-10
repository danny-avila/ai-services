# services\tree_of_thoughts_service.py
from typing import Dict
from logger import logger
from .utils import handle_exception, logger_stream_handler
from clients.tree_of_thoughts import AsyncOpenAILanguageModel, AsyncMonteCarloTreeofThoughts

def logger_stream_handler(message):
    logger.debug(message)

async def tree_of_thoughts(input_text: str, envs: Dict[str, str]) -> str:
    try:
        logger_stream_handler("Starting tree_of_thoughts service")
        api_model = envs["MODEL"]
        api_key = envs["OPENAI_API_KEY"]
        model = AsyncOpenAILanguageModel(api_key=api_key, api_model=api_model, stream_handler=logger_stream_handler)
        tree_of_thoughts = AsyncMonteCarloTreeofThoughts(model, stream_handler=logger_stream_handler)
        initial_prompt =  "design a new transportation system for an all-new city"
        num_thoughts = 1
        max_steps = 3
        max_states = 5
        pruning_threshold = 0.5

        solution = await tree_of_thoughts.solve(
        initial_prompt=initial_prompt,
        num_thoughts=num_thoughts, 
        max_steps=max_steps,
        max_states=max_states, 
        pruning_threshold=pruning_threshold,
        # sleep_time=sleep_time
        )

        # logger.debug("tree_of_thoughts: %s", solution)
        return f"Solution: {solution}"
    except Exception as e:
        handle_exception(e, "tree_of_thoughts")
