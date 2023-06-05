# services\ai_services.py
from typing import Dict
import json
import openai

def ask_question(input_text: str, envs: Dict[str, str]) -> str:
    try:
        openai.api_key = envs["OPENAI_API_KEY"]
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Answer the following question as best you can: {question}",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        print("ask_question", response)
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)


def sentiment_analysis(text: str, api_key: str) -> str:
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Analyze the sentiment of the following text: {text}",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        print("sentiment_analysis", response)
        sentiment = response.choices[0].text.strip()
        sentiment_dict = {"positive": float(sentiment.split()[0]), "negative": float(sentiment.split()[1])}
        return json.dumps(sentiment_dict)
    except Exception as e:
        return str(e)

def execute_ai_service(service: str, input_data: str, envs: Dict[str, str]) -> Dict[str, str]:
    if service == "q&a":
        return {"result": ask_question(input_data, envs["OPENAI_API_KEY"])}
    elif service == "sentiment_analysis":
        return {"result": sentiment_analysis(input_data, envs["OPENAI_API_KEY"])}
    else:
        return {"error": "Invalid service specified"}

AI_SERVICES = {
    "q&a": ask_question,
    "sentiment_analysis": sentiment_analysis
}