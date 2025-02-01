# src/youtube_transcriber/utils/audio_utils.py
import os
import ffmpeg
from typing import List
from youtube_transcriber.config.settings import OUTPUT_DIRS

def get_audio_duration(file_path: str) -> float:
    """Get duration of audio file in seconds using ffmpeg-python."""
    try:
        probe = ffmpeg.probe(file_path)
        return float(probe['format']['duration'])
    except ffmpeg.Error as e:
        print(f"Error getting duration: {e.stderr.decode()}")
        raise

def convert_video_to_audio(video_path: str, output_path: str) -> bool:
    """Convert video to audio using ffmpeg-python."""
    try:
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.output(
            stream,
            output_path,
            acodec='libmp3lame',  # MP3 codec
            ab='192k',            # Bitrate
            ac=2,                 # Stereo
            loglevel='error'      # Reduce ffmpeg output
        )
        ffmpeg.run(stream, overwrite_output=True)
        return True
    except ffmpeg.Error as e:
        print(f"Error converting video to audio: {e.stderr.decode()}")
        return False

def split_audio(file_path: str, chunk_duration: int) -> List[str]:
    """Split audio file into chunks of specified duration using ffmpeg-python."""
    try:
        duration = get_audio_duration(file_path)
        if duration <= chunk_duration:
            return [file_path]

        chunks = []
        base_path = os.path.splitext(file_path)[0]

        for i in range(0, int(duration), chunk_duration):
            output_path = f"{base_path}_chunk_{i}.mp3"

            stream = ffmpeg.input(file_path, ss=i, t=chunk_duration)
            stream = ffmpeg.output(
                stream,
                output_path,
                acodec='copy',    # Copy audio without re-encoding
                loglevel='error'
            )
            ffmpeg.run(stream, overwrite_output=True)
            chunks.append(output_path)

        return chunks
    except ffmpeg.Error as e:
        print(f"Error splitting audio: {e.stderr.decode()}")
        raise

def ensure_directories():
    """Ensure all required directories exist."""
    for directory in OUTPUT_DIRS.values():
        os.makedirs(directory, exist_ok=True)
