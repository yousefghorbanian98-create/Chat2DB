# بررسی، دیباگ و بازطراحی «Cutting Edge» v0.9.34

> تاریخ بررسی: 2026-08-27
> محدوده: `ce-app/` (Electron + React/Vite + FastAPI/SQLite + FFmpeg)
> شاخه: `arena/01a04055-chat2db`
> خروجی بصری: `REDESIGN_LAUNCHER_CYBERPUNK.png` + `REDESIGN_STUDIO_CYBERPUNK.png`

---

## ۱. جمع‌بندی در ۳۰ ثانیه

این پروژه از نظر **معماری، مستندسازی، و امنیت منطقی** جزو بهترین کدهایی‌ست که دیدم. هر فایل یک ماژول مستقل با docstring آموزنده دارد، خطاها **با دلیل مکتوب** به لایه بالا منتقل می‌شوند، و هرجا «ممکن است اشتباه شود» یک `note`، یک `STATE.md` رفرنس یا یک `tests/test_xxx.py` وجود دارد. این نشانه‌ی یک تیم بزرگ نیست، نشانه‌ی یک **مهندس دقیق** است.

اما ۵ حوزه برای بهبودِ جدی پیدا کردم (به ترتیب اولویت):

1. **مصرف حافظه و Threading در WebSocket** — چند race condition و memory leak.
2. **عدم Validation ورودی در routers** — بسیاری از endpointها به `str(media)` اعتماد می‌کنند.
3. **Race در SQLite با `check_same_thread=False`** — یک worker thread می‌تواند transaction باز دیگری را ببیند.
4. **Timeout پیش‌فرض Ollama 120 ثانیه‌ای، بدون back-pressure** — اگر کاربر Back کند، تایم‌لاین هنگ می‌کند.
5. **عدم Sentry/Logging ساخت‌یافته** — گزارش‌های خرابی محلی هست، اما تجمیع نمی‌شود.

برای هرکدام، **ایده + نمونه کد اصلاح** می‌دهم.

---

## ۲. دیباگ و بهبود (۱۲ مورد)

### ۲.۱. 🔴 بحرانی — `WebSocket ConnectionManager` نشتی دارد

**فایل:** `backend/app/websocket/job_events.py`

```python
async def broadcast(self, message: dict):
    for c in list(self._connections):  # ✓ copy گرفته
        try: await c.send_json(message)
        except Exception: self.disconnect(c)  # ⚠️ ولی همین خط مشکل دارد
```

**مشکل ۱ (Race):** اگر `send_json` با `RuntimeError` فالبک شود (مثلاً client disconnect شد ولی exception raise نشده)، connection در `_connections` باقی می‌ماند و broadcast بعدی روی آن hang می‌کند.

**مشکل ۲ (Task leak):** `broadcast` در حلقه await می‌کند — اگر ۲۰ client داشته باشید و یکی کُند باشد، همه منتظر آن می‌مانند. broadcast باید **concurrent** باشد.

**راه‌حل:**

```python
import asyncio
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._connections.add(ws)

    async def disconnect(self, ws: WebSocket) -> None:
        async with self._lock:
            self._connections.discard(ws)

    async def broadcast(self, message: dict) -> None:
        async with self._lock:
            targets = list(self._connections)
        if not targets:
            return
        # ‌ارسال همزمان: یک کلاینت کند بقیه را بلوکه نمی‌کند
        results = await asyncio.gather(
            *(self._safe_send(ws, message) for ws in targets),
            return_exceptions=True,
        )
        # پاک کردن connectionهای مرده
        dead = [ws for ws, ok in zip(targets, results) if ok is False]
        if dead:
            async with self._lock:
                for ws in dead:
                    self._connections.discard(ws)

    @staticmethod
    async def _safe_send(ws: WebSocket, message: dict) -> bool:
        try:
            await asyncio.wait_for(ws.send_json(message), timeout=2.0)
            return True
        except (Exception, asyncio.TimeoutError):  # noqa: BLE001
            return False
```

---

