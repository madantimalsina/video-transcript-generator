#!/usr/bin/env python3
"""
YouTube Transcript Extractor

Extracts transcripts from YouTube videos using video IDs or URLs.
"""

import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# ============================================================
# REPLACE THIS URL with your YouTube video link
# Example: "https://www.youtube.com/watch?v=RN5OMMfNjys"
# ============================================================
YOUTUBE_URL = "https://www.youtube.com/watch?v=RN5OMMfNjys"

TIMESTAMPS = False         # Set to True to include timestamps


def extract_video_id(url_or_id):
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
        r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return None


def main():
    video_id = extract_video_id(YOUTUBE_URL)
    if not video_id:
        print(f"Error: Could not extract video ID from: {YOUTUBE_URL}", file=sys.stderr)
        sys.exit(1)

    try:
        # Get transcript
        print(f"Fetching transcript for video: {video_id}...", file=sys.stderr)
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=["en"])

        # Format output
        if TIMESTAMPS:
            for entry in transcript:
                m, s = int(entry.start // 60), int(entry.start % 60)
                print(f"[{m}:{s:02d}] {entry.text}")
        else:
            print(' '.join([entry.text for entry in transcript]))

    except TranscriptsDisabled:
        print(f"Error: Transcripts are disabled for video: {video_id}", file=sys.stderr)
        sys.exit(1)
    except NoTranscriptFound:
        print(f"Error: No transcript found for video: {video_id}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
