the app is: Develop a RESTful API in Python using FastAPI. This API will interface with various AI utility libraries and securely manage user credentials for accessing these services.

the files we have decided to generate are: requirements.txt, main.py, Dockerfile, docker-compose.yaml, and files inside the routes directory.

Shared dependencies:

1. Exported variables:
   - app (FastAPI instance)

2. Data schemas:
   - RequestPayload (service, input, envs)
   - ApiResponse (result, error, stdout)

3. Id names of DOM elements: None (not applicable for this API)

4. Message names:
   - success_message
   - error_message

5. Function names:
   - ask
   - sentiment_analysis
   - authenticate
   - other AI utility functions based on the libraries used