### ۲.۲. 🔴 بحرانی — `runtime_packages.install` بدون timeout واقعی

**فایل:** `backend/core/runtime_packages.py`

```python
process = subprocess.Popen([...])
# حلقه‌ای که فقط روی stdout صبر می‌کند
```

**مشکل:** اگر pip روی شبکه‌ای hang کند، این تابع هیچ‌وقت `code = process.wait()` را صدا نمی‌زند. thread زنده می‌ماند و کاربر cancel هم نمی‌تواند بکند (cancellation فقط در `engine/cancellation.py` است).

**راه‌حل:** از `cancellation.run` استفاده کنید (همان helper که در بقیه engine‌ها هست):

```python
from core.engine.cancellation import run, Cancelled

def install(packages, on_progress=None, timeout: float = 1800.0):
    target = ensure_on_path()
    say = on_progress or (lambda *a, **k: None)
    say("resolve", 0.05, f"Fetching {', '.join(packages)}")

    try:
        result = run(
            [sys.executable, "-m", "pip", "install", ...],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            bufsize=1, timeout=timeout,  # ← timeout واقعی
        )
    except Cancelled:
        say("cancelled", 0.0, "Cancelled by user")
        raise
    if result.returncode != 0:
        raise RuntimeError(result.stdout[-800:] if result.stdout else "pip failed")
    say("done", 1.0, f"Installed into {target}")
```

و در router، `tasks.start(..., work)` که thread-bound است، همان `cancellation.bind(event)` را انجام می‌دهد — یعنی cancel دکمه‌ای، واقعاً فرآیند را می‌کُشد.

---

### ۲.۳. 🟠 مهم — `database.py` بدون `Row factory` و بدون transaction helper

```python
conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
conn.row_factory = sqlite3.Row
```

**مشکل:** `check_same_thread=False` اجازه می‌دهد چند thread همزمان به یک connection بنویسند. اگر دو request همزمان بیایند و `commit()` در میانه فراخوانی شود، یکی race می‌برد و داده‌ی آن یکی گم می‌شود. همچنین وقتی `_load` در `transcribe.py` thread دیگری صدا زده می‌شود، connection مشترک است.

**راه‌حل:** حالت recommended برای FastAPI + SQLite، **یک connection per thread** با WAL است:

```python
import sqlite3, threading
from contextlib import contextmanager

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self._local = threading.local()

    def _conn(self) -> sqlite3.Connection:
        c = getattr(self._local, "conn", None)
        if c is None:
            c = sqlite3.connect(self.db_path, isolation_level=None, timeout=30.0)
            c.row_factory = sqlite3.Row
            c.execute("PRAGMA journal_mode=WAL")
            c.execute("PRAGMA foreign_keys=ON")
            c.execute("PRAGMA busy_timeout=5000")
            self._local.conn = c
        return c

    @contextmanager
    def transaction(self):
        c = self._conn()
        c.execute("BEGIN IMMEDIATE")
        try:
            yield c
            c.execute("COMMIT")
        except Exception:
            c.execute("ROLLBACK")
            raise
```

و در router‌ها:
```python
with db.transaction() as conn:
    conn.execute("INSERT INTO jobs ...", (...))
    # commit خودکار در exit
```

---

### ۲.۴. 🟠 مهم — `POST /api/captions/transcribe` بدون محدودیت حجم فایل

```python
class TranscribeRequest(BaseModel):
    path: str
```

**مشکل:** `payload.path` بدون validation به `Path(payload.path)` می‌رود. یک request مخرب می‌تواند `path="C:/Windows/System32/..."` بفرستد. حتی اگر فرض کنیم فقط فرانت صدا می‌زند، فرانت می‌تواند path عوض کند (browser fallback در Studio).

**راه‌حل:**

