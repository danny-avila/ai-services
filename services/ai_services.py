from typing import Dict
import openai

def ask_question(question: str, api_key: str) -> str:
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Answer the following question as best you can: {question}",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

def sentiment_analysis(text: str, api_key: str) -> Dict[str, float]:
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Analyze the sentiment of the following text: {text}",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    sentiment = response.choices[0].text.strip()
    return {"positive": float(sentiment.split()[0]), "negative": float(sentiment.split()[1])}

def execute_ai_service(service: str, input_data: str, envs: Dict[str, str]) -> Dict[str, str]:
    if service == "q&a":
        return {"result": ask_question(input_data, envs["OPENAI_API_KEY"])}
    elif service == "sentiment_analysis":
        return {"result": sentiment_analysis(input_data, envs["OPENAI_API_KEY"])}
    else:
        return {"error": "Invalid service specified"}