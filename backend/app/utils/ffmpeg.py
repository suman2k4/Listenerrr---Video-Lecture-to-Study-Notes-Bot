import subprocess
from pathlib import Path
from typing import List


class FFmpegError(RuntimeError):
    pass


def run_ffmpeg(args: List[str]) -> None:
    command = ["ffmpeg", "-y"] + args
    process = subprocess.run(command, capture_output=True, text=True)
    if process.returncode != 0:
        raise FFmpegError(process.stderr)


def extract_audio(video_path: str, audio_path: str) -> str:
    Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
    run_ffmpeg(["-i", video_path, "-vn", "-acodec", "mp3", audio_path])
    return audio_path
