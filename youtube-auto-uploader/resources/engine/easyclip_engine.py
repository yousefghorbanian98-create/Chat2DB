"""EasyClip local processing engine.

This module combines and adapts two MIT-licensed projects:
- NaufalRizqullah/opensource-clipping: yt-dlp source selection and
  Faster-Whisper word-level transcription pipeline.
- toki-plus/ai-highlight-clip: sliding-window candidate generation and
  timestamp-aware subtitle layout.

It intentionally makes no network AI calls. Network access is used only when
`download` is explicitly asked to fetch a public video URL. Once input and a
Whisper model are present, analysis and rendering are local.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass
class Word:
    text: str
    start: float
    end: float


@dataclass
class Highlight:
    id: str
    start_seconds: float
    end_seconds: float
    score: int
    title: str
    transcript: str
    caption_path: str


def emit(event: str, **payload: object) -> None:
    print(json.dumps({"event": event, **payload}, ensure_ascii=False), file=sys.stderr, flush=True)


def output_result(**payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False), flush=True)


def build_format_selector(height: str) -> str:
    """Prefer broadly decodable H.264 sources (adapted from opensource-clipping)."""
    codec = "[vcodec!*=av01]"
    if height == "max":
        return f"bestvideo{codec}+bestaudio/best{codec}"
    try:
        limit = max(144, int(height))
    except ValueError:
        limit = 1080
    return (
        f"bestvideo[height<=?{limit}][ext=mp4]{codec}+bestaudio[ext=m4a]/"
        f"bestvideo[height<=?{limit}]{codec}+bestaudio/"
        f"best[height<=?{limit}]{codec}"
    )


def download(url: str, output_dir: Path, height: str) -> Path:
    from yt_dlp import YoutubeDL

    if not re.match(r"^https?://", url, re.I):
        raise ValueError("Only http/https video links are accepted")
    output_dir.mkdir(parents=True, exist_ok=True)
    template = str(output_dir / "%(title).120B-%(id)s.%(ext)s")

    def progress(data: dict) -> None:
        if data.get("status") == "downloading":
            total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
            done = data.get("downloaded_bytes") or 0
            emit("progress", stage="download", percent=round(done * 100 / total) if total else None)

    options = {
        "format": build_format_selector(height),
        "outtmpl": template,
        "merge_output_format": "mp4",
        "noplaylist": True,
        "windowsfilenames": True,
        "progress_hooks": [progress],
        "quiet": True,
    }
    emit("progress", stage="download", percent=0)
    with YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=True)
        requested = info.get("requested_downloads") or []
        candidate = requested[0].get("filepath") if requested else None
        path = Path(candidate or ydl.prepare_filename(info))
        merged = path.with_suffix(".mp4")
        if merged.exists():
            path = merged
    if not path.exists():
        matches = sorted(output_dir.glob("*"), key=lambda item: item.stat().st_mtime, reverse=True)
        if not matches:
            raise RuntimeError("The downloader completed without creating a video")
        path = matches[0]
    emit("progress", stage="download", percent=100)
    return path.resolve()


def transcribe(video: Path, model_name: str, language: str | None) -> list[Word]:
    from faster_whisper import WhisperModel

    # CUDA is attempted only when CTranslate2 reports a usable CUDA device.
    import ctranslate2
    requested_device = os.environ.get("EASYCLIP_DEVICE", "auto")
    cuda_available = ctranslate2.get_cuda_device_count() > 0
    device = "cuda" if requested_device in {"auto", "cuda"} and cuda_available else "cpu"
    compute = "float16" if device == "cuda" else "int8"
    emit("progress", stage="model", percent=0, detail=f"Loading {model_name}; first use downloads the model once")
    model_options = {
        "device": device,
        "compute_type": compute,
        "cpu_threads": max(2, (os.cpu_count() or 4) - 1),
        "num_workers": 1,
    }
    try:
        model = WhisperModel(model_name, **model_options)
    except Exception:
        if requested_device == "cuda":
            raise
        device, compute = "cpu", "int8"
        model_options.update(device=device, compute_type=compute)
        model = WhisperModel(model_name, **model_options)
    emit("progress", stage="model", percent=100, detail=f"{model_name} ready on {device}")
    emit("progress", stage="transcription", percent=0, detail=f"Fast transcription on {device}")
    segments, info = model.transcribe(
        str(video), language=None if language in {None, "auto"} else language,
        beam_size=1, best_of=1, vad_filter=True, word_timestamps=True,
        condition_on_previous_text=False,
        vad_parameters={"min_silence_duration_ms": 500},
    )
    duration = max(float(info.duration or 1), 1)
    words: list[Word] = []
    for segment in segments:
        for item in segment.words or []:
            text = item.word.strip()
            if text:
                words.append(Word(text, float(item.start), float(item.end)))
        emit("progress", stage="transcription", percent=min(99, round(float(segment.end) * 100 / duration)))
    emit("progress", stage="transcription", percent=100)
    if not words:
        raise RuntimeError("No speech was detected in the video")
    return words


def sentence_text(words: Sequence[Word]) -> str:
    text = " ".join(word.text for word in words)
    return re.sub(r"\s+([,.!?؛،؟:])", r"\1", text).strip()


def candidate_windows(words: Sequence[Word], target: int, tolerance: float = 0.35) -> list[list[Word]]:
    """Generate overlapping candidates (adapted from ai-highlight-clip)."""
    if not words:
        return []
    minimum, maximum = target * (1 - tolerance), target * (1 + tolerance)
    step = max(8.0, target * 0.35)
    end_time = words[-1].end
    windows: list[list[Word]] = []
    cursor = words[0].start
    while cursor < end_time:
        chunk = [word for word in words if word.end >= cursor and word.start <= cursor + maximum]
        if chunk:
            # Prefer punctuation near the target end, while respecting minimum duration.
            eligible = [i for i, word in enumerate(chunk) if word.end - chunk[0].start >= minimum]
            if eligible:
                desired = chunk[0].start + target
                cut = min(eligible, key=lambda i: abs(chunk[i].end - desired) - (2.0 if re.search(r"[.!?؟]$", chunk[i].text) else 0))
                chunk = chunk[: cut + 1]
            if len(chunk) >= 4:
                windows.append(chunk)
        cursor += step
    return windows


ENGAGING = {
    "why", "how", "secret", "mistake", "never", "best", "important", "truth", "imagine", "because",
    "چرا", "چطور", "چگونه", "راز", "اشتباه", "هرگز", "بهترین", "مهم", "حقیقت", "تصور", "زیرا", "اما",
}


def score_window(words: Sequence[Word], media_end: float) -> tuple[float, str]:
    text = sentence_text(words)
    normalized = re.findall(r"[\w\u0600-\u06ff]+", text.lower())
    duration = max(words[-1].end - words[0].start, 1)
    density = sum(token in ENGAGING for token in normalized) / max(len(normalized), 1)
    speech_rate = len(normalized) / duration
    pace = max(0.0, 1 - abs(speech_rate - 2.5) / 2.5)
    completeness = int(bool(re.search(r"[.!?؟]$", text)))
    question = int("?" in text or "؟" in text)
    # Small center bias avoids intros/outros without suppressing strong edge content.
    midpoint = (words[0].start + words[-1].end) / 2
    center = 1 - abs(midpoint / max(media_end, 1) - 0.5) * 0.35
    raw = 45 + density * 500 + pace * 18 + completeness * 8 + question * 8 + center * 10
    title_words = normalized[:8]
    title = " ".join(title_words).strip() or "Highlight"
    return min(99.0, raw), title[:72]


def overlaps(a: Sequence[Word], b: Sequence[Word]) -> float:
    intersection = max(0.0, min(a[-1].end, b[-1].end) - max(a[0].start, b[0].start))
    shortest = min(a[-1].end - a[0].start, b[-1].end - b[0].start)
    return intersection / max(shortest, 0.001)


def pick_highlights(words: Sequence[Word], target: int, count: int) -> list[tuple[list[Word], float, str]]:
    ranked = sorted(
        ((window, *score_window(window, words[-1].end)) for window in candidate_windows(words, target)),
        key=lambda row: row[1], reverse=True,
    )
    selected: list[tuple[list[Word], float, str]] = []
    for item in ranked:
        if all(overlaps(item[0], chosen[0]) < 0.45 for chosen in selected):
            selected.append(item)
        if len(selected) >= count:
            break
    return sorted(selected, key=lambda row: row[0][0].start)


def srt_time(seconds: float) -> str:
    millis = max(0, round(seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"


def caption_groups(words: Sequence[Word], max_chars: int = 32, max_words: int = 7) -> Iterable[list[Word]]:
    """Timestamp-aware compact captions, based on ai-highlight-clip's layout approach."""
    group: list[Word] = []
    for word in words:
        projected = sentence_text([*group, word])
        if group and (len(projected) > max_chars or len(group) >= max_words or word.start - group[-1].end > 0.8):
            yield group
            group = []
        group.append(word)
        if re.search(r"[.!?؟]$", word.text) and len(group) >= 3:
            yield group
            group = []
    if group:
        yield group