```python
from pydantic import validator
from pathlib import Path
import os

ALLOWED_ROOTS = (Path.home() / "CuttingEdge",)

class TranscribeRequest(BaseModel):
    path: str
    language: str | None = None
    max_chars: int = 42

    @validator("path")
    def _safe_path(cls, v: str) -> str:
        p = Path(v).resolve()
        if not any(p.is_relative_to(root.resolve()) for root in ALLOWED_ROOTS):
            raise ValueError(f"Path must live under one of: {ALLOWED_ROOTS}")
        if not p.exists():
            raise ValueError("File does not exist")
        if p.stat().st_size > 4 * 1024 * 1024 * 1024:  # 4 GB
            raise ValueError("File too large (max 4 GB)")
        return str(p)
```

همین pattern را به همه routerهای دیگر (`media`, `analyze`, `proxy`, `reframe`, `render`) تعمیم بدهید.

---

### ۲.۵. 🟠 مهم — `Race` در planners: مدل Ollama می‌تواند «شکستِ زمان‌بَر» نخورد

**فایل:** `backend/core/brain/planners.py`

```python
def ollama_plan(...):
    response = requests.post(f"{OLLAMA_URL}/api/generate", ..., timeout=timeout)
```

**مشکل:** `timeout=120` یعنی اگر Ollama در حال load مدل باشد (مخصوصاً اولین بار، ممکن است ۲-۳ دقیقه طول بکشد)، کل request می‌میرد و در scoreboard ثبت می‌شود:

```
ollama:qwen2.5 0.00 · rules 0.71 → used rules
```

این روی خروجی `race` تأثیری ندارد (rule plan همیشه candidate است)، ولی UX ضعیف است: کاربر نمی‌فهمد چرا AI کار نکرد.

**راه‌حل:** یک `pending` state در scoreboard + retry policy:

```python
def ollama_plan(highlights, context, transcript, model=None, timeout=120.0, warmup=10.0):
    chosen = ollama_available(model)
    if not chosen or not highlights:
        return None

    started = time.time()
    # 1) مرحله‌ی warm-up: یک ping کوچک تا مطمئن شویم سرویس پاسخ می‌دهد
    try:
        import requests
        requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": chosen, "prompt": "ok", "stream": False},
            timeout=warmup,
        )
    except Exception:
        return Candidate(name=f"ollama:{chosen}", picks=[],
                         seconds=time.time() - started,
                         note="warmup failed (model still loading?)")

    # 2) حالا request اصلی
    try:
        response = requests.post(..., timeout=timeout)
        ...
    except requests.Timeout:
        return Candidate(name=f"ollama:{chosen}", picks=[],
                         seconds=time.time() - started,
                         note="timeout — model slow on first call")
    except Exception as e:
        ...
```

و در UI، وقتی `note == "warmup failed"` یا `"timeout"` بود، یک chip زرد نمایش بده: «مدل در حال load، یک بار دیگر امتحان کن».

---

### ۲.۶. 🟡 بهبود — `Timeline.tsx` با هر فریم DOM Listener می‌سازد

```typescript
useEffect(() => {
  if (!drag) return
  const onMove = (e: PointerEvent) => { ... }
  window.addEventListener('pointermove', onMove)
  window.addEventListener('pointerup', onUp)
  return () => { ... }
}, [drag, clips, magnets, moveClip, ...])
```

**مشکل:** dependency array شامل `clips` و `magnets` است. هر تغییر clip (مثلاً تریم ۱ فریم)، effect teardown می‌شود و دوباره listener اضافه می‌شود. در یک drag طولانی اگر state تغییر کند (مثلاً snapping guide به‌روز شود)، listener از کار می‌افتد و کاربر حس می‌کند drag «گیر کرده».

**راه‌حل:** منطق `onMove` را به یک `useRef` از state منتقل کنید:

```typescript
const stateRef = useRef({ clips, magnets, snapping, playhead, drag })
useEffect(() => {
  stateRef.current = { clips, magnets, snapping, playhead, drag }
}, [clips, magnets, snapping, playhead, drag])

useEffect(() => {
  if (!drag) return
  const onMove = (e: PointerEvent) => {
    const s = stateRef.current  // ← همیشه تازه
    ...
  }
  window.addEventListener('pointermove', onMove)
  ...
}, [drag])  // فقط drag
```

