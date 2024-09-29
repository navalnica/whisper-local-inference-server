import logging

from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s (%(filename)s): %(message)s",
)
logger = logging.getLogger("whisper")


class WhisperConfig(BaseModel):
    hf_model_name: str
    language: str
    chunk_length_s: int
    stride_length_s: int


class FilesConfig(BaseModel):
    dir_path: str
    delete_after_transcription: bool = True


# NOTE: update configs below with your settings

WHISPER_CONFIG = WhisperConfig(
    hf_model_name="ales/whisper-small-belarusian",
    language="be",
    chunk_length_s=8,
    stride_length_s=1,
)

FILES_CONFIG = FilesConfig(
    dir_path="data/uploads",
    delete_after_transcription=True,
    # delete_after_transcription=False,  # for debug only
)
