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
import subprocess
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


@dataclass
class SpeakerTurn:
    speaker: str
    start_seconds: float
    end_seconds: float


@dataclass
class FaceSample:
    track_id: int
    time_seconds: float
    x: float
    y: float
    width: float
    height: float
    confidence: float
    mouth_activity: float


class AdaptiveLowPass:
    """One-Euro adaptive low-pass filter (Casiez, Roussel & Vogel, CHI 2012)."""
    def __init__(self, min_cutoff: float = 0.6, beta: float = 0.02):
        self.min_cutoff, self.beta = min_cutoff, beta
        self.value: float | None = None
        self.derivative = 0.0
        self.last_raw: float | None = None
        self.last_time: float | None = None

    def update(self, raw: float, timestamp: float) -> float:
        if self.value is None or self.last_time is None or timestamp <= self.last_time:
            self.value, self.last_raw, self.last_time = raw, raw, timestamp
            return raw
        dt = timestamp - self.last_time
        derivative = (raw - (self.last_raw if self.last_raw is not None else raw)) / dt
        derivative_alpha = 1.0 / (1.0 + 1.0 / (2 * math.pi * 1.0 * dt))
        self.derivative = derivative_alpha * derivative + (1 - derivative_alpha) * self.derivative
        cutoff = self.min_cutoff + self.beta * abs(self.derivative)
        alpha = 1.0 / (1.0 + 1.0 / (2 * math.pi * cutoff * dt))
        self.value = alpha * raw + (1 - alpha) * self.value
        self.last_raw, self.last_time = raw, timestamp
        return self.value


def smooth_face_tracks(samples: list[FaceSample], dead_zone: float = 0.007, max_velocity: float = 0.28) -> list[FaceSample]:
    """Remove detector jitter while retaining deliberate fast subject motion."""
    output: list[FaceSample] = []
    for track_id in sorted(set(item.track_id for item in samples)):
        track = sorted((item for item in samples if item.track_id == track_id), key=lambda item: item.time_seconds)
        filters = [AdaptiveLowPass(), AdaptiveLowPass(), AdaptiveLowPass(0.5, 0.01), AdaptiveLowPass(0.5, 0.01)]
        held: list[float] | None = None
        previous_time: float | None = None
        for item in track:
            raw = [item.x, item.y, item.width, item.height]
            filtered = [flt.update(value, item.time_seconds) for flt, value in zip(filters, raw)]
            if held is None:
                held = filtered
            else:
                dt = max(1e-3, item.time_seconds - (previous_time if previous_time is not None else item.time_seconds))
                for index, target in enumerate(filtered):
                    delta = target - held[index]
                    if abs(delta) < dead_zone:
                        continue
                    held[index] += max(-max_velocity * dt, min(max_velocity * dt, delta))
            output.append(FaceSample(item.track_id, item.time_seconds, round(held[0], 5), round(held[1], 5), round(held[2], 5), round(held[3], 5), item.confidence, item.mouth_activity))
            previous_time = item.time_seconds
    return sorted(output, key=lambda item: (item.time_seconds, item.track_id))


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
        first=next((index for index,word in enumerate(words) if word.end>=cursor),len(words)-1)
        # Deep boundary optimization: walk back to the nearest completed sentence,
        # but never add more than six seconds of unrelated lead-in.
        for index in range(first-1,max(-1,first-18),-1):
            if re.search(r"[.!?؟]$",words[index].text) and cursor-words[index].end<=6:
                first=index+1
                break
        chunk = [word for word in words[first:] if word.start <= cursor + maximum]
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


def score_window(words: Sequence[Word], media_end: float, user_intent: str = "") -> tuple[float, str]:
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
    intent_tokens=set(re.findall(r"[\w\u0600-\u06ff]+",user_intent.lower()))
    intent_match=len(intent_tokens.intersection(normalized))/max(1,len(intent_tokens)) if intent_tokens else 0
    raw = 45 + density * 500 + pace * 18 + completeness * 8 + question * 8 + center * 10 + intent_match * 25
    title_words = normalized[:8]
    title = " ".join(title_words).strip() or "Highlight"
    return min(99.0, raw), title[:72]