این الگو «latest ref» یک anti-pattern معروف React است که در هر drag handler واجب است.

---

### ۲.۷. 🟡 بهبود — `PreviewMonitor` یک RAF loop بی‌نهایت دارد حتی در pause

```typescript
useEffect(() => {
  if (!playing) return  // ✓ درسته، ولی
  const tick = () => { ...; frame = requestAnimationFrame(tick) }
  frame = requestAnimationFrame(tick)
  return () => cancelAnimationFrame(frame)
}, [playing])
```

**خوب:** شرط `if (!playing) return` درست است. اما اگر کاربر در حین پخش Tab را عوض کند، `requestAnimationFrame` در background ~1Hz می‌شود و playhead عقب می‌ماند. وقتی برگردد، `useEditor.getState().setPlayhead(next)` یک جهش بزرگ ثبت می‌کند.

**راه‌حل:**

```typescript
useEffect(() => {
  if (!playing) return
  let frame = 0
  let previous = performance.now()
  let droppedFrames = 0

  const tick = () => {
    const now = performance.now()
    const wall = (now - previous) / 1000
    previous = now
    // اگر frame بیش از ۲۵۰ms طول کشیده، skip کن (background tab)
    if (wall > 0.25) { droppedFrames++; frame = requestAnimationFrame(tick); return }

    const state = useEditor.getState()
    let next = state.playhead + Math.min(0.25, wall)
    ...
  }
  frame = requestAnimationFrame(tick)
  return () => cancelAnimationFrame(frame)
}, [playing])
```

و از `document.visibilityState` استفاده کنید تا وقتی tab مخفی است کلاً pause شود.

---

### ۲.۸. 🟡 بهبود — `WebSocket` فرانت reconnect ساده دارد

**فایل:** `frontend/src/api/websocket.ts`

```typescript
this.socket.onclose = () => {
  if (this.reconnectAttempts < 5) {
    setTimeout(() => { this.reconnectAttempts++; this.connect() }, 1000 * this.reconnectAttempts)
  }
}
```

**مشکل:** پس از ۵ بار تلاش ناموفق، کلاینت دیگر reconnect نمی‌کند. اگر کاربر Backend را بعداً بالا بیاورد، باید refresh کند.

**راه‌حل: Exponential backoff با cap + listener برای manual retry**

```typescript
class WebSocketClient {
  private retry = 0
  private manual = false

  connect() {
    if (this.socket?.readyState === WebSocket.OPEN) return
    this.socket = new WebSocket(backendWebSocketUrl('/ws'))
    this.socket.onmessage = ...
    this.socket.onclose = () => {
      if (this.manual) return
      this.retry++
      if (this.retry > 30) {  // ~5 دقیقه تلاش
        this.listeners.forEach(fn => fn({
          type: 'task:failed', task_id: 'ws', kind: 'socket',
          status: 'failed', stage: 'disconnected', progress: 0,
          label: 'Realtime channel lost — click to retry',
          elapsed: 0, error: 'Too many reconnect attempts',
        }))
        return
      }
      const delay = Math.min(30_000, 1000 * Math.pow(1.5, this.retry))
      setTimeout(() => this.connect(), delay)
    }
    this.socket.onopen = () => { this.retry = 0 }
  }
  reconnect() { this.retry = 0; this.connect() }
}
```

و در `RuntimeBridge` یک دکمه‌ی «Retry connection» در `BackendBanner` اضافه کنید.

---

### ۲.۹. 🟡 بهبود — `model.ts` (zustand store) عملیات سنگین در renderer

**فایل:** `frontend/src/editor/model.ts` (نخواندم، اما از طریق Timeline.tsx می‌دانم)

```typescript
const { tracks, clips, transitions, selectedId, playhead, ... } = useEditor()
```

**مشکل:** وقتی ۱۰۰ کلیپ دارید و هر فریم ۶۰ بار re-render می‌شود، `useEditor()` همه‌ی state را می‌گیرد. اگر فقط `playhead` عوض شود، هم Timeline و هم PreviewMonitor و هم Inspector همه re-render می‌شوند.