def write_srt(words: Sequence[Word], path: Path, offset: float) -> None:
    blocks = []
    for index, group in enumerate(caption_groups(words), 1):
        blocks.append(
            f"{index}\n{srt_time(group[0].start - offset)} --> {srt_time(group[-1].end - offset)}\n"
            f"{sentence_text(group)}\n"
        )
    path.write_text("\n".join(blocks), encoding="utf-8")


def transcript_cache_key(video: Path, model: str, language: str) -> str:
    stat = video.stat()
    identity = f"{video.resolve()}|{stat.st_size}|{stat.st_mtime_ns}|{model}|{language}"
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def cached_transcript(video: Path, model: str, language: str, cache_dir: Path | None) -> list[Word] | None:
    if not cache_dir:
        return None
    path = cache_dir / "transcripts" / f"{transcript_cache_key(video, model, language)}.json"
    if not path.is_file():
        return None
    emit("progress", stage="cache", percent=100, detail="Reusing cached transcript")
    return [Word(**item) for item in json.loads(path.read_text(encoding="utf-8"))]


def save_transcript_cache(video: Path, model: str, language: str, cache_dir: Path | None, words: list[Word]) -> None:
    if not cache_dir:
        return
    directory = cache_dir / "transcripts"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{transcript_cache_key(video, model, language)}.json"
    path.write_text(json.dumps([asdict(word) for word in words], ensure_ascii=False), encoding="utf-8")


