# server settings
HOST=127.0.0.1
PORT=8000
MODULE=src.server:app

# run the FastAPI server
run_server:
	uvicorn $(MODULE) --host $(HOST) --port $(PORT)

# install python dependencies in current environment
install:
	pip install -r requirements.txt

# format python files
format:
	black .
	isort .