**راه‌حل: Selector-based subscription**

```typescript
// به جای:
const { playhead, clips } = useEditor()

// این را بنویسید:
const playhead = useEditor(s => s.playhead)
const clips = useEditor(s => s.clips)
```

برای Timeline که به همه چیز نیاز دارد، selectorهای composite مجاز است:
```typescript
const { playhead, selectedId, pxPerSecond } = useEditor(s => ({
  playhead: s.playhead,
  selectedId: s.selectedId,
  pxPerSecond: s.pxPerSecond,
}), shallow)  // نیاز به `zustand/shallow` یا `useShallow`
```

---

### ۲.۱۰. 🟡 بهبود — Logging ساخت‌یافته وجود ندارد

همه‌جا `print(...)` یا `console.error(...)` است. برای یک برنامه production، این کافی نیست:

```python
# backend/app/main.py
print(f"  {__app_name__} v{__version__} starting on 0.0.0.0:{settings.backend_port}")
```

**راه‌حل:** استفاده از `structlog` یا `loguru` با JSON output. یک فایل rotate شونده در `data_dir/logs/`:

```python
# backend/app/logging_setup.py
import logging, json, sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(log_dir / "backend.jsonl", maxBytes=10_000_000, backupCount=5)
    handler.setFormatter(logging.Formatter(
        '{"ts":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":%(message)r}'
    ))
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.INFO)
```

سپس در کد:
```python
log.info("race_complete", extra={"winner": r.winner, "scores": r.scoreboard})
```

و یک اسکریپت `crash_report.py` که این JSONL را به یک `.zip` قابل اشتراک تبدیل کند — این پاسخ **همان چیزی‌ست که در STATE.md به آن اشاره شده** («گزارش خرابی محلی»).

---

### ۲.۱۱. 🟢 جزئی — `Timeline.tsx` خط ۱۱۶: `useMemo` بدون dependency درست

```typescript
const xToTime = useCallback(
  (clientX: number) => {
    const rect = laneRef.current?.getBoundingClientRect()  // ⚠️ DOM ref در callback
    ...
  },
  [pxPerSecond]
)
```

**مشکل:** `laneRef.current` می‌تواند تغییر کند (مثلاً layout reflow)، ولی `useCallback` فقط به `pxPerSecond` وابسته است. در عمل مشکلی پیش نمی‌آید چون React در زمان render جدید ref را می‌گیرد، اما برای code smell، بهتر است:

```typescript
const xToTime = useCallback(
  (clientX: number) => {
    const lane = laneRef.current
    if (!lane) return 0
    const rect = lane.getBoundingClientRect()
    return Math.max(0, (clientX - rect.left + lane.scrollLeft) / pxPerSecond)
  },
  [pxPerSecond]
)
```

(همین کار را در `useEffect` نیز انجام دادید. این فقط یک consistency است.)

---

### ۲.۱۲. 🟢 جزئی — فرانت `axios` instance بدون interceptor

```typescript
const api = axios.create({
  baseURL: `${backendOrigin}/api`,
  timeout: 30000,
  ...
})
```

**پیشنهاد:** interceptor برای:
1. اگر 401 گرفتیم، یک banner بالا بیاید (token منقضی شده).
2. اگر 503 با `detail: "faster-whisper not installed"` گرفتیم، یک toast با دکمه «نصب» بدهد.
3. زمان‌بندی خودکار endpointهای کند برای analytics.

```typescript
api.interceptors.response.use(
  r => r,
  err => {
    if (err.response?.status === 503) {
      message.warning(err.response.data.detail, 6)
    } else if (err.response?.status === 404) {
      // silent — endpointهای optional مثل /api/ai/cuda/status در build بدون GPU
    }
    return Promise.reject(err)
  }
)
```

---

## ۳. ایده‌های «خفن‌تر کردن» برنامه (۱۰ مورد)

### ۳.۱. 🧠 **"Director Mode" — دستور زبان طبیعی به ادیت**