def overlaps(a: Sequence[Word], b: Sequence[Word]) -> float:
    intersection = max(0.0, min(a[-1].end, b[-1].end) - max(a[0].start, b[0].start))
    shortest = min(a[-1].end - a[0].start, b[-1].end - b[0].start)
    return intersection / max(shortest, 0.001)


def pick_highlights(words: Sequence[Word], target: int, count: int, user_intent: str = "") -> list[tuple[list[Word], float, str]]:
    ranked = sorted(
        ((window, *score_window(window, words[-1].end, user_intent)) for window in candidate_windows(words, target)),
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


def censor_word(text: str) -> str:
    clean = re.sub(r"[^\w\u0600-\u06ff]", "", text.lower())
    blocked = {"fuck", "fucking", "shit", "bitch", "asshole", "لعنتی", "کثافت", "احمق", "حرومزاده"}
    if clean not in blocked or len(text) < 2:
        return text
    return text[0] + "•" * max(2, len(text) - 1)


def write_srt(words: Sequence[Word], path: Path, offset: float) -> None:
    blocks = []
    for index, group in enumerate(caption_groups(words), 1):
        blocks.append(
            f"{index}\n{srt_time(group[0].start - offset)} --> {srt_time(group[-1].end - offset)}\n"
            f"{' '.join(censor_word(word.text) for word in group)}\n"
        )
    path.write_text("\n".join(blocks), encoding="utf-8")


def write_karaoke_ass(words: Sequence[Word], path: Path, offset: float) -> None:
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Karaoke,Vazirmatn,68,&H00FFFFFF,&H006C63FF,&H00100D18,&H80000000,-1,0,0,0,100,100,0,0,1,4,1,2,70,70,150,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    dialogues: list[str] = []
    for group in caption_groups(words, max_chars=30, max_words=6):
        karaoke = []
        for word in group:
            duration = max(1, round((word.end - word.start) * 100))
            text = censor_word(word.text).replace("{", "(").replace("}", ")")
            karaoke.append(f"{{\\k{duration}}}{text}")
        start = srt_time(group[0].start - offset).replace(",", ".")[:-1]
        end = srt_time(group[-1].end - offset).replace(",", ".")[:-1]
        dialogues.append(f"Dialogue: 0,{start},{end},Karaoke,,0,0,0,,{' '.join(karaoke)}")
    path.write_text(header + "\n".join(dialogues) + "\n", encoding="utf-8-sig")


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


def analyze(video: Path, output_dir: Path, model: str, language: str, target: int, count: int, cache_dir: Path | None = None, user_intent: str = "") -> list[Highlight]:
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
    selected = pick_highlights(words, max(15, min(target, 180)), max(1, min(count, 30)), user_intent)
    filler_words={"um","uh","like","basically","actually","well","یعنی","مثلا","مثلاً","خب","حالا","درواقع","اِ","اُم"}
    normalized_words=[re.sub(r"[^\w\u0600-\u06ff]","",word.text.lower()) for word in words]
    filler_count=sum(token in filler_words for token in normalized_words)
    speech_duration=max(.1,words[-1].end-words[0].start)
    stats={"wordCount":len(words),"fillerCount":filler_count,"fillerRatio":round(filler_count/max(1,len(words)),4),"wordsPerMinute":round(len(words)*60/speech_duration,1),"goldenQuotes":[{"title":title,"score":round(score),"start":round(window[0].start,2),"end":round(window[-1].end,2)} for window,score,title in sorted(selected,key=lambda item:item[1],reverse=True)[:10]]}
    (output_dir / "speech-stats.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding="utf-8")
    highlights = []
    for index, (window, score, title) in enumerate(selected, 1):
        caption = output_dir / f"highlight-{index:02}.ass"
        write_karaoke_ass(window, caption, window[0].start)
        write_srt(window, output_dir / f"highlight-{index:02}.srt", window[0].start)
        highlights.append(Highlight(
            id=f"highlight-{index:02}", start_seconds=round(window[0].start, 3),
            end_seconds=round(window[-1].end, 3), score=round(score), title=title,
            transcript=sentence_text(window), caption_path=str(caption.resolve()),
        ))
    (output_dir / "highlights.json").write_text(
        json.dumps([asdict(item) for item in highlights], ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return highlights


def merge_speaker_turns(turns: list[SpeakerTurn], gap: float = 0.35) -> list[SpeakerTurn]:
    merged: list[SpeakerTurn] = []
    for turn in sorted(turns, key=lambda item: item.start_seconds):
        if merged and merged[-1].speaker == turn.speaker and turn.start_seconds - merged[-1].end_seconds <= gap:
            merged[-1].end_seconds = max(merged[-1].end_seconds, turn.end_seconds)
        else:
            merged.append(turn)
    return merged


def diarization_cache_path(video: Path, cache_dir: Path) -> Path:
    stat = video.stat()
    identity = f"{video.resolve()}|{stat.st_size}|{stat.st_mtime_ns}|speaker-diarization-3.1"
    directory = cache_dir / "diarization"
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{hashlib.sha256(identity.encode('utf-8')).hexdigest()}.json"


def diarize_video(video: Path, output_dir: Path, cache_dir: Path, min_speakers: int, max_speakers: int) -> list[SpeakerTurn]:
    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Professional speaker-model access is not configured")
    cached = diarization_cache_path(video, cache_dir)
    if cached.is_file():
        emit("progress", stage="diarization-cache", percent=100, detail="Reusing cached speaker timeline")
        return [SpeakerTurn(**item) for item in json.loads(cached.read_text(encoding="utf-8"))]
    output_dir.mkdir(parents=True, exist_ok=True)
    audio = output_dir / "speaker-analysis.wav"
    emit("progress", stage="diarization-audio", percent=5, detail="Preparing speech audio")
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video),
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(audio)
    ], check=True)
    emit("progress", stage="diarization-model", percent=15, detail="Loading encrypted speaker model access")
    from pyannote.audio import Pipeline
    try:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", token=token)
    except TypeError:
        pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=token)
    if pipeline is None:
        raise RuntimeError("Speaker model could not be loaded; verify accepted model terms")
    try:
        import torch
        if torch.cuda.is_available():
            pipeline.to(torch.device("cuda"))
            emit("progress", stage="diarization-model", percent=30, detail="Speaker model loaded on NVIDIA GPU")
        else:
            emit("progress", stage="diarization-model", percent=30, detail="Speaker model loaded on CPU")
        result = pipeline(str(audio), min_speakers=min_speakers, max_speakers=max_speakers)
        annotation = getattr(result, "speaker_diarization", result)
        turns = [SpeakerTurn(str(label), round(float(segment.start), 3), round(float(segment.end), 3))
                 for segment, _, label in annotation.itertracks(yield_label=True)]
        turns = merge_speaker_turns(turns)
        cached.write_text(json.dumps([asdict(turn) for turn in turns], ensure_ascii=False, indent=2), encoding="utf-8")
        emit("progress", stage="diarization", percent=100, detail=f"Detected {len(set(turn.speaker for turn in turns))} speakers")
        return turns
    finally:
        audio.unlink(missing_ok=True)


