import pytest
from fastapi.testclient import TestClient
from main import app
from services.ai_services import AI_SERVICES

client = TestClient(app)

def test_ask():
    test_data = {
        "service": "q&a",
        "input": "How many people live in canada as of 2023?",
        "envs": {
            "OPENAI_API_KEY": "test_key",
        }
    }
    response = client.post("/ask", json=test_data)
    assert response.status_code == 200
    assert "result" in response.json()
    assert "error" in response.json()
    assert "stdout" in response.json()

def test_ask_invalid_service():
    test_data = {
        "service": "invalid_service",
        "input": "How many people live in canada as of 2023?",
        "envs": {
            "OPENAI_API_KEY": "test_key",
        }
    }
    response = client.post("/ask", json=test_data)
    assert response.status_code == 400
    assert "detail" in response.json()

def test_sentiment_analysis():
    test_data = {
        "text": "I love this product!",
        "envs": {
            "OPENAI_API_KEY": "test_key",
        }
    }
    response = client.post("/sentiment_analysis", json=test_data)
    assert response.status_code == 200
    assert "result" in response.json()
    assert "error" in response.json()
    assert "stdout" in response.json()

def test_sentiment_analysis_invalid_input():
    test_data = {
        "text": "",
        "envs": {
            "OPENAI_API_KEY": "test_key",
        }
    }
    response = client.post("/sentiment_analysis", json=test_data)
    assert response.status_code == 422
    assert "detail" in response.json()

@pytest.mark.parametrize("service_name", AI_SERVICES.keys())
def test_ai_services(service_name):
    test_data = {
        "service": service_name,
        "input": "Test input",
        "envs": {
            "OPENAI_API_KEY": "test_key",
        }
    }
    response = client.post("/ask", json=test_data)
    assert response.status_code == 200
    assert "result" in response.json()
    assert "error" in response.json()
    assert "stdout" in response.json()