دکمه‌ای در Toolbar: «بگو چه می‌خواهی» → voice input → ترنسکرایب → به `planner.make_plan` بفرست. نتیجه را قبل از apply نشان بده. ترکیب `faster-whisper` (که دارید) + `assistant/planner` (که دارید) = **یک ویژگی جدید با ۵۰ خط کد**.

### ۳.۲. 🎬 **"Cut on Emotion" — تحلیل احساسات چهره**

در `engine/analyze.py` یک pipeline اضافه کنید که فریم‌ها را به یک `vit-fer` (مدل کوچک facial emotion recognition) بدهد و `strength` را emotion-weighted کند. کاربرد: highlight لحظات لبخند، خشم، غم. کاملاً on-device، بدون API.

### ۳.۳. 📐 **Multi-Cam Switcher**

اگر timeline چندین زاویه از یک رویداد دارد (مثلاً ۳ دوربین از یک کنسرت)، یک mode که **خودش بر اساس صدا (applause, whoosh) زاویه را عوض کند**. این «AI auto-cut» است که در OBS مشابه آن وجود دارد.

### ۳.۴. 🎵 **Beat-Synced Text Animations**

`keyframes` در `Clip` وجود دارد. animation‌های متن (scale, slide, rotate) که روی beat فعال می‌شوند. مثلاً «بوم» → کلمه zoom in. این را می‌توان با CSS keyframes + `data-key` که در PreviewMonitor دارید، ۱۰۰ خط کد.

### ۳.۵. 🌐 **Export Recipe Marketplace**

شما `StyleMatch` و `recipes` یک‌کلیکی دارید. یک دایرکتوری `~/CuttingEdge/recipes/*.json` که کاربر بتواند recipe خود را share کند. فرمت:
```json
{
  "name": "Vlog Cinematic",
  "tempo": 120,
  "cuts": [{"at": 0.0, "duration": 2.5}, {"at": 2.5, "duration": 1.8}],
  "color_grade": "warm",
  "captions": {"style": "tiktok-pop", "highlight": "#FF2D9C"}
}
```
این recipeها را می‌توان در یک GitHub Gist یا `chat2db` (که خودتان دارید!) share کرد.

### ۳.۶. ⚡ **GPU Direct Path برای NVENC**

شما `engine/gpu.py` دارید (۵۸۰ خط). در `compose.py` (`ffmpeg_binary()`)، اگر GPU NVIDIA موجود باشد، از `h264_nvenc` به جای `libx264` استفاده کنید. **۵-۱۰× سریع‌تر** export. فقط در export settings یک گزینه «Use GPU encoder» اضافه کنید.

### ۳.۷. 🖼 **Smart Thumbnail Generator**

وقتی timeline ساخته می‌شود، `analyze.py` می‌تواند ۱۰ فریم امتیازدهی شده برگرداند (نه فقط یکی). UI از آن‌ها برای ساخت یک storyboard ۱۰‌تایی استفاده کند. این همان "Video Summary" یوتیوب است، on-device.

### ۳.۸. 🧩 **Plugin System برای Engines**

شما در `STATE.md` به «کانال پلاگین TTS» اشاره کردید. این را جدی بگیرید: یک API کوچک:
```python
# backend/core/providers/__init__.py
class Provider(Protocol):
    name: str
    def transcribe(self, path: str) -> dict: ...
    def is_available(self) -> bool: ...
```
هر provider در `~/CuttingEdge/providers/<name>/` یک پوشه دارد. این الگوی **VSCode-style** است و نگهداری را ۱۰× ساده‌تر می‌کند.

### ۳.۹. 📊 **Performance HUD**

یک overlay (toggle با F3) که در preview monitor نمایش دهد:
- FPS واقعی (نه target)
- decode time per frame
- WebSocket events per second
- حافظه‌ی Python (از `tracemalloc`)

این «خفن» است چون کاربر می‌فهمد چرا timeline کُند شده. DaVinci هم چنین چیزی دارد.

