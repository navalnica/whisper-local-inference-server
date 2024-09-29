"""
fastapi server to transcribe uploaded audio files

NOTE: must be started from the root of repository
"""

import os
import shutil
import time
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from src.config import FILES_CONFIG, WHISPER_CONFIG, logger
from src.whisper import WhisperModel

logger.info(
    'initializing the web server. please wait for the explicit message '
    'that the server has started and is ready to accept requests'
)

# initialize app and resources
app = FastAPI()
# speech-to-text model
stt_model = WhisperModel(whisper_config=WHISPER_CONFIG)

# fastapi logging does not work for some reason.
# can't log incoming requests, even using custom middleware...


@app.middleware('http')
async def log_requests(request: Request, call_next):
    """Custom request logger"""
    logger.info(f"incoming request: {request.method} {request.url}")
    time_start = time.time()
    response = await call_next(request)
    duration = time.time() - time_start
    logger.info(
        f"request completed: [{response.status_code}] {request.method} {request.url}. "
        f"(duration: {duration:.2f}s)"
    )
    return response


@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
):
    try:
        orig_filename = file.filename

        # save the uploaded audio file to temp location
        _, ext = os.path.splitext(orig_filename)
        uuid = str(uuid4())
        audio_fn = f"{uuid}{ext}"
        audio_fp = os.path.join(FILES_CONFIG.dir_path, audio_fn)
        with open(audio_fp, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcription = stt_model.transcribe(audio_fp)

        if FILES_CONFIG.delete_after_transcription:
            # delete temp audio files after transcription
            os.remove(audio_fp)

        return JSONResponse(content={"transcription": transcription})

    except Exception as e:
        logger.exception(f"transcription failed")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing audio file: {str(e)}",
        )


logger.info(f'server started and is ready to accept requests')