def track_faces(video: Path, cache_dir: Path, samples_per_second: float = 5.0) -> list[FaceSample]:
    stat = video.stat()
    identity = f"{video.resolve()}|{stat.st_size}|{stat.st_mtime_ns}|mediapipe-face-v3-mouth-motion|{samples_per_second}"
    directory = cache_dir / "face-tracking"
    directory.mkdir(parents=True, exist_ok=True)
    cached = directory / f"{hashlib.sha256(identity.encode('utf-8')).hexdigest()}.json"
    if cached.is_file():
        emit("progress", stage="face-cache", percent=100, detail="Reusing cached precision face tracks")
        return [FaceSample(**item) for item in json.loads(cached.read_text(encoding="utf-8"))]
    import cv2
    detector_name = "MediaPipe"
    media_detector = None
    try:
        import mediapipe as mp
        media_detector = mp.solutions.face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.42)
    except Exception:
        detector_name = "OpenCV fallback"
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    capture = cv2.VideoCapture(str(video))
    if not capture.isOpened():
        raise RuntimeError("Video could not be opened for face tracking")
    fps = max(1.0, capture.get(cv2.CAP_PROP_FPS) or 25.0)
    total = max(1, int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 1))
    stride = max(1, int(fps / max(0.5, samples_per_second)))
    # cx, cy, width, height, vx, vy, last_frame, confidence
    tracks: dict[int, tuple[float, float, float, float, float, float, int, float]] = {}
    next_id = 1
    samples: list[FaceSample] = []
    mouth_history: dict[int, object] = {}
    previous_histogram = None
    frame_index = 0
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if frame_index % stride:
                frame_index += 1
                continue
            height, width = frame.shape[:2]
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            histogram = cv2.calcHist([gray], [0], None, [32], [0, 256])
            cv2.normalize(histogram, histogram)
            if previous_histogram is not None and cv2.compareHist(previous_histogram, histogram, cv2.HISTCMP_CORREL) < 0.38:
                # A hard shot boundary starts a fresh identity domain. Never pan
                # from a face in one camera shot toward a face in the next shot.
                tracks.clear()
                mouth_history.clear()
            previous_histogram = histogram
            found: list[tuple[float, float, float, float, float]] = []
            if media_detector is not None:
                result = media_detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                for detection in result.detections or []:
                    box = detection.location_data.relative_bounding_box
                    x, y = max(0.0, box.xmin), max(0.0, box.ymin)
                    face_width, face_height = min(1.0 - x, box.width), min(1.0 - y, box.height)
                    if face_width > 0.015 and face_height > 0.015:
                        found.append((x, y, face_width, face_height, float(detection.score[0])))
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                for x, y, face_width, face_height in cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(max(32, width // 40), max(32, height // 40))):
                    found.append((x / width, y / height, face_width / width, face_height / height, 0.68))
            available = set(tracks)
            for x, y, face_width, face_height, confidence in sorted(found, key=lambda item: item[2] * item[3], reverse=True):
                center_x, center_y = x + face_width / 2, y + face_height / 2
                candidates = []
                for track_id, old in tracks.items():
                    if track_id not in available or frame_index - old[6] > stride * 12:
                        continue
                    elapsed = max(1, frame_index - old[6]) / stride
                    predicted_x, predicted_y = old[0] + old[4] * elapsed, old[1] + old[5] * elapsed
                    distance = (center_x - predicted_x) ** 2 + (center_y - predicted_y) ** 2
                    size_penalty = abs(face_width * face_height - old[2] * old[3]) * 0.35
                    candidates.append((track_id, distance + size_penalty))
                track_id, distance = min(candidates, key=lambda item: item[1]) if candidates else (next_id, 999.0)
                if distance > 0.065:
                    track_id = next_id
                    next_id += 1
                    old = (center_x, center_y, face_width, face_height, 0.0, 0.0, frame_index, confidence)
                else:
                    old = tracks[track_id]
                available.discard(track_id)
                alpha = 0.42
                smooth_x, smooth_y = old[0] * (1-alpha) + center_x * alpha, old[1] * (1-alpha) + center_y * alpha
                smooth_w, smooth_h = old[2] * (1-alpha) + face_width * alpha, old[3] * (1-alpha) + face_height * alpha
                velocity_x = old[4] * 0.65 + (smooth_x - old[0]) * 0.35
                velocity_y = old[5] * 0.65 + (smooth_y - old[1]) * 0.35
                tracks[track_id] = (smooth_x, smooth_y, smooth_w, smooth_h, velocity_x, velocity_y, frame_index, confidence)
                # Approximate lip activity from the lower-central face region. This is
                # deliberately computed after identity assignment so every track has
                # its own temporal baseline and background motion is not mixed in.
                left = max(0, int((smooth_x - smooth_w * 0.28) * width))
                right = min(width, int((smooth_x + smooth_w * 0.28) * width))
                top = max(0, int((smooth_y + smooth_h * 0.08) * height))
                bottom = min(height, int((smooth_y + smooth_h * 0.43) * height))
                mouth_activity = 0.0
                if right > left and bottom > top:
                    mouth = cv2.resize(gray[top:bottom, left:right], (40, 24))
                    previous_mouth = mouth_history.get(track_id)
                    if previous_mouth is not None:
                        mouth_activity = min(1.0, float(cv2.absdiff(mouth, previous_mouth).mean()) / 32.0)
                    mouth_history[track_id] = mouth
                samples.append(FaceSample(track_id, round(frame_index / fps, 3), round(max(0, smooth_x-smooth_w/2), 5), round(max(0, smooth_y-smooth_h/2), 5), round(smooth_w, 5), round(smooth_h, 5), round(confidence, 4), round(mouth_activity, 4)))
            if frame_index % max(stride, int(total / 100) or 1) == 0:
                emit("progress", stage="face-tracking", percent=min(99, round(frame_index * 100 / total)), detail=f"{detector_name}: tracking {max(0, next_id - 1)} faces")
            frame_index += 1
    finally:
        capture.release()
        if media_detector is not None:
            media_detector.close()
    samples = smooth_face_tracks(samples)
    cached.write_text(json.dumps([asdict(sample) for sample in samples], ensure_ascii=False), encoding="utf-8")
    emit("progress", stage="face-tracking", percent=100, detail=f"{detector_name}: created {max(0, next_id - 1)} stable, smoothed tracks")
    return samples


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
    diarize = sub.add_parser("diarize")
    diarize.add_argument("--input", required=True, type=Path)
    diarize.add_argument("--output-dir", required=True, type=Path)
    diarize.add_argument("--cache-dir", required=True, type=Path)
    diarize.add_argument("--min-speakers", type=int, default=1)
    diarize.add_argument("--max-speakers", type=int, default=4)
    faces = sub.add_parser("track-faces")
    faces.add_argument("--input", required=True, type=Path)
    faces.add_argument("--cache-dir", required=True, type=Path)
    faces.add_argument("--samples-per-second", type=float, default=4.0)
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
    run.add_argument("--user-intent", default="")
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
        elif args.command == "diarize":
            turns = diarize_video(args.input, args.output_dir, args.cache_dir, max(1, args.min_speakers), max(args.min_speakers, args.max_speakers))
            output_result(ok=True, speakers=sorted(set(turn.speaker for turn in turns)), turns=[asdict(turn) for turn in turns])
        elif args.command == "track-faces":
            samples = track_faces(args.input, args.cache_dir, args.samples_per_second)
            output_result(ok=True, trackCount=len(set(sample.track_id for sample in samples)), samples=[asdict(sample) for sample in samples])
        elif args.command == "download":
            path = download(args.url, args.output_dir, args.height)
            output_result(ok=True, path=str(path))
        else:
            highlights = analyze(args.input, args.output_dir, args.model, args.language, args.target_duration, args.clip_count, args.cache_dir, args.user_intent)
            output_result(ok=True, highlights=[asdict(item) for item in highlights])
        return 0
    except Exception as exc:
        emit("error", message=str(exc), error_type=type(exc).__name__)
        output_result(ok=False, error=str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
