from youtube_transcriber.core.downloader import download_and_convert
from youtube_transcriber.core.transcriber import Transcriber

def main():
    url = input("Enter YouTube URL: ")

    print("Downloading and converting video...")
    audio_path = download_and_convert(url)
    if not audio_path:
        print("Failed to download/convert video")
        return

    print("Transcribing audio...")
    transcriber = Transcriber()
    transcription = transcriber.transcribe_audio(audio_path)
    if transcription:
        transcriber.save_transcription(transcription, audio_path)
        print("Transcription completed successfully!")
    else:
        print("Transcription failed")

if __name__ == "__main__":
    main()
