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

# ============================================================
# REPLACE THIS LINK with your Google Drive video sharing URL
# ============================================================
GDRIVE_LINK = "https://drive.google.com/file/d/1qM29M4g7IqRj-ZBxWlknTDH12o1UTLd-/view?usp=sharing"

MODEL = "base"            # Whisper model: tiny, base, small, medium, large
TIMESTAMPS = False         # Set to True to include timestamps


def extract_file_id(url):
    """Extract the Google Drive file ID from various URL formats."""
    patterns = [
        r'/file/d/([a-zA-Z0-9_-]+)',
        r'[?&]id=([a-zA-Z0-9_-]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    if re.match(r'^[a-zA-Z0-9_-]+$', url):
        return url
    return None


def main():
    file_id = extract_file_id(GDRIVE_LINK)
    if not file_id:
        print("Error: Could not extract file ID from the provided URL.", file=sys.stderr)
        sys.exit(1)

    tmp_dir = tempfile.mkdtemp()
    downloaded_path = None

    try:
        # Download
        url = f"https://drive.google.com/uc?id={file_id}"
        output_path = os.path.join(tmp_dir, "gdrive_video")
        print(f"Downloading from Google Drive (file ID: {file_id})...", file=sys.stderr)
        downloaded_path = gdown.download(url, output_path, quiet=False, fuzzy=True)
        if downloaded_path is None:
            raise RuntimeError("Failed to download. Check that the link is public.")

        # Transcribe
        print(f"Loading Whisper '{MODEL}' model...", file=sys.stderr)
        model = whisper.load_model(MODEL)
        print(f"Transcribing...", file=sys.stderr)
        result = model.transcribe(downloaded_path, language="en")

        # Format output
        if TIMESTAMPS:
            for seg in result['segments']:
                m, s = int(seg['start'] // 60), int(seg['start'] % 60)
                print(f"[{m}:{s:02d}] {seg['text'].strip()}")
        else:
            print(result['text'].strip())

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if downloaded_path and os.path.exists(downloaded_path):
            os.remove(downloaded_path)
            print("Cleaned up temporary file.", file=sys.stderr)
        if os.path.exists(tmp_dir):
            os.rmdir(tmp_dir)


if __name__ == "__main__":
    main()
