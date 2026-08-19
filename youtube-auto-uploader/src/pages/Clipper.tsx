import { useCallback, useEffect, useRef, useState } from 'react';
import { Bot, Captions, Check, ChevronDown, Download, FileAudio, FileVideo, Layers3, Loader2, Pause, Play, Plus, Scissors, SlidersHorizontal, Sparkles, Trash2, Upload, WandSparkles, ZoomIn, ZoomOut } from 'lucide-react';
import { toast } from 'sonner';
import type { AnalysisMode } from '../../electron/types';
import type { ClipRow } from '../global';

const recommended = ['qwen2.5:7b-instruct-q4_0', 'llama3.1:8b-instruct', 'gemma2:9b-instruct'];

export function Clipper(): JSX.Element {
  const [url, setUrl] = useState('');
  const [file, setFile] = useState<string>();
  const [running, setRunning] = useState(false);
  const [models, setModels] = useState<string[]>([]);
  const [ollamaRunning, setOllamaRunning] = useState(false);
  const [model, setModel] = useState(recommended[0] ?? '');
  const [localEngine, setLocalEngine] = useState<{ available: boolean; cudaAvailable: boolean; error?: string }>({ available: false, cudaAvailable: false });
  const [analysisMode, setAnalysisMode] = useState<AnalysisMode>('hybrid');
  const [profile, setProfile] = useState<'fast'|'balanced'|'professional'>('balanced');
  const [whisperModel, setWhisperModel] = useState('base');
  const [localModels, setLocalModels] = useState<Array<{name:string;installed:boolean;sizeBytes:number}>>([]);
  const [modelBusy, setModelBusy] = useState(false);
  const [language, setLanguage] = useState<'auto' | 'fa' | 'en'>('auto');
  const [count, setCount] = useState(5);
  const [maxLength, setMaxLength] = useState(60);
  const [category, setCategory] = useState('Auto');
  const [aspect, setAspect] = useState('9:16');
  const [captions, setCaptions] = useState(true);
  const [smartZoom, setSmartZoom] = useState(true);
  const [music, setMusic] = useState(false);
  const [blurBackground, setBlurBackground] = useState(true);
  const [pull, setPull] = useState<{ percent: number; status: string }>();
  const [progress, setProgress] = useState<{ phase: string; percent: number; message?: string }>();
  const [clips, setClips] = useState<ClipRow[]>([]);
  const [speakerTimeline, setSpeakerTimeline] = useState<{speakers:string[];turns:Array<{speaker:string;start_seconds:number;end_seconds:number}>}>();
  const [faceTrackCount, setFaceTrackCount] = useState(0);
  const activeJobId = useRef<string | undefined>(undefined);

  const load = useCallback((): void => { void window.api.clipper.clips().then(setClips); }, []);
  const checkEngines = useCallback(async (): Promise<void> => {
    const [ollama, local, inventory] = await Promise.all([window.api.ollama.status(), window.api.localAI.status(), window.api.localAI.models().catch(() => [])]);
    setOllamaRunning(ollama.running);
    setModels(ollama.models);
    setLocalEngine(local);
    setLocalModels(inventory);
    if (ollama.models[0] && !ollama.models.includes(model)) setModel(ollama.models[0]);
  }, [model]);

  useEffect(() => {
    void checkEngines();
    load();
    void window.api.clipper.job().then((job) => {
      if (!job || job.status !== 'running') return;
      activeJobId.current = job.jobId;
      setRunning(true);
      setProgress({ phase: job.phase, percent: job.percent, message: job.message });
    });
    const progressUnsubscribe = window.api.on('job:progress', (value) => {
      const update = value as { jobId: string; phase: string; percent: number; message?: string };
      if (activeJobId.current && update.jobId !== activeJobId.current) return;
      setProgress(update);
    });
    const clipUnsubscribe = window.api.on('clip:ready', load);
    const speakerUnsubscribe = window.api.on('speaker:timeline', (value) => setSpeakerTimeline(value as {speakers:string[];turns:Array<{speaker:string;start_seconds:number;end_seconds:number}>}));
    const faceUnsubscribe = window.api.on('face:timeline', (value) => setFaceTrackCount((value as {trackCount:number}).trackCount));
    const pullUnsubscribe = window.api.on('ollama:pull-progress', (value) => setPull(value as { percent: number; status: string }));
    const doneUnsubscribe = window.api.on('job:done', (value) => {
      const result = value as { jobId: string; error?: string };
      if (activeJobId.current && result.jobId !== activeJobId.current) return;
      activeJobId.current = undefined;
      setRunning(false); load();
      if (result.error) toast.error(result.error); else toast.success('Highlight clips are ready');
    });
    return () => { progressUnsubscribe(); clipUnsubscribe(); speakerUnsubscribe(); faceUnsubscribe(); pullUnsubscribe(); doneUnsubscribe(); };
  }, [checkEngines, load]);

  const applyProfile = (next: 'fast'|'balanced'|'professional'): void => {
    setProfile(next);
    if (next === 'fast') { setWhisperModel('tiny'); setAnalysisMode('local'); setSmartZoom(false); setMaxLength(30); }
    if (next === 'balanced') { setWhisperModel('base'); setAnalysisMode('hybrid'); setSmartZoom(true); setMaxLength(60); }
    if (next === 'professional') { setWhisperModel('large-v3'); setAnalysisMode('hybrid'); setSmartZoom(true); setCaptions(true); setBlurBackground(true); setMaxLength(90); }
  };

  const toggleWhisperModel = async (): Promise<void> => {
    const current = localModels.find((item) => item.name === whisperModel);
    setModelBusy(true);
    try {
      const inventory = current?.installed
        ? await window.api.localAI.deleteModel(whisperModel)
        : await window.api.localAI.prepareModel(whisperModel);
      setLocalModels(inventory);
      toast.success(current?.installed ? 'Speech model removed' : 'Speech model is ready');
    } catch (error: unknown) { toast.error(error instanceof Error ? error.message : String(error)); }
    finally { setModelBusy(false); }
  };

  const cancel = async (): Promise<void> => {
    if (!activeJobId.current) return;
    await window.api.clipper.cancel(activeJobId.current);
    setRunning(false);
    toast.info('Cancellation requested');
  };

  const start = async (): Promise<void> => {
    if (!localEngine.available) { toast.error(localEngine.error || 'The local Whisper engine is not installed'); return; }
    if (analysisMode === 'ollama' && !ollamaRunning) { toast.error('Start Ollama before clipping'); return; }
    if (analysisMode === 'ollama' && !models.includes(model)) { toast.error('Install the selected Ollama model first'); return; }
    if (!url && !file) { toast.error('Choose a YouTube URL or local video'); return; }
    try {
      setRunning(true);
      const handle = await window.api.clipper.start({ url: url || undefined, localPath: file, model, whisperModel, language, analysisMode, processingProfile: profile, count, maxLength, category, aspect, captions, smartZoom, music, blurBackground });
      activeJobId.current = handle.jobId;
      toast.success('Clipping continues in the background when you change pages');
    } catch (error: unknown) {
      setRunning(false);
      toast.error(error instanceof Error ? error.message : String(error));
    }
  };

  const pullModel = async (): Promise<void> => {
    try { await window.api.ollama.pull(model); await checkEngines(); toast.success('Model installed'); }
    catch (error: unknown) { toast.error(error instanceof Error ? error.message : String(error)); }
  };

  const approveAll = async (): Promise<void> => {
    await Promise.all(clips.filter((clip) => clip.status === 'pending').map((clip) => window.api.clipper.update(clip.id, { status: 'approved' })));
    load();
  };

  const uploadApproved = async (): Promise<void> => {
    const approved = clips.filter((clip) => clip.status === 'approved');
    await Promise.all(approved.map((clip) => window.api.clipper.upload(clip.id)));
    toast.success(`${String(approved.length)} clips queued`);
    load();
  };

  const preview = clips[0];
  const formatSize = (bytes: number): string => bytes ? `${(bytes / 1_048_576).toFixed(0)} MB` : 'Not installed';
  return <div className="editor-page">
    <div className="editor-commandbar">
      <div className="project-title"><b>{file?.split(/[\\/]/).pop() ?? 'Untitled AI project'}</b><span>{file ? 'Local media · autosaved' : 'Import media to begin'}</span></div>
      <div className="profile-switch">{(['fast','balanced','professional'] as const).map((name)=><button key={name} className={profile===name?'active':''} onClick={()=>applyProfile(name)}>{{fast:'Fast',balanced:'Balanced',professional:'Professional'}[name]}</button>)}</div>
      <button className="btn !py-2 flex items-center gap-2"><SlidersHorizontal size={14}/> Project <ChevronDown size={12}/></button>
      <button className="btn btn-primary !py-2 flex items-center gap-2" disabled={!clips.length} onClick={()=>void uploadApproved()}><Upload size={14}/> Export</button>
    </div>

    <div className="editor-workspace">
      <aside className="asset-panel">
        <div className="asset-tabs"><button><FileVideo size={15}/><span>Media</span></button><button><FileAudio size={15}/><span>Audio</span></button><button><Captions size={15}/><span>Text</span></button><button><Sparkles size={15}/><span>AI</span></button></div>
        <div className="panel-heading"><span>Project media</span><Plus size={14}/></div>
        <button className="import-zone w-[calc(100%-24px)]" onClick={()=>void window.api.settings.pickFile().then((value)=>value&&setFile(value))}><div><Plus className="mx-auto text-violet-400" size={24}/><b className="block text-zinc-300 text-[11px] mt-2">Import video</b><span className="text-[9px]">or drop media here</span></div></button>
        <label className="block px-3"><span className="label">Online source</span><input className="input text-[10px]" value={url} onChange={(event)=>setUrl(event.target.value)} placeholder="Paste video URL"/></label>
        {(file||url)&&<div className="source-card"><div className="aspect-video rounded bg-gradient-to-br from-violet-950 to-slate-900 grid place-items-center"><FileVideo className="text-violet-400" size={24}/></div><b className="mt-2">{file?.split(/[\\/]/).pop()??'Online video'}</b><span>Ready for analysis</span></div>}
        <div className="panel-heading mt-3"><span>AI engines</span><span className="engine-dot"/></div>
        <div className="engine-strip"><span className="engine-dot"/><span className="text-[9px] text-zinc-400">Speech · {localEngine.cudaAvailable?'GPU':'CPU'}</span></div>
        <div className="engine-strip"><span className={`engine-dot ${ollamaRunning?'':'!bg-amber-500'}`}/><span className="text-[9px] text-zinc-400">Language model · {ollamaRunning?'Ready':'Optional'}</span></div><div className="engine-strip"><span className={`engine-dot ${faceTrackCount?'':'!bg-violet-500'}`}/><span className="text-[9px] text-zinc-400">Face tracks · {faceTrackCount||'Professional'}</span></div>
      </aside>

      <section className="viewer-column">
        <div className="viewer-stage"><div className="viewer-canvas">{preview?<video src={`media://file?path=${encodeURIComponent(preview.local_path)}`} poster={`media://file?path=${encodeURIComponent(preview.thumbnail_path)}`}/>:<div className="viewer-empty"><WandSparkles className="mx-auto" size={37}/><b>Your preview appears here</b><span className="text-[9px]">AI framing · {aspect}</span></div>}<div className="safe-zone"/></div></div>
        <div className="viewer-controls"><button><ZoomOut size={14}/></button><span className="text-[9px]">42%</span><button><ZoomIn size={14}/></button><time>00:00:00</time><button className="play">{running?<Pause size={13}/>:<Play size={13} fill="currentColor"/>}</button><time>{preview?`${Math.round(preview.end_time-preview.start_time)} sec`:'00:00:00'}</time><button><Layers3 size={14}/></button></div>
      </section>

      <aside className="inspector-panel">
        <div className="panel-heading"><span>AI inspector</span><WandSparkles className="text-violet-400" size={15}/></div>
        <div className="inspector-section"><h3>Processing</h3><div className="compact-grid"><label><span className="label">Analysis</span><select className="input" value={analysisMode} onChange={(e)=>setAnalysisMode(e.target.value as AnalysisMode)}><option value="local">Local</option><option value="hybrid">Hybrid</option><option value="ollama">Ollama</option></select></label><label><span className="label">Language</span><select className="input" value={language} onChange={(e)=>setLanguage(e.target.value as 'auto'|'fa'|'en')}><option value="auto">Auto</option><option value="fa">Persian</option><option value="en">English</option></select></label></div>{analysisMode!=='local'&&<div className="mt-3"><span className="label">Local language model</span><div className="flex gap-1"><select className="input text-[10px]" value={model} onChange={(e)=>setModel(e.target.value)}>{[...new Set([...models,...recommended])].map(name=><option key={name}>{models.includes(name)?'★ ':''}{name}</option>)}</select>{!models.includes(model)&&<button className="btn !px-2 text-[9px]" onClick={()=>void pullModel()}>Install</button>}</div>{pull&&<div className="progress mt-2"><div style={{width:`${pull.percent}%`}}/></div>}</div>}</div>
        <div className="inspector-section"><h3>Speech model</h3><select className="input text-xs" value={whisperModel} onChange={(e)=>setWhisperModel(e.target.value)}>{['tiny','base','small','medium','large-v3'].map(name=><option key={name}>{localModels.find(item=>item.name===name)?.installed?'★ ':''}{name}</option>)}</select><div className="flex justify-between mt-2 text-[9px] text-zinc-500"><span>{localModels.find(item=>item.name===whisperModel)?.installed?'Installed':'Download required'}</span><span>{formatSize(localModels.find(item=>item.name===whisperModel)?.sizeBytes??0)}</span></div><button className="btn w-full mt-2 !py-2 text-[10px]" disabled={modelBusy||running} onClick={()=>void toggleWhisperModel()}>{modelBusy?'Preparing…':localModels.find(item=>item.name===whisperModel)?.installed?'Remove model':'Install model'}</button></div>
        <div className="inspector-section"><h3>Clip generation</h3><label><span className="label flex justify-between">Highlights <b>{count}</b></span><input type="range" min="3" max="20" value={count} onChange={(e)=>setCount(Number(e.target.value))} className="w-full accent-violet-500"/></label><div className="compact-grid mt-3"><label><span className="label">Duration</span><select className="input" value={maxLength} onChange={(e)=>setMaxLength(Number(e.target.value))}>{[15,30,60,90].map(v=><option key={v} value={v}>{v}s</option>)}</select></label><label><span className="label">Canvas</span><select className="input" value={aspect} onChange={(e)=>setAspect(e.target.value)}>{['9:16','1:1','16:9','4:5'].map(v=><option key={v}>{v}</option>)}</select></label></div><label className="block mt-3"><span className="label">Content category</span><select className="input text-[10px]" value={category} onChange={(e)=>setCategory(e.target.value)}>{['Auto','Sports','Gaming','Educational','Vlog','Comedy','News','Challenge'].map(value=><option key={value}>{value}</option>)}</select></label></div>
        <div className="inspector-section"><h3>Enhancements</h3><div className="space-y-2"><Toggle label="Dynamic captions" value={captions} set={setCaptions}/><Toggle label="Smart reframing" value={smartZoom} set={setSmartZoom}/><Toggle label="Blur background" value={blurBackground} set={setBlurBackground}/><Toggle label="Background music" value={music} set={setMusic}/></div></div>
        <div className="p-3 sticky bottom-0 bg-[#111218] border-t border-[#292b38]"><button disabled={running||!localEngine.available||(!file&&!url)} className="btn btn-primary w-full flex justify-center gap-2 disabled:opacity-40" onClick={()=>void start()}>{running?<Loader2 className="animate-spin" size={16}/>:<Bot size={16}/>} {running?'Analyzing…':'Find highlight moments'}</button>{running&&<button className="btn w-full mt-2 !py-2 text-red-300" onClick={()=>void cancel()}>Cancel job</button>}</div>
      </aside>
    </div>

    {progress&&<div className="editor-progress"><div className="flex justify-between mb-2"><span className="flex gap-2"><Loader2 className="animate-spin text-violet-400" size={13}/>{progress.phase} · {progress.message}</span><b>{progress.percent}%</b></div><div className="progress"><div style={{width:`${progress.percent}%`}}/></div></div>}

    <div className="editor-timeline"><div className="timeline-tools"><b>Timeline</b><div className="tool-row"><button><Scissors size={13}/></button><button><Trash2 size={13}/></button><button><ZoomOut size={13}/></button><button><ZoomIn size={13}/></button></div><span className="block text-[8px] text-zinc-600 mt-4">{clips.length} generated clips</span></div><div className="timeline-area"><div className="timeline-ruler"><span>00:00</span><span>00:15</span><span>00:30</span><span>00:45</span><span>01:00</span></div><div className="playhead"/><div className="track"><span className="track-label">VIDEO 1</span><div className="track-clip">{file?.split(/[\\/]/).pop()??'Source video'}</div></div><div className="track audio"><span className="track-label">AUDIO 1</span><div className="track-clip">Speech waveform</div></div><div className="track caption"><span className="track-label">CAPTIONS</span><div className="track-clip">Word-synced captions</div></div>{speakerTimeline?.speakers.slice(0,3).map((speaker,index)=><div className="track" key={speaker}><span className="track-label">{speaker}</span><div className="track-clip" style={{marginLeft:`${index*40}px`,width:`${Math.max(120,speakerTimeline.turns.filter(turn=>turn.speaker===speaker).reduce((sum,turn)=>sum+turn.end_seconds-turn.start_seconds,0)*4)}px`}}>Active speaker</div></div>)}</div></div>

    {clips.length>0&&<div className="results-drawer"><div className="panel-heading"><span>Generated highlights</span><div className="flex gap-1"><button className="btn !p-1" onClick={()=>void approveAll()}><Check size={12}/></button><button className="btn !p-1" onClick={()=>void uploadApproved()}><Upload size={12}/></button></div></div>{clips.slice(0,8).map(clip=><div className="result-mini" key={clip.id}><video src={`media://file?path=${encodeURIComponent(clip.local_path)}`}/><div className="min-w-0 flex-1"><span className="badge text-violet-300">{clip.score}/10</span><input className="input mt-2" defaultValue={clip.suggested_title} onBlur={(e)=>void window.api.clipper.update(clip.id,{suggested_title:e.target.value})}/><div className="flex gap-1 mt-1"><button className="btn !p-1" onClick={()=>void window.api.clipper.export(clip.id)}><Download size={11}/></button><button className="btn !p-1" onClick={()=>void window.api.clipper.update(clip.id,{status:'approved'}).then(load)}><Check size={11}/></button></div></div></div>)}</div>}
  </div>;
}
function Toggle({ label, value, set }: { label: string; value: boolean; set: (value: boolean) => void }): JSX.Element {
  return <label className="flex items-center gap-2 rounded border border-border p-2"><input type="checkbox" className="accent-red-600" checked={value} onChange={(event) => set(event.target.checked)}/>{label}</label>;
}
