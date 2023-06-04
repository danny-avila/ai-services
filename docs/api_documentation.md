# AI Utility API Documentation

This API provides a RESTful interface to various AI utility libraries and securely manages user credentials for accessing these services.

## Endpoints

### POST /ask

This endpoint accepts a question and returns an answer using the specified AI service.

**URL**: `/ask`

**Method**: `POST`

**Content-Type**: `application/json`

**Request Payload**:

```json
{
  "service": "q&a",
  "input": "How many people live in Canada as of 2023?",
  "envs": {
    "OPENAI_API_KEY": "your_openai_api_key"
  }
}
```

**Success Response**:

- **Code**: `200 OK`
- **Content**:

```json
{
  "result": "Arrr, there be 38,645,670 people livin' in Canada as of 2023!",
  "error": "",
  "stdout": "Answer the following questions as best you can, but speaking as a pirate might speak...Final Answer: Arrr, there be 38,645,670 people livin' in Canada as of 2023!"
}
```

**Error Response**:

- **Code**: `400 Bad Request`
- **Content**:

```json
{
  "detail": "Invalid request payload."
}
```

### POST /sentiment_analysis

This endpoint accepts text data and returns the sentiment score using the specified AI service.

**URL**: `/sentiment_analysis`

**Method**: `POST`

**Content-Type**: `application/json`

**Request Payload**:

```json
{
  "service": "sentiment_analysis",
  "input": "I love this product!",
  "envs": {
    "OPENAI_API_KEY": "your_openai_api_key"
  }
}
```

**Success Response**:

- **Code**: `200 OK`
- **Content**:

```json
{
  "result": "positive",
  "error": "",
  "stdout": "The sentiment analysis result is: positive"
}
```

**Error Response**:

- **Code**: `400 Bad Request`
- **Content**:

```json
{
  "detail": "Invalid request payload."
}
```

## Authentication

This API uses a secret-based token for authentication. Include the token in the `Authorization` header of your requests.

**Example**:

```
Authorization: Bearer your_secret_token
```

## Errors

In case of errors, the API will return an appropriate HTTP status code along with a JSON object containing the error message.

**Example**:

```json
{
  "detail": "Invalid request payload."
}
```