# Whisper Local Asynchronous Inference Server

Simple implementation of asynchronous server to run Whisper speech-to-text model locally.
Implemented in FastAPI.

By default it's configured to serve **Belarusian Whisper model**: [ales/whisper-small-belarusian](https://huggingface.co/ales/whisper-small-belarusian)

## WARNING
- despite the server is asynchronous, the Whisper model itself
seems to sometimes process incoming requests in parallel, and sometimes - sequentially
- we need to understand how huggingface transformers' `automatic-speech-recognition` pipeline works
- and optimize it if possible to handle simultaneous requests more efficiently

## Server endpoints

- `/transcribe` - main transcription endpoint
- you can see Swagger UI docs using `/docs` endpoint
- docs in ReDoc format are available using `/redoc` endpoint

## Run server inside docker container

`docker compose up --build`

Docker will map host's `localhost:8000` to the Server.

## Run server on host machine, without docker

1. `make install`
2. `make run_server`

Server will listen on `127.0.0.1:8000`.

## How to send files for transcription

**TODO: clarify this section**

Simply use `/transcribe` endpoint. It expects `{'file': filepath}` body content. See the Swagger docs for details.

You can send requests:
1. Either using CURL, like<br>`curl -X POST http://127.0.0.1:8000/transcribe -F "audio=@/path/to/your/audiofile.wav"`
2. Or using python script:<br>
    - `python scripts/transcribe.py -f data/samples/audio1.mp3`
    - You can send multiple files:<br>
    `python scripts/transcribe.py -f data/samples/audio1.mp3 dadta/samples/audio2.mp3`
    - See the help message:
    `python scripts/transcribe.py -h`

## How to Configure

Simply update configs in `config.py`

## Load testing

Use `transcribe.py` script and pass multiple files:<br>
`python scripts/transcribe.py -f data/samples/*.mp3`

## Transcribe without Server

You can also instantiate Whisper model and run transcription in one go, without any server.

For that, use `python scripts/transcribe_no_server.py -f data/samples/audio1.mp3`