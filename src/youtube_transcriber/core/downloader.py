# src/youtube_transcriber/core/downloader.py
from typing import Optional
import os
from pytubefix import YouTube
from youtube_transcriber.config.settings import OUTPUT_DIRS
from youtube_transcriber.utils.audio_utils import ensure_directories, convert_video_to_audio
import logging as log
import subprocess
import json
from typing import Tuple

def download_and_convert(url: str) -> Optional[str]:
    """Downloads YouTube video and converts to audio using ffmpeg-python."""
    try:
        ensure_directories()

        # Download video
        yt = YouTube(url, use_po_token=True, po_token_verifier=po_token_verifier)
        video = yt.streams.get_highest_resolution()
        video_path = video.download(output_path=OUTPUT_DIRS["videos"])

        # Prepare audio path
        audio_filename = os.path.splitext(os.path.basename(video_path))[0] + ".mp3"
        final_audio_path = os.path.join(OUTPUT_DIRS["audio"], audio_filename)

        # Convert to audio using ffmpeg-python
        if convert_video_to_audio(video_path, final_audio_path):
            # Clean up video file
            os.remove(video_path)
            return final_audio_path
        else:
            print("Audio conversion failed")
            return None

    except Exception as e:
        print(f"Error in download/conversion: {e}")
        return None

def cmd(command, check=True, shell=True, capture_output=True, text=True):
    """
    Runs a command in a shell, and throws an exception if the return code is non-zero.
    :param command: any shell command.
    :return:
    """
    log.info(f" + {command}")
    try:
        return subprocess.run(command, check=check, shell=shell, capture_output=capture_output, text=text)
    except subprocess.CalledProcessError as error:
        raise CommandFailedError(
            msg=f"\"{command}\" return exit code: {error.returncode}",
            stdout=error.stdout,
            stderr=error.stderr
        )

def po_token_verifier() -> Tuple[str, str]:
    token_object = generate_youtube_token()
    return token_object["visitorData"], token_object["poToken"]


def generate_youtube_token() -> dict:
    log.info("Generating YouTube token")
    result = cmd("node scripts/youtube-token-generator.js")
    data = json.loads(result.stdout)
    log.info(f"Result: {data}")
    return data

class CommandFailedError(Exception):
    def __init__(self, msg: str, stdout: str = None, stderr: str = None):
        self.msg = msg
        self.stdout = stdout
        self.stderr = stderr
        super().__init__(self.msg)
