# src/youtube_transcriber/utils/gcs_utils.py
from google.cloud import storage
import os
from typing import Optional
from youtube_transcriber.config.settings import GCS_BUCKET_NAME

class GCSHandler:
    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(GCS_BUCKET_NAME)

    def upload_file(self, local_file_path: str) -> Optional[str]:
        """
        Uploads a file to Google Cloud Storage.
        Returns the GCS URI if successful, None otherwise.
        """
        try:
            file_name = os.path.basename(local_file_path)
            blob = self.bucket.blob(file_name)
            blob.upload_from_filename(local_file_path)
            return f"gs://{GCS_BUCKET_NAME}/{file_name}"
        except Exception as e:
            print(f"Error uploading to GCS: {e}")
            return None

    def delete_file(self, gcs_uri: str) -> bool:
        """
        Deletes a file from Google Cloud Storage.
        Returns True if successful, False otherwise.
        """
        try:
            file_name = gcs_uri.split('/')[-1]
            blob = self.bucket.blob(file_name)
            blob.delete()
            return True
        except Exception as e:
            print(f"Error deleting from GCS: {e}")
            return False
