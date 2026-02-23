#!/usr/bin/env python3
"""
Local Video Transcript Extractor

Extracts transcripts from local video/audio files using OpenAI's Whisper model.
"""

import sys
import os
import whisper

# ============================================================
# REPLACE THIS PATH with your local video/audio file
# ============================================================
VIDEO_PATH = "/Users/madan12/Desktop/vibe-coding/video-transcript-generator/DUNE_Profiling.mp4"

MODEL = "base"            # Whisper model: tiny, base, small, medium, large
TIMESTAMPS = False         # Set to True to include timestamps


def main():
    if not os.path.isfile(VIDEO_PATH):
        print(f"Error: File not found: {VIDEO_PATH}", file=sys.stderr)
        sys.exit(1)

    # Transcribe
    print(f"Loading Whisper '{MODEL}' model...", file=sys.stderr)
    model = whisper.load_model(MODEL)
    print(f"Transcribing: {VIDEO_PATH}", file=sys.stderr)
    result = model.transcribe(VIDEO_PATH, language="en")

    # Format output
    if TIMESTAMPS:
        for seg in result['segments']:
            m, s = int(seg['start'] // 60), int(seg['start'] % 60)
            print(f"[{m}:{s:02d}] {seg['text'].strip()}")
    else:
        print(result['text'].strip())


if __name__ == "__main__":
    main()
