## Device Registration API

Internal API responsible for registering user device types.

### Tech Env
- Python 3.11
- FastAPI
- Docker

### How to run locally
Make sure to have python installed locally :
- python3 -m venv .venv # Create virtual env
- source .venv/bin/activate # Enable virtual Env
- pip install -r device-registration-api/requirements.txt # install dependencies
- cd device-registration-api
- uvicorn app.main:app --reload # Run the api
INFO:     Will watch for changes in these directories: ['xxxx']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [40886] using WatchFiles
INFO:     Started server process [40888]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:63681 - "GET / HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:63681 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:63688 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:63688 - "GET /openapi.json HTTP/1.1" 200 OK

### How to run with docker
Make sure to have docker installed locally :
- cd device-registration-api
- docker build -t device-registration-api:1.0.0 . 
- docker run -p 8000:8000 -d device-registration-api:1.0.0

then open localhost:8000/docs to see the swagger
