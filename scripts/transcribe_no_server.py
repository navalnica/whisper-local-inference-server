"""
transcribe single audio file without using a web-server:
- launch Whisper model
- transcribe file in the same process
- Whisper model is instantiated on each script run

NOTE: Must be launched from the repository root.
"""

# update sys path to import from src
import sys

sys.path.append(".")

import argparse

from src.config import WHISPER_CONFIG, logger
from src.whisper import WhisperModel


def main(audio_fp: str):
    # model is instantiated on each script run
    model = WhisperModel(whisper_config=WHISPER_CONFIG)

    try:
        transcription = model.transcribe(audio_fp)
        logger.info(f'transcription: "{transcription}"')
    except Exception as e:
        logger.exception(f"Exception occured while transcribing")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe Belarusian audio recording using Whisper model"
    )
    parser.add_argument("-f", "--file", type=str, help="Path to the audio file")
    args = parser.parse_args()

    main(audio_fp=args.file)
