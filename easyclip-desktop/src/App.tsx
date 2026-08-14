import { useEffect, useMemo, useRef, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import { open, save } from "@tauri-apps/plugin-dialog";
import Autopilot from "./Autopilot";
import {
  BarChart3,
  Captions,
  Check,
  ChevronLeft,
  CircleUserRound,
  Clapperboard,
  Cpu,
  Download,
  FileText,
  FileVideo,
  FolderOpen,
  Gauge,
  Languages,
  LayoutDashboard,
  MonitorPlay,
  Play,
  Plus,
  Radio,
  Scissors,
  Settings,
  Sparkles,
  Upload,
  WandSparkles,
  Youtube,
  Zap,
} from "lucide-react";

type Language = "fa" | "en";
type CaptionLanguage = Language | "auto";
type Page = "home" | "projects" | "editor" | "youtube" | "analytics" | "settings";
type SystemProfile = { os: string; arch: string; nvidia_available: boolean; gpu_name?: string; ffmpeg_available: boolean; whisper_available: boolean; model_available: boolean };
type VideoInfo = { name: string; path: string; size_bytes: number; extension: string; duration_seconds: number; width: number; height: number; codec: string };
type Project = { id: number; name: string; path: string; status: "ready" | "draft"; createdAt: string; duration: number; width: number; height: number; codec: string };
type CaptionSegment = { index: number; startMs: number; endMs: number; text: string };
type TranscriptionResult = { subtitlePath: string; language: CaptionLanguage; durationSeconds: number; segments: CaptionSegment[] };
type TranscriptionProgress = { jobId: string; stage: "extracting" | "transcribing" | "writing" | "complete"; progress: number };

const copy = {
  fa: {
    appName: "ایزی‌کلیپ",
    appSub: "استودیوی هوشمند ویدیو",
    home: "خانه",
    projects: "پروژه‌ها",
    youtube: "یوتیوب",
    analytics: "آمار",
    settings: "تنظیمات",
    badge: "پردازش کاملاً محلی",
    title1: "یک ویدیو،",
    title2: "ده‌ها کلیپ تماشایی.",
    subtitle: "هوش مصنوعی محلی بهترین لحظه‌ها را پیدا می‌کند، زیرنویس می‌سازد و خروجی عمودی آماده انتشار تحویل می‌دهد.",
    import: "انتخاب ویدیو",
    connect: "اتصال کانال یوتیوب",
    privacy: "ویدیوهای شما از کامپیوتر خارج نمی‌شوند",
    pipeline: "خط تولید هوشمند",
    pipelineSub: "از ویدیوی خام تا Shorts آماده انتشار",
    allLocal: "همه مراحل روی دستگاه شما",
    transcript: "زیرنویس دقیق",
    transcriptSub: "Whisper فارسی و انگلیسی",
    moments: "لحظات برتر",
    momentsSub: "امتیازدهی وایرال با AI",
    reframe: "کادر عمودی",
    reframeSub: "دنبال‌کردن خودکار چهره",
    render: "خروجی سریع",
    renderSub: "رندر NVIDIA با FFmpeg",
    recent: "پروژه‌های اخیر",
    empty: "اولین ویدیوی خود را اضافه کنید",
    emptySub: "فرمت‌های MP4، MOV، MKV و WebM پشتیبانی می‌شوند.",
    ready: "آماده پردازش",
    draft: "پیش‌نویس",
    open: "باز کردن",
    system: "وضعیت سیستم",
    checking: "در حال بررسی…",
    nvidia: "شتاب‌دهی NVIDIA",
    detected: "فعال و آماده",
    notDetected: "شناسایی نشد؛ حالت CPU استفاده می‌شود",
    apTitle: "خلبان خودکار یوتیوب",
    apLoading: "در حال بارگذاری…",
    apAccount: "حساب گوگل شما",
    apAccountSub: "ویدیوها در کانال خودِ شما منتشر می‌شوند",
    apClientId: "شناسه کلاینت (Client ID)",
    apClientSecret: "رمز کلاینت (Client secret)",
    apSaveCredentials: "ذخیره اطلاعات",
    apCredentialsSaved: "اطلاعات ذخیره شد",
    apEditCredentials: "ویرایش اطلاعات",
    apSignIn: "ورود با گوگل",
    apWaitingBrowser: "منتظر مرورگر…",
    apConnectedAs: "متصل شد به",
    apDisconnect: "قطع اتصال",
    apSubscribers: "دنبال‌کننده",
    apVideos: "ویدیو",
    apGuideTitle: "چطور Client ID بسازم؟",
    apGuide1: "به console.cloud.google.com بروید و یک پروژه بسازید.",
    apGuide2: "از بخش Library، سرویس YouTube Data API v3 را فعال کنید.",
    apGuide3: "در OAuth consent screen نوع External را بزنید و ایمیل خودتان را در Test users اضافه کنید.",
    apGuide4: "از Credentials یک OAuth client ID از نوع Desktop app بسازید.",
    apGuide5: "توجه: تا وقتی برنامه در حالت Testing است، هر ۷ روز باید دوباره وارد شوید.",
    apUploadsLeft: "آپلود باقی‌مانده امروز",
    apQuotaNote: "هر آپلود ۱۶۰۰ واحد از سهمیه ۱۰٬۰۰۰ واحدی روزانه مصرف می‌کند؛ یعنی حدود ۶ آپلود در روز. سهمیه نیمه‌شب به وقت اقیانوس آرام صفر می‌شود.",
    apSource: "کانال مبدأ",
    apSourceSub: "لینک ویدیو یا کانال را بچسبانید",
    apLoad: "خواندن",
    apVideosFound: "ویدیو پیدا شد",
    apOwnChannel: "کانال خودتان",
    apFilter: "جستجو در عنوان‌ها…",
    apSelectAll: "انتخاب همه",
    apClear: "پاک کردن",
    apCcLicence: "کریتیو کامانز",
    apStdLicence: "لایسنس استاندارد",
    apWarnTitle: "هشدار جدی درباره کپی‌رایت",
    apWarnBody: "بازنشر ویدیوی دیگران بدون اجازه، استرایک کپی‌رایت می‌گیرد. سه استرایک در ۹۰ روز یعنی حذف دائمی کانال و تمام ویدیوها. دانلود ویدیوی دیگران هم خلاف شرایط خدمات یوتیوب است.",
    apWarnAccept: "این محتوا متعلق به من است یا اجازه کتبی از صاحب اثر دارم.",
    apPrivacy: "وضعیت انتشار",
    apPrivate: "خصوصی",
    apUnlisted: "لینک‌دار",
    apPublic: "عمومی",
    apTitleTemplate: "الگوی عنوان",
    apAddToQueue: "افزودن به صف",
    apQueued: "ویدیو به صف اضافه شد",
    apSelectSomething: "اول چند ویدیو را انتخاب کنید",
    apQueue: "صف پردازش",
    apJobs: "کار",
    apPause: "توقف",
    apResume: "ادامه",
    apDryRun: "اجرای آزمایشی (بدون آپلود)",
    apDryRunDone: "اجرای آزمایشی کامل شد؛ چیزی آپلود نشد",
    apUploadDone: "آپلود کامل شد",
    apRun: "اجرا",
    apRetry: "تلاش دوباره",
    apSelfTest: "بررسی سلامت",
    apNoYtDlp: "ابزار yt-dlp پیدا نشد. برنامه را دوباره نصب کنید.",
    pending: "در انتظار",
    downloading: "در حال دانلود",
    clipping: "در حال کلیپ‌سازی",
    uploading: "در حال آپلود",
    done: "انجام شد",
    failed: "ناموفق",
    skipped: "رد شد",
    phase: "نسخه ۰.۲ محلی",
    phaseText: "FFmpeg، مدل چندزبانه Whisper و رندر زیرنویس فارسی و انگلیسی همراه برنامه آماده‌اند.",
    lang: "EN",
    local: "LOCAL",
    editor: "ویرایش و خروجی",
    start: "شروع کلیپ (ثانیه)",
    end: "پایان کلیپ (ثانیه)",
    captionsFile: "فایل زیرنویس SRT از تایم‌لاین اصلی (اختیاری)",
    chooseCaptions: "انتخاب زیرنویس UTF-8",
    captionStudio: "زیرنویس خودکار",
    captionStudioSub: "تبدیل گفتار به زیرنویس کاملاً آفلاین با whisper.cpp",
    captionLanguage: "زبان گفتار",
    persian: "فارسی",
    english: "English",
    automatic: "تشخیص خودکار",
    generateCaptions: "ساخت زیرنویس SRT",
    generatingCaptions: "در حال ساخت زیرنویس…",
    extracting: "استخراج صدای ویدیو",
    transcribing: "تشخیص گفتار روی دستگاه",
    writing: "ذخیره زیرنویس SRT",
    complete: "زیرنویس آماده است",
    captionReady: "زیرنویس تولید و برای رندر انتخاب شد",
    captionError: "ساخت زیرنویس ناموفق بود",
    captionHint: "مدل چندزبانه Base همراه برنامه نصب می‌شود؛ هیچ فایل یا صدایی آپلود نمی‌شود.",
    segments: "قطعه زیرنویس",
    enginesReady: "FFmpeg + Whisper آماده",
    enginesMissing: "موتورهای محلی ناقص‌اند؛ برنامه را دوباره نصب کنید",
    renderClip: "ساخت کلیپ عمودی با زیرنویس",
    rendering: "در حال رندر با FFmpeg…",
    rendered: "کلیپ با موفقیت ساخته شد",
    renderError: "ساخت کلیپ ناموفق بود",
    videoInfo: "مشخصات ویدیو",
    back: "بازگشت به پروژه‌ها",
  },
  en: {
    appName: "EasyClip",
    appSub: "AI Video Studio",
    home: "Home",
    projects: "Projects",
    youtube: "YouTube",
    analytics: "Analytics",
    settings: "Settings",
    badge: "100% local processing",
    title1: "One video,",
    title2: "dozens of great clips.",
    subtitle: "Local AI finds the best moments, creates captions, and delivers vertical videos ready to publish.",
    import: "Choose video",
    connect: "Connect YouTube channel",
    privacy: "Your videos never leave your computer",
    pipeline: "Smart pipeline",
    pipelineSub: "From raw footage to publish-ready Shorts",
    allLocal: "Every step runs on your device",
    transcript: "Accurate captions",
    transcriptSub: "Persian & English Whisper",
    moments: "Best moments",
    momentsSub: "AI viral-score analysis",
    reframe: "Vertical framing",
    reframeSub: "Automatic face tracking",
    render: "Fast export",
    renderSub: "NVIDIA FFmpeg rendering",
    recent: "Recent projects",
    empty: "Add your first video",
    emptySub: "MP4, MOV, MKV and WebM are supported.",
    ready: "Ready to process",
    draft: "Draft",
    open: "Open",
    system: "System status",
    checking: "Checking…",
    nvidia: "NVIDIA acceleration",
    detected: "Active and ready",
    notDetected: "Not detected; CPU mode will be used",
    apTitle: "YouTube Autopilot",
    apLoading: "Loading…",
    apAccount: "Your Google account",
    apAccountSub: "Videos are published to your own channel",
    apClientId: "Client ID",
    apClientSecret: "Client secret",
    apSaveCredentials: "Save credentials",
    apCredentialsSaved: "Credentials saved",
    apEditCredentials: "Edit credentials",
    apSignIn: "Sign in with Google",
    apWaitingBrowser: "Waiting for the browser…",
    apConnectedAs: "Connected as",
    apDisconnect: "Disconnect",
    apSubscribers: "subscribers",
    apVideos: "videos",
    apGuideTitle: "How do I get a Client ID?",
    apGuide1: "Open console.cloud.google.com and create a project.",
    apGuide2: "In Library, enable the YouTube Data API v3.",
    apGuide3: "On the OAuth consent screen pick External and add your own account under Test users.",
    apGuide4: "Under Credentials create an OAuth client ID of type Desktop app.",
    apGuide5: "Note: while the app stays in Testing mode Google expires the sign-in every 7 days.",
    apUploadsLeft: "uploads left today",
    apQuotaNote: "Each upload costs 1600 of the 10,000 daily quota units, so roughly 6 uploads per day. The quota resets at midnight Pacific time.",
    apSource: "Source channel",
    apSourceSub: "Paste a video or channel link",
    apLoad: "Load",
    apVideosFound: "videos found",
    apOwnChannel: "Your own channel",
    apFilter: "Search titles…",
    apSelectAll: "Select all",
    apClear: "Clear",
    apCcLicence: "Creative Commons",
    apStdLicence: "Standard licence",
    apWarnTitle: "Serious copyright warning",
    apWarnBody: "Re-uploading someone else's videos without permission causes copyright strikes. Three strikes in 90 days permanently deletes the channel and every video on it. Downloading other people's videos also breaks YouTube's Terms of Service.",
    apWarnAccept: "I own this content or have written permission from the rights holder.",
    apPrivacy: "Privacy",
    apPrivate: "Private",
    apUnlisted: "Unlisted",
    apPublic: "Public",
    apTitleTemplate: "Title template",
    apAddToQueue: "Add to queue",
    apQueued: "videos added to the queue",
    apSelectSomething: "Select at least one video first",
    apQueue: "Queue",
    apJobs: "jobs",
    apPause: "Pause",
    apResume: "Resume",
    apDryRun: "Dry run (no upload)",
    apDryRunDone: "Dry run finished; nothing was uploaded",
    apUploadDone: "Upload complete",
    apRun: "Run",
    apRetry: "Retry",
    apSelfTest: "Self-test",
    apNoYtDlp: "yt-dlp is missing. Reinstall EasyClip Desktop.",
    pending: "Pending",
    downloading: "Downloading",
    clipping: "Clipping",
    uploading: "Uploading",
    done: "Done",
    failed: "Failed",
    skipped: "Skipped",
    phase: "Local AI · v0.2",
    phaseText: "Bundled FFmpeg, multilingual Whisper, and Persian/English caption rendering are ready offline.",
    lang: "فا",
    local: "LOCAL",
    editor: "Edit & export",
    start: "Clip start (seconds)",
    end: "Clip end (seconds)",
    captionsFile: "Source-timeline SRT captions (optional)",
    chooseCaptions: "Choose UTF-8 captions",
    captionStudio: "Automatic captions",
    captionStudioSub: "Offline speech-to-subtitles powered by whisper.cpp",
    captionLanguage: "Spoken language",
    persian: "فارسی",
    english: "English",
    automatic: "Auto detect",
    generateCaptions: "Generate SRT captions",
    generatingCaptions: "Generating captions…",
    extracting: "Extracting video audio",
    transcribing: "Transcribing locally",
    writing: "Saving the SRT file",
    complete: "Captions are ready",
    captionReady: "Captions generated and selected for rendering",
    captionError: "Caption generation failed",
    captionHint: "The multilingual Base model is installed with the app. No media or audio is uploaded.",
    segments: "caption segments",
    enginesReady: "FFmpeg + Whisper ready",
    enginesMissing: "Local engines are incomplete; reinstall the app",
    renderClip: "Create captioned vertical clip",
    rendering: "Rendering with FFmpeg…",
    rendered: "Clip created successfully",
    renderError: "Clip rendering failed",
    videoInfo: "Video details",
    back: "Back to projects",
  },
};

type Translation = (typeof copy)[Language];

const isTauri = () => "__TAURI_INTERNALS__" in window;

export default function App() {
  const [language, setLanguage] = useState<Language>(() => (localStorage.getItem("easyclip-language") as Language) || "fa");
  const [page, setPage] = useState<Page>("home");
  const [profile, setProfile] = useState<SystemProfile | null>(null);
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [projects, setProjects] = useState<Project[]>(() => {
    try { return JSON.parse(localStorage.getItem("easyclip-projects") || "[]"); } catch { return []; }
  });
  const fileInput = useRef<HTMLInputElement>(null);
  const t = copy[language];
  const rtl = language === "fa";

  useEffect(() => {
    document.documentElement.lang = language;
    document.documentElement.dir = rtl ? "rtl" : "ltr";
    localStorage.setItem("easyclip-language", language);
  }, [language, rtl]);

  useEffect(() => {
    if (isTauri()) {
      invoke<SystemProfile>("system_profile").then(setProfile).catch(() => setProfile({ os: "Windows", arch: "x64", nvidia_available: false, ffmpeg_available: false, whisper_available: false, model_available: false }));
    } else {
      setProfile({ os: "Windows 11", arch: "x64", nvidia_available: true, gpu_name: "NVIDIA GPU (preview)", ffmpeg_available: true, whisper_available: true, model_available: true });
    }
  }, []);

  const addProject = async (path: string, browserFile?: File) => {
    let info: VideoInfo;
    if (isTauri()) {
      info = await invoke<VideoInfo>("inspect_video", { path });
    } else {
      info = { name: browserFile?.name || path, path, size_bytes: browserFile?.size || 0, extension: path.split(".").pop() || "mp4", duration_seconds: 120, width: 1920, height: 1080, codec: "h264" };
    }
    const project: Project = { id: Date.now(), name: info.name, path: info.path, status: "ready", createdAt: new Date().toLocaleDateString(language === "fa" ? "fa-IR" : "en-US"), duration: info.duration_seconds, width: info.width, height: info.height, codec: info.codec };
    const next = [project, ...projects.filter((item) => item.path !== path)];
    setProjects(next);
    localStorage.setItem("easyclip-projects", JSON.stringify(next));
    setSelectedProject(project);
    setPage("editor");
  };

  const chooseVideo = async () => {
    if (!isTauri()) { fileInput.current?.click(); return; }
    const selected = await open({ multiple: false, title: t.import, filters: [{ name: "Video", extensions: ["mp4", "mov", "mkv", "webm", "avi", "m4v"] }] });
    if (typeof selected === "string") {
      try { await addProject(selected); } catch (error) { window.alert(String(error)); }
    }
  };

  const openProject = (project: Project) => {
    setSelectedProject(project);
    setPage("editor");
  };

  // Map the ap-prefixed translation keys onto the plain names Autopilot expects,
  // and pass the job-state labels through unchanged.
  const apCopy = useMemo(() => {
    const source = t as unknown as Record<string, string>;
    const out: Record<string, string> = {};
    for (const [key, value] of Object.entries(source)) {
      if (key.startsWith("ap") && key.length > 2 && key[2] === key[2].toUpperCase()) {
        out[key[2].toLowerCase() + key.slice(3)] = value;
      }
    }
    for (const key of ["pending", "downloading", "clipping", "uploading", "done", "failed", "skipped"]) {
      if (source[key]) out[key] = source[key];
    }
    return out;
  }, [t]);

  const nav = useMemo(() => [
    { id: "home" as Page, label: t.home, icon: LayoutDashboard },
    { id: "projects" as Page, label: t.projects, icon: Clapperboard },
    { id: "youtube" as Page, label: t.youtube, icon: Youtube },
    { id: "analytics" as Page, label: t.analytics, icon: BarChart3 },
    { id: "settings" as Page, label: t.settings, icon: Settings },
  ], [t]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand"><img src="/icon.png" /><div><strong>{t.appName}</strong><span>{t.appSub}</span></div></div>
        <nav>{nav.map(({ id, label, icon: Icon }) => <button key={id} className={page === id ? "active" : ""} onClick={() => setPage(id)}><Icon size={19}/><span>{label}</span></button>)}</nav>
        <div className="side-bottom">
          <div className="local-chip"><span className="pulse"/><div><b>{t.local}</b><small>{t.privacy}</small></div></div>
          <button className="profile"><CircleUserRound size={30}/><div><b>Creator</b><span>Windows 11</span></div><ChevronLeft size={16}/></button>
        </div>
      </aside>

      <main>
        <header><div className="status"><span className="status-dot"/>{t.badge}</div><button className="language" onClick={() => setLanguage(language === "fa" ? "en" : "fa")}><Languages size={17}/>{t.lang}</button></header>
        {page === "home" && <Home t={t} chooseVideo={chooseVideo} setPage={setPage} profile={profile} projects={projects} />}
        {page === "projects" && <Projects t={t} projects={projects} chooseVideo={chooseVideo} openProject={openProject} />}
        {page === "editor" && selectedProject && <Editor t={t} project={selectedProject} profile={profile} goBack={() => setPage("projects")} />}
        {page === "youtube" && <Autopilot t={apCopy} dir={language === "fa" ? "rtl" : "ltr"} />}
        {page !== "home" && page !== "projects" && page !== "editor" && page !== "youtube" && <ComingSoon page={page} t={t} profile={profile} />}
      </main>
      <input ref={fileInput} hidden type="file" accept="video/*" onChange={(e) => { const file = e.target.files?.[0]; if (file) void addProject(file.name, file); }} />
    </div>
  );
}

function Home({ t, chooseVideo, setPage, profile, projects }: { t: Translation; chooseVideo: () => void; setPage: (p: Page) => void; profile: SystemProfile | null; projects: Project[] }) {
  const stages = [
    { icon: Captions, title: t.transcript, sub: t.transcriptSub, tone: "violet", step: "01" },
    { icon: Sparkles, title: t.moments, sub: t.momentsSub, tone: "lime", step: "02" },
    { icon: MonitorPlay, title: t.reframe, sub: t.reframeSub, tone: "blue", step: "03" },
    { icon: Zap, title: t.render, sub: t.renderSub, tone: "orange", step: "04" },
  ];
  return <div className="content">
    <section className="hero">
      <div className="hero-copy"><div className="eyebrow"><WandSparkles size={15}/>{t.badge}</div><h1>{t.title1}<br/><span>{t.title2}</span></h1><p>{t.subtitle}</p><div className="hero-actions"><button className="primary" onClick={chooseVideo}><FolderOpen size={20}/>{t.import}</button><button className="secondary" onClick={() => setPage("youtube")}><Youtube size={20}/>{t.connect}</button></div><div className="privacy"><Check size={14}/>{t.privacy}</div></div>
      <div className="hero-visual"><div className="glow"/><div className="video-frame"><div className="frame-top"><span/><span/><span/></div><div className="portrait"><div className="play"><Play size={28} fill="currentColor"/></div><div className="caption-lines"><b>YOUR NEXT VIRAL MOMENT</b><span>شروع داستان از همین‌جاست</span></div></div><div className="timeline"><div className="wave"/><div className="cut cut-a"/><div className="cut cut-b"/><span className="playhead"/></div></div><div className="score"><Gauge size={18}/><div><small>VIRAL SCORE</small><b>92</b></div></div></div>
    </section>

    <section className="section-head"><div><h2>{t.pipeline}</h2><p>{t.pipelineSub}</p></div><span><Cpu size={16}/>{t.allLocal}</span></section>
    <section className="pipeline">{stages.map(({ icon: Icon, title, sub, tone, step }) => <article key={step} className={`stage ${tone}`}><div className="step">{step}</div><div className="stage-icon"><Icon size={24}/></div><h3>{title}</h3><p>{sub}</p></article>)}</section>

    <section className="lower-grid"><div className="recent-card"><div className="card-title"><div><h2>{t.recent}</h2><span>{projects.length}</span></div><button onClick={chooseVideo}><Plus size={17}/></button></div>{projects.length === 0 ? <button className="empty" onClick={chooseVideo}><div><Upload size={25}/></div><b>{t.empty}</b><span>{t.emptySub}</span></button> : projects.slice(0, 3).map(p => <div className="project-row" key={p.id}><div className="thumb"><FileVideo size={22}/></div><div><b>{p.name}</b><span>{p.createdAt}</span></div><span className="ready">{t.ready}</span></div>)}</div>
      <div className="system-card"><div className="card-title"><div><h2>{t.system}</h2></div><Cpu size={20}/></div><div className="gpu-icon"><Zap size={28}/></div><h3>{profile?.gpu_name || (profile ? "CPU" : t.checking)}</h3><p>{t.nvidia}</p><div className={`system-state ${profile?.nvidia_available ? "ok" : "warn"}`}><span/>{profile ? (profile.nvidia_available ? t.detected : t.notDetected) : t.checking}</div><div className="engine-badges"><span className={profile?.ffmpeg_available ? "ok" : ""}>FFmpeg</span><span className={profile?.whisper_available && profile?.model_available ? "ok" : ""}>Whisper.cpp</span></div><div className="phase-note"><b>{t.phase}</b><span>{t.phaseText}</span></div></div></section>
  </div>;
}

function Projects({ t, projects, chooseVideo, openProject }: { t: Translation; projects: Project[]; chooseVideo: () => void; openProject: (project: Project) => void }) {
  return <div className="content page"><div className="page-title"><div><span>LIBRARY</span><h1>{t.projects}</h1></div><button className="primary" onClick={chooseVideo}><Plus size={19}/>{t.import}</button></div>{projects.length === 0 ? <button className="large-empty" onClick={chooseVideo}><div><Scissors size={34}/></div><h2>{t.empty}</h2><p>{t.emptySub}</p></button> : <div className="project-grid">{projects.map(p => <article className="project-card" key={p.id}><div className="project-preview"><FileVideo size={35}/><span>9:16</span></div><div className="project-info"><h3>{p.name}</h3><p>{p.path}</p><div><span className="ready">{t.ready}</span><button onClick={() => openProject(p)}>{t.open}<ChevronLeft size={15}/></button></div></div></article>)}</div>}</div>;
}

function formatCaptionTime(milliseconds: number) {
  const totalSeconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${String(seconds).padStart(2, "0")}`;
}

function Editor({ t, project, profile, goBack }: { t: Translation; project: Project; profile: SystemProfile | null; goBack: () => void }) {
  const [start, setStart] = useState(0);
  const [end, setEnd] = useState(Math.min(project.duration || 60, 60));
  const [captionPath, setCaptionPath] = useState<string | null>(null);
  const [captionLanguage, setCaptionLanguage] = useState<CaptionLanguage>("fa");
  const [transcript, setTranscript] = useState<TranscriptionResult | null>(null);
  const [transcribing, setTranscribing] = useState(false);
  const [progress, setProgress] = useState<TranscriptionProgress | null>(null);
  const [rendering, setRendering] = useState(false);
  const [message, setMessage] = useState<{ ok: boolean; text: string } | null>(null);
  const activeJob = useRef<string | null>(null);

  useEffect(() => {
    setStart(0);
    setEnd(Math.min(project.duration || 60, 60));
    setCaptionPath(null);
    setTranscript(null);
    setProgress(null);
    setMessage(null);
  }, [project.path, project.duration]);

  useEffect(() => {
    if (!isTauri()) return;
    let disposed = false;
    let stopListening: (() => void) | undefined;
    void listen<TranscriptionProgress>("transcription-progress", ({ payload }) => {
      if (payload.jobId === activeJob.current) setProgress(payload);
    }).then((unlisten) => {
      if (disposed) unlisten(); else stopListening = unlisten;
    });
    return () => { disposed = true; stopListening?.(); };
  }, []);

  const chooseCaptions = async () => {
    if (!isTauri()) return;
    const selected = await open({ multiple: false, filters: [{ name: "SubRip captions (UTF-8)", extensions: ["srt"] }] });
    if (typeof selected === "string") {
      setCaptionPath(selected);
      setTranscript(null);
      setMessage(null);
    }
  };

  const generateCaptions = async () => {
    const baseName = project.name.replace(/\.[^.]+$/, "");
    const jobId = `captions-${Date.now()}`;
    activeJob.current = jobId;
    setTranscribing(true);
    setProgress({ jobId, stage: "extracting", progress: 4 });
    setMessage(null);

    if (!isTauri()) {
      const previewText = captionLanguage === "en" ? "Your next story starts right here." : "داستان بعدی شما از همین‌جا شروع می‌شود.";
      const preview: TranscriptionResult = {
        subtitlePath: `${baseName}-${captionLanguage}.srt`,
        language: captionLanguage,
        durationSeconds: 6.2,
        segments: [
          { index: 1, startMs: 0, endMs: 3100, text: previewText },
          { index: 2, startMs: 3200, endMs: 6200, text: captionLanguage === "en" ? "Everything stays on your device." : "همه‌چیز روی دستگاه شما می‌ماند." },
        ],
      };
      setTranscript(preview);
      setCaptionPath(preview.subtitlePath);
      setProgress({ jobId, stage: "complete", progress: 100 });
      setMessage({ ok: true, text: t.captionReady });
      setTranscribing(false);
      return;
    }

    const outputPath = await save({
      defaultPath: `${baseName}-${captionLanguage}.srt`,
      filters: [{ name: "SubRip captions", extensions: ["srt"] }],
    });
    if (!outputPath) {
      setTranscribing(false);
      setProgress(null);
      return;
    }

    try {
      const result = await invoke<TranscriptionResult>("generate_subtitles", {
        request: { inputPath: project.path, outputPath, language: captionLanguage, jobId },
      });
      setTranscript(result);
      setCaptionPath(result.subtitlePath);
      setMessage({ ok: true, text: `${t.captionReady} · ${result.segments.length} ${t.segments}` });
    } catch (error) {
      setMessage({ ok: false, text: `${t.captionError}: ${String(error)}` });
      setProgress(null);
    } finally {
      setTranscribing(false);
    }
  };

  const render = async () => {
    if (!isTauri()) { setMessage({ ok: false, text: "Rendering is available in the installed Windows app." }); return; }
    const baseName = project.name.replace(/\.[^.]+$/, "");
    const outputPath = await save({ defaultPath: `${baseName}-vertical.mp4`, filters: [{ name: "MP4 video", extensions: ["mp4"] }] });
    if (!outputPath) return;
    setRendering(true);
    setMessage(null);
    try {
      const result = await invoke<{ outputPath: string; usedNvidia: boolean }>("render_vertical_clip", {
        request: { inputPath: project.path, outputPath, startSeconds: start, endSeconds: end, captionPath, useNvidia: profile?.nvidia_available ?? false },
      });
      setMessage({ ok: true, text: `${t.rendered}: ${result.outputPath}${result.usedNvidia ? " · NVIDIA NVENC" : " · CPU"}` });
    } catch (error) {
      setMessage({ ok: false, text: `${t.renderError}: ${String(error)}` });
    } finally {
      setRendering(false);
    }
  };

  const runtimeReady = Boolean(profile?.ffmpeg_available && profile.whisper_available && profile.model_available);
  const runtimeLabel = !profile ? t.checking : runtimeReady ? t.enginesReady : t.enginesMissing;
  const progressLabel = progress ? t[progress.stage] : t.generatingCaptions;

  return <div className="content page editor-page">
    <button className="back-button" onClick={goBack}><ChevronLeft size={17}/>{t.back}</button>
    <div className="page-title"><div><span>LOCAL AI · VERTICAL 9:16</span><h1>{t.editor}</h1></div><div className={`engine-pill ${runtimeReady ? "ready" : "missing"}`}><span/>{runtimeLabel}</div></div>
    <div className="editor-grid">
      <section className="editor-preview"><div className="preview-phone"><FileVideo size={50}/><b>{project.name}</b><span>1080 × 1920</span>{transcript && <div className="phone-caption">{transcript.segments[0]?.text}</div>}</div></section>
      <section className="editor-controls">
        <div className="info-panel"><h3>{t.videoInfo}</h3><div><span>{project.width} × {project.height}</span><span>{project.codec.toUpperCase()}</span><span>{Math.round(project.duration)}s</span></div></div>
        <div className="range-row"><label>{t.start}<input type="number" min="0" max={end - 1} step="0.5" value={start} onChange={(e) => setStart(Number(e.target.value))}/></label><label>{t.end}<input type="number" min={start + 1} max={project.duration || 180} step="0.5" value={end} onChange={(e) => setEnd(Number(e.target.value))}/></label></div>
        <div className="duration-bar"><span style={{ width: `${Math.min(100, ((end - start) / Math.max(project.duration, 1)) * 100)}%` }}/></div>

        <div className="caption-studio">
          <div className="caption-studio-head"><div className="caption-studio-icon"><FileText size={20}/></div><div><h3>{t.captionStudio}</h3><p>{t.captionStudioSub}</p></div></div>
          <label className="caption-language-label">{t.captionLanguage}</label>
          <div className="caption-languages">
            {(["fa", "en", "auto"] as CaptionLanguage[]).map((value) => <button key={value} className={captionLanguage === value ? "active" : ""} disabled={transcribing} onClick={() => setCaptionLanguage(value)}>{value === "fa" ? t.persian : value === "en" ? t.english : t.automatic}</button>)}
          </div>
          <button className="generate-captions" disabled={transcribing || !runtimeReady} onClick={generateCaptions}>{transcribing ? <><span className="spinner"/>{t.generatingCaptions}</> : <><Sparkles size={18}/>{t.generateCaptions}</>}</button>
          {(transcribing || progress) && <div className="transcription-progress"><div><span>{progressLabel}</span><b>{progress?.progress ?? 0}%</b></div><div className="progress-track"><span style={{ width: `${progress?.progress ?? 0}%` }}/></div></div>}
          <p className="caption-hint"><Check size={13}/>{t.captionHint}</p>
          {transcript && <div className="transcript-preview"><div className="transcript-summary"><b>{transcript.segments.length} {t.segments}</b><span>{transcript.subtitlePath}</span></div>{transcript.segments.slice(0, 3).map((segment) => <div className="transcript-segment" key={segment.index}><time>{formatCaptionTime(segment.startMs)}</time><p dir="auto">{segment.text}</p></div>)}</div>}
        </div>

        <button className="caption-picker" disabled={transcribing} onClick={chooseCaptions}><Captions size={19}/><div><b>{t.captionsFile}</b><span>{captionPath || t.chooseCaptions}</span></div></button>
        <div className="render-engine"><Zap size={18}/><div><b>{profile?.nvidia_available ? profile.gpu_name : "CPU / libx264"}</b><span>{profile?.nvidia_available ? "NVIDIA NVENC" : "Software encoder"}</span></div><Check size={17}/></div>
        <button className="primary render-button" disabled={rendering || transcribing || !profile?.ffmpeg_available} onClick={render}>{rendering ? <><span className="spinner"/>{t.rendering}</> : <><Download size={20}/>{t.renderClip}</>}</button>
        {message && <div className={`render-message ${message.ok ? "success" : "error"}`}>{message.ok ? <Check size={17}/> : <span>!</span>}<p>{message.text}</p></div>}
      </section>
    </div>
  </div>;
}

function ComingSoon({ page, t, profile }: { page: Page; t: Translation; profile: SystemProfile | null }) {
  const Icon = page === "youtube" ? Youtube : page === "analytics" ? BarChart3 : Settings;
  return <div className="content page"><div className="coming"><div><Icon size={36}/></div><span>{t.phase}</span><h1>{page === "youtube" ? t.connect : page === "analytics" ? t.analytics : t.settings}</h1><p>{t.phaseText}</p>{page === "settings" && <div className="spec"><Cpu size={18}/><b>{profile?.gpu_name || "NVIDIA / CPU"}</b><span>{profile?.os} · {profile?.arch}</span></div>}</div></div>;
}