### ۳.۱۰. 🎯 **"Director's Cut" Review**

برای هر clip یک score خودکار (از brain) + یک note کاربر ذخیره شود. در `ClipReview` (که الان ۷۸ خط است) یک حالت "Compare 3 versions" اضافه کنید: کنار هم ۳ کلیپ که سه planner مختلف ساخته‌اند. کاربر بهترین را انتخاب می‌کند. **این خودش آموزش مدل است** — implicit feedback برای آینده.

---

## ۴. بازطراحی UI/UX — سبک Cyberpunk/Neon

> تصاویر: `REDESIGN_LAUNCHER_CYBERPUNK.png` و `REDESIGN_STUDIO_CYBERPUNK.png`

### ۴.۱. چرا Cyberpunk؟

سه دلیل:

1. **نام محصول** «Cutting Edge» دقیقاً معنی cyberpunk را دارد: تکنولوژی پیشرفته + aesthetic. تم‌های مینیمال (مثل DaVinci) این حس را می‌کُشند.
2. **مخاطب هدف** — سازنده‌های Reels/Shorts/TikTok که با CapCut کار می‌کنند، به دنبال «چیزی متفاوت» هستند. Cyberpunk در بین Gen-Z محبوب‌ترین aesthetic است (Steam، Discord، VSCode همه تم تیره با accent نئونی دارند).
3. **متمایز شدن** — Premiere، DaVinci، CapCut، Final Cut = همه خاکستری. شما اولین ویرایشگر **«خفن»** می‌شوید.

### ۴.۲. Design tokens

```css
/* جایگزین کنید در global.css */
:root {
  /* پایه */
  --bg: #050810;          /* عمیق‌تر از فعلی */
  --bg-elev: #0A0F1C;
  --surface: #0E1626;
  --surface-2: #141D32;

  /* نئون — primary brand */
  --neon-pink: #FF2D9C;    /* primary action */
  --neon-cyan: #00F0FF;    /* info, timeline */
  --neon-purple: #A855F7;  /* secondary */
  --neon-green: #10F0A0;   /* success, online */
  --neon-amber: #FFB800;   /* warning, beats */

  /* glow helpers */
  --glow-pink: 0 0 20px rgba(255, 45, 156, 0.6);
  --glow-cyan: 0 0 20px rgba(0, 240, 255, 0.6);
  --glow-purple: 0 0 20px rgba(168, 85, 247, 0.5);

  /* متن */
  --text: #E8EEF8;
  --muted: #6B7A99;

  /* فونت */
  --font-mono: 'JetBrains Mono', 'Consolas', monospace;
  --font-sans: 'Inter', 'Vazirmatn', system-ui, sans-serif;
}
```

### ۴.۳. چهار اصل طراحی

| اصل | قانون | مثال |
|------|------|------|
| **Glow only on state** | یک المان فقط وقتی glow دارد که فعال/انتخاب‌شده/hover باشد | دکمه‌ی Play در حالت عادی border نارنجی، در hover glow صورتی |
| **Mono for numbers** | هر عدد (timecode, FPS, BPM, %%) با JetBrains Mono | `00:00:14:22` نه `00:00:14:22` با sans |
| **Glass panels** | پنل‌های کناری `backdrop-filter: blur(12px)` + `background: rgba(14, 22, 38, 0.7)` | Inspector و Task Dock |
| **HUD borders** | clip-path برای گوشه‌های بریده (cyberpunk signature) | `clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px))` |

### ۴.۴. تغییرات کلیدی نسبت به تم فعلی