def analyze(video: Path, output_dir: Path, model: str, language: str, target: int, count: int, cache_dir: Path | None = None) -> list[Highlight]:
    if not video.is_file():
        raise FileNotFoundError(f"Video does not exist: {video}")
    output_dir.mkdir(parents=True, exist_ok=True)
    words = cached_transcript(video, model, language, cache_dir)
    if words is None:
        words = transcribe(video, model, language)
        save_transcript_cache(video, model, language, cache_dir, words)
    (output_dir / "transcript.json").write_text(
        json.dumps([asdict(word) for word in words], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    selected = pick_highlights(words, max(15, min(target, 180)), max(1, min(count, 30)))
    highlights = []
    for index, (window, score, title) in enumerate(selected, 1):
        caption = output_dir / f"highlight-{index:02}.srt"
        write_srt(window, caption, window[0].start)
        highlights.append(Highlight(
            id=f"highlight-{index:02}", start_seconds=round(window[0].start, 3),
            end_seconds=round(window[-1].end, 3), score=round(score), title=title,
            transcript=sentence_text(window), caption_path=str(caption.resolve()),
        ))
    (output_dir / "highlights.json").write_text(
        json.dumps([asdict(item) for item in highlights], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return highlights


def model_cache_path(model: str) -> Path:
    root = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface")) / "hub"
    return root / f"models--Systran--faster-whisper-{model}"


def model_inventory() -> list[dict]:
    result = []
    for name in ["tiny", "base", "small", "medium", "large-v3"]:
        directory = model_cache_path(name)
        size = sum(item.stat().st_size for item in directory.rglob("*") if item.is_file()) if directory.is_dir() else 0
        result.append({"name": name, "installed": directory.is_dir(), "sizeBytes": size})
    return result


def prepare_model(model: str) -> None:
    if model not in {"tiny", "base", "small", "medium", "large-v3"}:
        raise ValueError("Unsupported Whisper model")
    emit("progress", stage="model-download", percent=1, detail=f"Downloading or verifying {model}")
    WhisperModel = __import__("faster_whisper", fromlist=["WhisperModel"]).WhisperModel
    WhisperModel(model, device="cpu", compute_type="int8", cpu_threads=2, num_workers=1)
    emit("progress", stage="model-download", percent=100, detail=f"{model} is ready")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="easyclip-engine")
    sub = root.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("models")
    prepare = sub.add_parser("prepare-model")
    prepare.add_argument("--model", required=True)
    remove = sub.add_parser("delete-model")
    remove.add_argument("--model", required=True)
    get = sub.add_parser("download")
    get.add_argument("--url", required=True)
    get.add_argument("--output-dir", required=True, type=Path)
    get.add_argument("--height", default="1080")
    run = sub.add_parser("analyze")
    run.add_argument("--input", required=True, type=Path)
    run.add_argument("--output-dir", required=True, type=Path)
    run.add_argument("--model", default="small")
    run.add_argument("--language", default="auto")
    run.add_argument("--target-duration", type=int, default=60)
    run.add_argument("--clip-count", type=int, default=5)
    run.add_argument("--cache-dir", type=Path)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "status":
            import ctranslate2
            output_result(
                ok=True,
                engineVersion="1.0.0",
                cudaAvailable=ctranslate2.get_cuda_device_count() > 0,
                recommendedModels=["tiny", "base", "small", "medium", "large-v3"],
            )
        elif args.command == "models":
            output_result(ok=True, models=model_inventory())
        elif args.command == "prepare-model":
            prepare_model(args.model)
            output_result(ok=True, models=model_inventory())
        elif args.command == "delete-model":
            directory = model_cache_path(args.model)
            if directory.is_dir():
                shutil.rmtree(directory)
            output_result(ok=True, models=model_inventory())
        elif args.command == "download":
            path = download(args.url, args.output_dir, args.height)
            output_result(ok=True, path=str(path))
        else:
            highlights = analyze(args.input, args.output_dir, args.model, args.language, args.target_duration, args.clip_count, args.cache_dir)
            output_result(ok=True, highlights=[asdict(item) for item in highlights])
        return 0
    except Exception as exc:
        emit("error", message=str(exc), error_type=type(exc).__name__)
        output_result(ok=False, error=str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
