# AI Tutor Skill

A Claude Code skill that breaks down technical concepts — particularly in AI and ML — into clear, jargon-free explanations. It uses structured narrative frameworks to make dense ideas approachable, whether you are learning or teaching.

## Prerequisites

- **Python** 3.12 or newer
- **[uv](https://github.com/astral-sh/uv)** — Python package and project manager
- **FFmpeg** — required by Whisper for audio processing (not needed for YouTube-only usage)

### Install uv

```bash
# Mac
brew install uv

# Or on any platform
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install FFmpeg

```bash
# Mac
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows
winget install ffmpeg
```

> **Note:** If you only need YouTube transcripts, you can skip FFmpeg — that script fetches existing captions and doesn't use Whisper.

## Getting Started

```bash
git clone https://github.com/madantimalsina/video-transcript-generator.git
cd video-transcript-generator
uv sync
```

No need to manually create or activate a virtual environment. `uv sync` automatically creates a `.venv` in the project directory and installs all dependencies. When you run scripts with `uv run`, they execute inside that environment automatically.

## Transcript Tools

Three scripts pull transcripts from different video sources. Each script has configuration variables at the top — just replace the URL/path and run.

---

### `get_local_video_transcript.py`

Transcribes a local video or audio file using OpenAI's Whisper model.

**How it works:**
1. Reads the file path from `VIDEO_PATH` at the top of the script
2. Loads the Whisper model (size set by `MODEL`)
3. Runs the audio through Whisper to generate a transcript
4. Prints plain text, or timestamped lines if `TIMESTAMPS = True`

**Configuration:**
```python
VIDEO_PATH = "/path/to/your.mp4"
MODEL = "base"            # tiny, base, small, medium, large
TIMESTAMPS = False
```

**Run:**
```bash
uv run scripts/get_local_video_transcript.py
```

---

### `get_gdrive_video_transcript.py`

Downloads a video from a public Google Drive link and transcribes it with Whisper.

**How it works:**
1. Extracts the file ID from the Google Drive URL in `GDRIVE_LINK`
2. Downloads the video to a temporary directory using `gdown`
3. Loads the Whisper model and transcribes the downloaded file
4. Prints the transcript (plain text or with timestamps)
5. Cleans up the temporary file automatically

**Configuration:**
```python
GDRIVE_LINK = "https://drive.google.com/file/d/FILE_ID/view?usp=sharing"
MODEL = "base"            # tiny, base, small, medium, large
TIMESTAMPS = False
```

**Run:**
```bash
uv run scripts/get_gdrive_video_transcript.py
```

> The Google Drive link must be publicly shared for the download to work.

---

### `get_youtube_transcript.py`

Retrieves existing captions from YouTube using the YouTube Transcript API (no Whisper needed).

**How it works:**
1. Extracts the video ID from the YouTube URL in `YOUTUBE_URL`
2. Fetches the available English captions via the YouTube Transcript API
3. Prints the transcript (plain text or with timestamps)

**Configuration:**
```python
YOUTUBE_URL = "https://www.youtube.com/watch?v=RN5OMMfNjys"
TIMESTAMPS = False
```

**Run:**
```bash
uv run scripts/get_youtube_transcript.py
```

---

### Whisper Model Sizes

The local and Google Drive scripts use Whisper for transcription. Available models:

| Model | Speed | Accuracy |
|-------|-------|----------|
| `tiny` | Fastest | Lowest |
| `base` | Fast | Good (default) |
| `small` | Moderate | Better |
| `medium` | Slow | High |
| `large` | Slowest | Highest |

## Note on `uv.lock`

- **[uv](https://github.com/astral-sh/uv)** for dependency and script management

The `uv.lock` file pins every dependency (and their sub-dependencies) to exact versions. This guarantees that anyone cloning the repo gets an identical environment. The transcript scripts will still work without it — uv resolves dependencies on the fly — but keeping it checked in ensures reproducible builds across machines.

## License

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.
