#!/usr/bin/env python3
"""
Local Video Transcript Extractor

Extracts transcripts from local video/audio files using OpenAI's Whisper model.
"""

import sys
import os
import whisper


def transcribe_video(file_path, model_name='base', language='en'):
    """
    Transcribe a local video or audio file using Whisper.

    Args:
        file_path: Path to the video/audio file
        model_name: Whisper model size (tiny, base, small, medium, large)
        language: Language code (default: 'en')

    Returns:
        Transcription result dict with 'text' and 'segments'
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

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
        print("Usage: python get_local_video_transcript.py <video_path> [--timestamps] [--model MODEL]")
        print("\nModels: tiny, base (default), small, medium, large")
        print("\nExamples:")
        print("  uv run get_local_video_transcript.py DUNE_Profiling.mp4")
        print("  uv run get_local_video_transcript.py DUNE_Profiling.mp4 --timestamps")
        print("  uv run get_local_video_transcript.py DUNE_Profiling.mp4 --model small")
        sys.exit(1)

    file_path = sys.argv[1]
    include_timestamps = '--timestamps' in sys.argv

    # Parse model name
    model_name = 'base'
    if '--model' in sys.argv:
        model_idx = sys.argv.index('--model')
        if model_idx + 1 < len(sys.argv):
            model_name = sys.argv[model_idx + 1]

    try:
        result = transcribe_video(file_path, model_name=model_name)
        formatted_text = format_transcript(result, include_timestamps)
        print(formatted_text)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
