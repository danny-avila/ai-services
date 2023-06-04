import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_authentication_success():
    response = client.post(
        "/ask",
        json={
            "service": "q&a",
            "input": "How many people live in canada as of 2023?",
            "envs": {
                "OPENAI_API_KEY": "valid_api_key",
            }
        }
    )
    assert response.status_code == 200
    assert "result" in response.json()
    assert "error" in response.json()
    assert "stdout" in response.json()

def test_authentication_failure():
    response = client.post(
        "/ask",
        json={
            "service": "q&a",
            "input": "How many people live in canada as of 2023?",
            "envs": {
                "OPENAI_API_KEY": "invalid_api_key",
            }
        }
    )
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid API key"