FROM python:3.12-slim

# set working dir
WORKDIR /app

# install ffmpeg and then clean apt cache and tmp files to reduce docker image size
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/

# expose fastapi port
EXPOSE 8000

# run fastapi server via uvicorn
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]
