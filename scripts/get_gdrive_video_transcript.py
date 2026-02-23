#!/usr/bin/env python3
"""
Google Drive Video Transcript Extractor

Downloads a video from a Google Drive sharing link and transcribes it using Whisper.
"""

import sys
import os
import re
import tempfile
import gdown
import whisper


def extract_file_id(url):
    """
    Extract the Google Drive file ID from various URL formats.

    Supported formats:
        https://drive.google.com/file/d/FILE_ID/view?usp=sharing
        https://drive.google.com/open?id=FILE_ID
        https://drive.google.com/uc?id=FILE_ID
        Raw file ID string
    """
    patterns = [
        r'/file/d/([a-zA-Z0-9_-]+)',
        r'[?&]id=([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # If no pattern matched, assume the input is a raw file ID
    if re.match(r'^[a-zA-Z0-9_-]+$', url):
        return url

    return None


def download_from_gdrive(file_id, output_dir):
    """
    Download a file from Google Drive using gdown.

    Args:
        file_id: Google Drive file ID
        output_dir: Directory to save the downloaded file

    Returns:
        Path to the downloaded file
    """
    url = f"https://drive.google.com/uc?id={file_id}"
    output_path = os.path.join(output_dir, "gdrive_video")

    print(f"Downloading from Google Drive (file ID: {file_id})...", file=sys.stderr)
    result = gdown.download(url, output_path, quiet=False, fuzzy=True)

    if result is None:
        raise RuntimeError("Failed to download file from Google Drive. Check that the link is public.")

    return result


def transcribe_video(file_path, model_name='base', language='en'):
    """
    Transcribe a video or audio file using Whisper.

    Args:
        file_path: Path to the video/audio file
        model_name: Whisper model size (tiny, base, small, medium, large)
        language: Language code (default: 'en')

    Returns:
        Transcription result dict with 'text' and 'segments'
    """
    print(f"Loading Whisper '{model_name}' model...", file=sys.stderr)
    model = whisper.load_model(model_name)

    print(f"Transcribing: {file_path}", file=sys.stderr)
    result = model.transcribe(file_path, language=language)
    return result


def format_transcript(result, include_timestamps=False):
    """
    Format transcription result into readable text.

    Args:
        result: Whisper transcription result
        include_timestamps: Whether to include timestamps

    Returns:
        Formatted transcript text
    """
    if include_timestamps:
        formatted = []
        for segment in result['segments']:
            start = segment['start']
            minutes = int(start // 60)
            seconds = int(start % 60)
            formatted.append(f"[{minutes}:{seconds:02d}] {segment['text'].strip()}")
        return '\n'.join(formatted)
    else:
        return result['text'].strip()


def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        print("Usage: python get_gdrive_video_transcript.py <google_drive_url> [--timestamps] [--model MODEL]")
        print("\nModels: tiny, base (default), small, medium, large")
        print("\nExamples:")
        print("  uv run get_gdrive_video_transcript.py 'https://drive.google.com/file/d/FILE_ID/view?usp=sharing'")
        print("  uv run get_gdrive_video_transcript.py 'https://drive.google.com/file/d/FILE_ID/view?usp=sharing' --timestamps")
        print("  uv run get_gdrive_video_transcript.py 'https://drive.google.com/file/d/FILE_ID/view?usp=sharing' --model small")
        sys.exit(1)

    gdrive_url = sys.argv[1]
    include_timestamps = '--timestamps' in sys.argv

    # Parse model name
    model_name = 'base'
    if '--model' in sys.argv:
        model_idx = sys.argv.index('--model')
        if model_idx + 1 < len(sys.argv):
            model_name = sys.argv[model_idx + 1]

    # Extract file ID
    file_id = extract_file_id(gdrive_url)
    if not file_id:
        print("Error: Could not extract file ID from the provided URL.", file=sys.stderr)
        sys.exit(1)

    tmp_dir = tempfile.mkdtemp()
    downloaded_path = None

    try:
        downloaded_path = download_from_gdrive(file_id, tmp_dir)
        result = transcribe_video(downloaded_path, model_name=model_name)
        formatted_text = format_transcript(result, include_timestamps)
        print(formatted_text)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Clean up temp files
        if downloaded_path and os.path.exists(downloaded_path):
            os.remove(downloaded_path)
            print("Cleaned up temporary file.", file=sys.stderr)
        if os.path.exists(tmp_dir):
            os.rmdir(tmp_dir)


if __name__ == "__main__":
    main()
