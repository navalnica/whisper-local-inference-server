import time

import torch
from transformers import pipeline

from src.config import WhisperConfig, logger


class WhisperModel:
    def __init__(self, whisper_config: WhisperConfig):
        """Initialize the model and prepare it for transcription"""

        logger.info(f"initializing whisper model with the following params: {whisper_config}")

        device = 0 if torch.cuda.is_available() else "cpu"
        logger.info(f"using following device: {device}")

        self.pipe = pipeline(
            task="automatic-speech-recognition",
            model=whisper_config.hf_model_name,
            chunk_length_s=whisper_config.chunk_length_s,
            stride_length_s=whisper_config.stride_length_s,
            device=device,
        )

        self.pipe.model.config.forced_decoder_ids = self.pipe.tokenizer.get_decoder_prompt_ids(
            language=whisper_config.language, task="transcribe"
        )

    def transcribe(self, filepath: str) -> str:
        """Transcribe an audiofile located under 'filepath'."""

        if not filepath:
            raise FileNotFoundError(f'could not find the file for transcription: "{filepath}"')

        # TODO: this model call is not asynchronous - need to make it async
        # TODO: check for data races and memory errors
        # TODO: check how differnt audio formats (extension, codec, bitrate) influence transcription
        # TODO: feed .wav file and compare len(input_bytes) with len(output_bytes)

        # TODO: notes from the log:
        # The attention mask is not set and cannot be inferred from input
        # because pad token is same as eos token.
        # As a consequence, you may observe unexpected behavior.
        # Please pass your input's `attention_mask` to obtain reliable results.

        logger.info(f'starting transcribing "{filepath}"')
        time_start = time.time()
        text = self.pipe(filepath)["text"]
        elapsed = time.time() - time_start
        logger.info(f'finished transcribing "{filepath}". elapsed: {elapsed:.2f}s')

        return text
