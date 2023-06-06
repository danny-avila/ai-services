# services\ai_services.py
import json
import openai
from typing import Dict
from logger import logger
from aiohttp import ClientSession
from .utils.handle_exception import handle_exception
from clients.tree_of_thoughts import AsyncOpenAILanguageModel, AsyncMonteCarloTreeofThoughts

openai.aiosession.set(ClientSession())
def logger_stream_handler(message):
    logger.debug(message)

async def ask_question(input_text: str, envs: Dict[str, str]) -> str:
    try:
        openai.api_key = envs["OPENAI_API_KEY"]
        messages = [{"role": "user", "content": f"Answer the following question as best you can: {input_text}" }]
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        logger.debug("ask_question: %s", response)
        return response.choices[0].message.content.strip()
    except Exception as e:
        handle_exception(e, "ask_question")

async def tree_of_thoughts(input_text: str, envs: Dict[str, str]) -> str:
    try:
        logger_stream_handler("Starting tree_of_thoughts service")
        api_model = envs["MODEL"]
        api_key = envs["OPENAI_API_KEY"]
        model = AsyncOpenAILanguageModel(api_key=api_key, api_model=api_model, stream_handler=logger_stream_handler)
        tree_of_thoughts = AsyncMonteCarloTreeofThoughts(model, stream_handler=logger_stream_handler)
        # model = OpenAILanguageModel(api_key=api_key, api_model=api_model)
        # tree_of_thoughts = MonteCarloTreeofThoughts(model)
        # initial_prompt =  """
        # Input: 2 8 8 14
        # Possible next steps:
        # 2 + 8 = 10 (left: 8 10 14)
        # 8 / 2 = 4 (left: 4 8 14)
        # 14 + 2 = 16 (left: 8 8 16)
        # 2 * 8 = 16 (left: 8 14 16)
        # 8 - 2 = 6 (left: 6 8 14)
        # 14 - 8 = 6 (left: 2 6 8)
        # 14 /  2 = 7 (left: 7 8 8)
        # 14 - 2 = 12 (left: 8 8 12)
        # Input: use 4 numbers and basic arithmetic operations (+-*/) to obtain 24 in 1 equation
        # Possible next steps:
        # """
        initial_prompt =  "design a new transportation system for an all-new city"
        num_thoughts = 1
        max_steps = 3
        max_states = 4
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

async def sentiment_analysis(text: str, api_key: str) -> str:
    try:
        openai.api_key = api_key
        response = await openai.Completion.acreate(
            engine="davinci-codex",
            prompt=f"Analyze the sentiment of the following text: {text}",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        logger.debug("sentiment_analysis: %s", response)
        sentiment = response.choices[0].text.strip()
        sentiment_dict = {"positive": float(sentiment.split()[0]), "negative": float(sentiment.split()[1])}
        return json.dumps(sentiment_dict)
    except Exception as e:
        handle_exception(e, "sentiment_analysis")

AI_SERVICES = {
    "q&a": ask_question,
    "tree_of_thoughts": tree_of_thoughts,
    "sentiment_analysis": sentiment_analysis,
}