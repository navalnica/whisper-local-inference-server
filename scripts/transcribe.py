"""
transcribe audio file(s) using launched Whisper server.

NOTE: Must be launched from the repository root.
"""

# update sys path to import from src
import sys

sys.path.append(".")

import argparse
import asyncio
import os
import random
import time

import httpx

from src.config import logger

# server settings
SERVER_URL = "http://127.0.0.1:8000"
TRANSCRIPTION_URL = f"{SERVER_URL}/transcribe"


def get_delay_between_requests():
    """
    Delay between successive requests.
    Used to imitate real-world load when server may process multiple requests simultaneously
    """
    delay = random.uniform(0.5, 4)
    return delay


async def transcribe_file(audio_fp: str):
    logger.info(f'sending request to transcribe "{audio_fp}"')
    time_start = time.time()

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(120, connect=3)) as client:
            with open(audio_fp, "rb") as audio_file:
                response = await client.post(TRANSCRIPTION_URL, files={"file": audio_file})
        response.raise_for_status()
        resp_json = response.json()

        elapsed = time.time() - time_start
        logger.info(f'response for "{audio_fp}" received: {resp_json}. elapsed: {elapsed:.2f}s')
    except Exception as e:
        elapsed = time.time() - time_start
        logger.exception(f'failed to retrieve response for "{audio_fp}". elapsed: {elapsed:.2f}s')


async def transcribe_multiple_files(fps: list[str]):
    for fp in fps:
        if not os.path.isfile(fp):
            raise FileNotFoundError(fp)

    logger.info(f'will send requests to transcribe {len(fps)} files')

    tasks_set = set()
    for ix, fp in enumerate(fps, start=1):
        # schedule a task to run in background.
        # it will run as soon as possible, no need to call 'await'.
        task = asyncio.create_task(transcribe_file(audio_fp=fp))
        # add tasks to container to prevent them to be deleted by garbage collector
        tasks_set.add(task)
        # To prevent keeping references to finished tasks forever,
        # make each task remove its own reference from the set after completion.
        # reference: https://docs.python.org/3/library/asyncio-task.html#creating-tasks
        task.add_done_callback(tasks_set.discard)

        logger.info(f'scheduled a task for file #{ix}')

        if ix < len(fps):  # we start from 1
            # wait before sending next request
            delay = get_delay_between_requests()
            logger.info(f'will wait for {delay:.2f}s before sending the next request')
            await asyncio.sleep(delay)

    # wait for unfinished tasks
    await asyncio.gather(*tasks_set)

    logger.info(f'all {len(fps)} transcription tasks gathered')


async def main():
    parser = argparse.ArgumentParser(
        description=(
            "Send audio file(s) to web-server for transcription. "
            "You can pass multiple files - "
            "they will be sent in a sequence with random intervals between them. "
            "This is useful to understand real-world server response times "
            "under constant requests load."
        )
    )
    parser.add_argument(
        "-f",
        "--files",
        type=str,
        nargs='+',
        help=(
            "Paths to audio files. You can provide more than one file - "
            "all of them will be transcribed"
        ),
    )
    args = parser.parse_args()

    await transcribe_multiple_files(fps=args.files)


if __name__ == "__main__":
    asyncio.run(main())
