# AI Tutor Skill

A Claude Code skill that breaks down technical concepts — particularly in AI and ML — into clear, jargon-free explanations. It uses structured narrative frameworks to make dense ideas approachable, whether you are learning or teaching.

Resources:
- [YouTube Explainer](https://www.youtube.com/watch?v=RN5OMMfNjys)

## Prerequisites

- **Python** 3.12 or newer
- **[uv](https://github.com/astral-sh/uv)** for dependency and script management
- All Python packages (openai-whisper, gdown, youtube-transcript-api) are installed automatically on first run

## Getting Started

Clone the repo and install dependencies:

```bash
git clone https://github.com/madantimalsina/video-transcript-generator.git
cd video-transcript-generator
uv sync
```

## Transcript Tools

Three helper scripts pull text from different video sources so the tutor skill can work with video content.

### Local Video / Audio

Runs a local file through OpenAI's Whisper model to generate a transcript on your machine.

```bash
uv run scripts/get_local_video_transcript.py recording.mp4
uv run scripts/get_local_video_transcript.py recording.mp4 --timestamps
uv run scripts/get_local_video_transcript.py recording.mp4 --model small
```

### Google Drive Video

Downloads a video from a public Google Drive sharing link, then transcribes it with Whisper. The temporary file is cleaned up automatically after transcription.

```bash
uv run scripts/get_gdrive_video_transcript.py "https://drive.google.com/file/d/FILE_ID/view?usp=sharing"
uv run scripts/get_gdrive_video_transcript.py "https://drive.google.com/file/d/FILE_ID/view?usp=sharing" --timestamps
uv run scripts/get_gdrive_video_transcript.py "https://drive.google.com/file/d/FILE_ID/view?usp=sharing" --model small
```

### YouTube

Retrieves existing captions from YouTube using the Transcript API.

```bash
uv run scripts/get_youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
uv run scripts/get_youtube_transcript.py "https://youtu.be/VIDEO_ID" --timestamps
```

> **Heads up:** YouTube blocks requests that originate from cloud servers. Run Claude Code on your local machine for this script to work.

### Whisper Model Sizes

The `--model` flag (used by the local and Google Drive scripts) accepts: `tiny`, `base` (default), `small`, `medium`, `large`. Bigger models produce more accurate transcripts but take longer to run.

## Note on `uv.lock`

The `uv.lock` file pins every dependency (and their sub-dependencies) to exact versions. This guarantees that anyone cloning the repo gets an identical environment. The transcript scripts will still work without it — uv resolves dependencies on the fly — but keeping it checked in ensures reproducible builds across machines.

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
