# src/youtube_transcriber/core/transcriber.py
import os
from typing import Optional
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from youtube_transcriber.config.settings import GOOGLE_CLOUD_PROJECT, OUTPUT_DIRS
from youtube_transcriber.utils.gcs_utils import GCSHandler
import pdb
class Transcriber:
    def __init__(self):
        self.client = SpeechClient()
        self.gcs_handler = GCSHandler()

    def transcribe_audio(self, audio_path: str, language: str = "ar-SA") -> Optional[str]:
        """
        Transcribes audio using Google Cloud Speech-to-Text batch recognition.
        """
        try:
            # Upload audio to GCS
            gcs_uri = self.gcs_handler.upload_file(audio_path)
            if not gcs_uri:
                return None

            # Prepare recognition config
            config = cloud_speech.RecognitionConfig(
                auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
                language_codes=[language],
                model="latest_long",
            )

            file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)

            # Prepare batch recognition request
            request = cloud_speech.BatchRecognizeRequest(
                recognizer=f"projects/{GOOGLE_CLOUD_PROJECT}/locations/global/recognizers/_",
                config=config,
                files=[file_metadata],
                recognition_output_config=cloud_speech.RecognitionOutputConfig(
                    inline_response_config=cloud_speech.InlineOutputConfig(),
                ),
                processing_strategy=cloud_speech.BatchRecognizeRequest.ProcessingStrategy.DYNAMIC_BATCHING,
            )

            # Perform transcription
            print("Starting batch transcription...")
            operation = self.client.batch_recognize(request=request)
            print("Waiting for operation to complete...")
            response = operation.result()  # No timeout as files might be long

            # Process results
            results = response.results[gcs_uri].transcript.results
            transcription = "\n".join(
                result.alternatives[0].transcript.strip()
                for result in results
                if hasattr(result, 'alternatives') and result.alternatives
            )
            # Cleanup GCS
            self.gcs_handler.delete_file(gcs_uri)

            return transcription

        except Exception as e:
            print(f"Transcription error: {e}")
            if gcs_uri:
                self.gcs_handler.delete_file(gcs_uri)
            return None

    def save_transcription(self, text: str, original_filename: str) -> None:
        """Saves transcription to a text file."""
        base_name = os.path.splitext(os.path.basename(original_filename))[0]
        output_path = os.path.join(
            OUTPUT_DIRS["transcriptions"],
            f"{base_name}_transcription.txt"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Transcription saved to: {output_path}")
