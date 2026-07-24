
from __future__ import annotations

import asyncio
import logging
import os
import tempfile
import wave

import edge_tts
import numpy as np
import pygame
import sounddevice as sd

from faster_whisper import WhisperModel


logger = logging.getLogger(__name__)


class VoiceService:

    def __init__(
        self,
        model_size: str = "small",
        sample_rate: int = 16000,
    ):

        self.sample_rate = sample_rate
        self.channels = 1

        self.is_recording = False
        self.stream = None
        self.audio_frames = []

        logger.info("=" * 60)
        logger.info("Initializing Voice Service")
        logger.info("=" * 60)

        self.model = self._load_whisper(model_size)

        try:
            pygame.mixer.init()
            logger.info("Pygame mixer initialized.")

        except Exception as e:
            logger.warning(f"Pygame initialization failed : {e}")

    # ----------------------------------------------------
    # Whisper Loader
    # ----------------------------------------------------

    def _load_whisper(
        self,
        model_size: str,
    ):

        try:

            logger.info("Trying CUDA...")

            model = WhisperModel(
                model_size,
                device="cuda",
                compute_type="float16",
            )

            logger.info("CUDA Whisper Loaded")

            return model

        except Exception as gpu_error:

            logger.warning(
                f"CUDA unavailable : {gpu_error}"
            )

            logger.info("Switching to CPU...")

            try:

                model = WhisperModel(
                    model_size,
                    device="cpu",
                    compute_type="int8",
                )

                logger.info("CPU Whisper Loaded")

                return model

            except Exception as cpu_error:

                logger.error(cpu_error)

                raise RuntimeError(
                    "Unable to load Faster-Whisper."
                )

    # ----------------------------------------------------
    # Recording Callback
    # ----------------------------------------------------

    def _callback(
        self,
        indata,
        frames,
        time,
        status,
    ):

        if status:
            logger.warning(status)

        if self.is_recording:
            self.audio_frames.append(indata.copy())

    # ----------------------------------------------------
    # Start Recording
    # ----------------------------------------------------

    def start_recording(self):

        if self.is_recording:
            return

        self.audio_frames = []

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._callback,
        )

        self.stream.start()

        self.is_recording = True

        logger.info("Recording Started.")

    # ----------------------------------------------------
    # Stop Recording
    # ----------------------------------------------------

    def stop_recording(self):

        if not self.is_recording:
            return None

        self.is_recording = False

        if self.stream:

            self.stream.stop()
            self.stream.close()

        if len(self.audio_frames) == 0:
            return None

        audio = np.concatenate(
            self.audio_frames,
            axis=0,
        )

        temp = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        )

        filename = temp.name

        temp.close()

        with wave.open(filename, "wb") as wf:

            wf.setnchannels(self.channels)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)

            audio_int16 = (
                audio * 32767
            ).astype(np.int16)

            wf.writeframes(
                audio_int16.tobytes()
            )

        logger.info("Recording Saved.")

        return filename

# ----------------------------------------------------
    # Speech To Text
    # ----------------------------------------------------

    def speech_to_text(
        self,
        audio_path: str,
    ) -> str:

        if audio_path is None:
            return ""

        if not os.path.exists(audio_path):
            return ""

        try:

            logger.info("Starting transcription...")

            try:
                # Try with the loaded model (GPU if available)
                segments, info = self.model.transcribe(
                    audio_path,
                    beam_size=5,
                    language="en",
                    vad_filter=True,
                )

            except Exception as gpu_error:

                logger.warning(
                    f"GPU transcription failed: {gpu_error}"
                )

                logger.info(
                    "Retrying transcription on CPU..."
                )

                cpu_model = WhisperModel(
                    "small",
                    device="cpu",
                    compute_type="int8",
                )

                segments, info = cpu_model.transcribe(
                    audio_path,
                    beam_size=5,
                    language="en",
                    vad_filter=True,
                )

            text = ""

            for segment in segments:

                text += segment.text.strip() + " "

            text = text.strip()

            logger.info(
                "Transcription completed."
            )

            return text

        except Exception as e:

            logger.exception(e)

            return ""

        finally:

            try:

                if os.path.exists(audio_path):
                    os.remove(audio_path)

            except Exception:
                pass

    # ----------------------------------------------------
    # Edge TTS
    # ----------------------------------------------------

    async def _generate_audio(
        self,
        text: str,
        output_file: str,
    ):

        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-AriaNeural",
        )

        await communicate.save(output_file)

    # ----------------------------------------------------
    # Text To Speech
    # ----------------------------------------------------

    def text_to_speech(
        self,
        text: str,
    ):

        if not text.strip():
            return

        temp = tempfile.NamedTemporaryFile(
            suffix=".mp3",
            delete=False,
        )

        filename = temp.name

        temp.close()

        try:

            asyncio.run(
                self._generate_audio(
                    text,
                    filename,
                )
            )

            pygame.mixer.music.load(filename)

            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():

                pygame.time.Clock().tick(10)

        except Exception as e:

            logger.exception(e)

        finally:

            try:

                pygame.mixer.music.unload()

            except Exception:
                pass

            try:

                if os.path.exists(filename):
                    os.remove(filename)

            except Exception:
                pass

    # ----------------------------------------------------
    # Record + Transcribe
    # ----------------------------------------------------

    def record_and_transcribe(self):

        print()

        print("Recording...")

        print("Press ENTER to stop.")

        print()

        self.start_recording()

        input()

        audio = self.stop_recording()

        if audio is None:
            return ""

        return self.speech_to_text(audio)

    # ----------------------------------------------------
    # Health Check
    # ----------------------------------------------------

    def health_check(self):

        return {
            "recording": self.is_recording,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "whisper_loaded": self.model is not None,
        }