import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

OUTPUT_DIRS = {
    "videos": "videos",
    "audio": "audio",
    "transcriptions": "transcriptions"
}
