# To create a virtual env
virtualenv venv --python=python3.8

# To run fastapi
uvicorn main:app --reload --port 8080