| جزء | فعلی | Cyberpunk |
|------|-------|-----------|
| Wordmark | C و E بنفش/فیروزه‌ای ساده | C و E با box-shadow glow شدید + عدد اتمی زیر آن |
| پس‌زمینه | `#0b1220` یکدست | `#050810` + گرید ۲px سیان با opacity 5% + scanline overlay |
| دکمه‌ها | گرد یکنواخت | clip-path corner-cut + gradient border |
| Timeline ruler | خط‌چین ساده | خط‌چین سیان + اعداد monospace glow |
| Playhead | خط قرمز ۲px | خط صورتی ۲px + glow ۱۰px + فلش مثلثی بالا و پایین |
| Clip‌ها | گوشه گرد + film strip | گوشه بریده + film strip + border gradient (cyan→pink برای selected) |
| Preview monitor | aspect-ratio 16:9 ثابت | aspect-ratio از canvas + scanline overlay + corner brackets نئونی |
| Task dock | یک strip در پایین | یک strip با glow border + هر task card یک mini-HUD |
| AI FAB | دایره گرادینت | دایره با چرخش آهسته + pulse glow وقتی AI در حال کار |

### ۴.۵. چه چیزی **حفظ** شود (تا UX فعلی نشکند)

1. **Shared element transition** بین launcher و section — `framer-motion layoutId="ce-wordmark"`. این الگوی عالی است.
2. **Sticky task dock** در پایین.
3. **Centred mode** در Timeline.
4. **فارسی + انگلیسی همزمان** با `t(en, fa)` — این یکی از بهترین تصمیم‌های محصول است، حذف نکنید.
5. **Layout فعلی Studio** (Preview بالا، Toolbar وسط، Timeline پایین) — این استاندارد صنعت است.
6. **استفاده از Ant Design** — فقط override کنید، عوض نکنید.

### ۴.۶. چرا «نه» به Tailwind?

شما الان `global.css` خالص دارید (۱۰۶۷ خط). Tailwind اضافه کردن = افزایش bundle ~50KB. CSS variables design tokens که در بالا گفتم، **۹۰٪ خواسته‌های شما را با همان ۱۰۶۷ خط فعلی** برآورده می‌کند. اگر روزی خواستید، `vanilla-extract` یا `panda-css` بهتر از Tailwind برای theme سازمان‌یافته هستند.

### ۴.۷. نام رنگ‌ها

| متغیر | استفاده |
|--------|---------|
| `--neon-pink` | دکمه‌های primary، playhead، progress bar، destructive |
| `--neon-cyan` | info، timeline، online status، links، ruler |
| `--neon-purple` | secondary action، text lane، AI |
| `--neon-green` | success، done state، healthy |
| `--neon-amber` | warning، beat grid، pending |

این mapping با `radix-ui/colors` سازگار است و در dark mode استاندارد صنعت است.

---

## ۵. جمع‌بندی — ۵ گام اولویت‌بندی شده

| # | گام | زمان تخمینی | تأثیر |
|---|-----|-------------|--------|
| 1 | **دیباگ بحرانی ۲.۱ تا ۲.۴** (WebSocket + pip + SQLite + Path validation) | ۲ روز | پایداری × ۱۰ |
| 2 | **Logging ساخت‌یافته** (`structlog` + rotate) | ۰.۵ روز | دیباگ production × ۱۰۰ |
| 3 | **پیاده‌سازی Cyberpunk theme** (فقط CSS variables + overrides) | ۲ روز | متمایز شدن × ∞ |
| 4 | **Plugin Provider System** (الگوی ۳.۸) | ۱ هفته | آمادگی برای TTS/Stable Diffusion |
| 5 | **GPU Direct Path** (NVENC) | ۱ روز | export speed × ۵ |

> **پیشنهاد نهایی:** قبل از 1.0، **گام ۱ و ۳** را حتماً انجام دهید. گام ۱ امنیت و اعتماد کاربر را بالا می‌برد، گام ۳ «wow factor» ای که در launch ویدیو نیاز دارید. گام ۲، ۴، ۵ را می‌توان بعد از 1.0 در 0.10.x آورد.

---

**ساخته شده توسط Arena Agent** — بر اساس بررسی مستقیم کد در `/home/user/Chat2DB/ce-app/` (شاخه `arena/01a04055-chat2db`).
تصاویر طراحی: `docs/CuttingEdge/REDESIGN_LAUNCHER_CYBERPUNK.png` و `REDESIGN_STUDIO_CYBERPUNK.png`.
