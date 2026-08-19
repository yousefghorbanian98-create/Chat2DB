import { useEffect, useState } from 'react';
import { CheckCircle2, ExternalLink, KeyRound, Loader2, ShieldCheck, Trash2, XCircle } from 'lucide-react';
import { useStore } from '@/lib/store';
import { toast } from 'sonner';
import type { AppSettings, Privacy } from '../../electron/types';
import type { HuggingFaceState, SystemProfile } from '../global';

export function Settings(): JSX.Element {
  const settings = useStore((state) => state.settings);
  const setSettings = useStore((state) => state.setSettings);
  const [token, setToken] = useState('');
  const [modelAccess, setModelAccess] = useState<HuggingFaceState>();
  const [checking, setChecking] = useState(false);
  const [system, setSystem] = useState<SystemProfile>();

  useEffect(() => { void Promise.all([window.api.huggingFace.state(false),window.api.system.profile()]).then(([access,profile])=>{setModelAccess(access);setSystem(profile)}); }, []);
  if (!settings) return <div className="page">Loading…</div>;
  const save = async (patch: Partial<AppSettings>): Promise<void> => { setSettings(await window.api.settings.set(patch)); toast.success('Setting saved'); };
  const saveToken = async (): Promise<void> => {
    setChecking(true);
    try { const state = await window.api.huggingFace.save(token); setModelAccess(state); setToken(''); toast.success('Professional model access verified and stored securely'); }
    catch (error: unknown) { toast.error(error instanceof Error ? error.message : String(error)); }
    finally { setChecking(false); }
  };
  const verify = async (): Promise<void> => { setChecking(true); setModelAccess(await window.api.huggingFace.state(true)); setChecking(false); };
  const remove = async (): Promise<void> => { setModelAccess(await window.api.huggingFace.remove()); setToken(''); toast.success('Access token removed'); };
  const cleanTemporary = async ():Promise<void>=>{const result=await window.api.system.cleanup();setSystem(await window.api.system.profile());toast.success(`${String(result.removed)} old temporary items removed`)};
  const size=(bytes?:number):string=>bytes===undefined?'—':bytes>=1024**3?`${(bytes/1024**3).toFixed(1)} GB`:`${(bytes/1024**2).toFixed(0)} MB`;

  return <div className="page"><div className="flex items-end justify-between"><div><span className="text-[10px] tracking-[.18em] text-violet-400">VIOLETCUT SYSTEM</span><h1 className="text-2xl font-bold mt-1">Settings</h1><p className="muted text-sm mt-1">Hardware, publishing, and private model access.</p></div><ShieldCheck className="text-violet-400" size={30}/></div><div className="grid grid-cols-2 gap-5 mt-6">
    <Section title="Hardware and storage"><div className="grid grid-cols-2 gap-3 text-xs"><div className="rounded-lg bg-[#0d0e13] p-3"><span className="muted">Processor</span><b className="block mt-1 truncate">{system?.cpu??'Scanning…'}</b><small>{system?.logicalCores??0} logical cores</small></div><div className="rounded-lg bg-[#0d0e13] p-3"><span className="muted">Graphics</span><b className="block mt-1 truncate">{system?.gpu??'CPU mode'}</b><small>{size(system?.gpuMemory)}</small></div><div className="rounded-lg bg-[#0d0e13] p-3"><span className="muted">Memory</span><b className="block mt-1">{size(system?.totalMemory)}</b><small>{size(system?.freeMemory)} free</small></div><div className="rounded-lg bg-[#0d0e13] p-3"><span className="muted">Disk</span><b className="block mt-1">{size(system?.diskFree)} free</b><small>Models {size(system?.modelBytes)}</small></div></div><div className="flex justify-between items-center rounded-lg border border-violet-900/50 bg-violet-950/20 p-3"><div><span className="label">Recommended processing profile</span><b className="capitalize">{system?.recommendedProfile??'Scanning'}</b></div><button className="btn" onClick={()=>void cleanTemporary()}>Clean old temporary files</button></div><p className="text-xs muted">Temporary files: {size(system?.temporaryBytes)} · {system?.os}</p></Section>
    <Section title="Professional AI models"><div className={`rounded-lg border p-3 ${modelAccess?.verified?'border-emerald-800 bg-emerald-950/20':'border-[#343645] bg-[#0d0e13]'}`}><div className="flex items-center gap-3">{modelAccess?.verified?<CheckCircle2 className="text-emerald-400" size={20}/>:<KeyRound className="text-violet-400" size={20}/>}<div><b className="text-sm">{modelAccess?.verified?'Speaker models authorized':modelAccess?.configured?'Token stored · verification required':'Access token not configured'}</b><p className="muted text-xs mt-1">{modelAccess?.username?`Account: ${modelAccess.username}`:'The full token is never shown after saving.'}</p></div></div></div>
    {!modelAccess?.configured&&<Field label="Read-only access token"><input className="input" type="password" autoComplete="off" value={token} onChange={(event)=>setToken(event.target.value)} placeholder="hf_••••••••••••••••"/></Field>}
    {modelAccess?.repositories.map((repository)=><div className="flex items-center justify-between text-xs" key={repository.id}><code>{repository.id}</code>{repository.accessible?<CheckCircle2 className="text-emerald-400" size={15}/>:<XCircle className="text-zinc-600" size={15}/>}</div>)}
    {modelAccess?.error&&<p className="text-red-300 text-xs">{modelAccess.error}</p>}
    <div className="flex flex-wrap gap-2">{!modelAccess?.configured?<button className="btn btn-primary flex items-center gap-2" disabled={checking||!token} onClick={()=>void saveToken()}>{checking?<Loader2 className="animate-spin" size={14}/>:<KeyRound size={14}/>} Verify and save</button>:<><button className="btn" disabled={checking} onClick={()=>void verify()}>{checking?'Checking…':'Verify access'}</button><button className="btn text-red-300 flex items-center gap-2" onClick={()=>void remove()}><Trash2 size={14}/> Remove token</button></>}<button className="btn flex items-center gap-2" onClick={()=>void window.api.openExternal('https://huggingface.co/settings/tokens')}><ExternalLink size={14}/> Account settings</button></div></Section>
    <Section title="Uploads"><Field label="Default privacy"><select className="input" value={settings.defaultPrivacy} onChange={(event)=>void save({defaultPrivacy:event.target.value as Privacy})}><option value="private">Private</option><option value="unlisted">Unlisted</option><option value="public">Public</option></select></Field><Toggle label="Keep downloaded source files" value={settings.keepDownloads} onChange={(value)=>void save({keepDownloads:value})}/></Section>
    <Section title="Local language model"><Field label="Endpoint"><input className="input" defaultValue={settings.ollamaEndpoint} onBlur={(event)=>void save({ollamaEndpoint:event.target.value})}/></Field><Field label="Default model"><input className="input" defaultValue={settings.defaultModel} onBlur={(event)=>void save({defaultModel:event.target.value})}/></Field><button className="btn" onClick={()=>void window.api.openExternal('https://ollama.com/download/windows')}>Download local model server</button></Section>
    <Section title="Performance"><Field label="Download concurrency"><input className="input" type="number" min="1" max="4" value={settings.downloadConcurrency} onChange={(event)=>void save({downloadConcurrency:Number(event.target.value)})}/></Field><Field label="Upload concurrency"><input className="input" type="number" min="1" max="2" value={settings.uploadConcurrency} onChange={(event)=>void save({uploadConcurrency:Number(event.target.value)})}/></Field><Toggle label="Start monitor with app" value={settings.autoStartMonitor} onChange={(value)=>void save({autoStartMonitor:value})}/><Toggle label="Minimize to system tray" value={settings.minimizeToTray} onChange={(value)=>void save({minimizeToTray:value})}/></Section>
    <Section title="Account and diagnostics"><button className="btn" onClick={()=>void window.api.auth.logout().then(()=>location.reload())}>Sign out</button><Toggle label="Enable production developer tools" value={settings.devtools} onChange={(value)=>void save({devtools:value})}/></Section>
    <Section title="About"><p className="muted">VioletCut · Professional AI Video Studio</p><p className="muted text-sm mt-2">Credentials use Windows secure storage. Tokens are never written to application settings or logs.</p></Section>
  </div></div>;
}

function Section({title,children}:{title:string;children:React.ReactNode}):JSX.Element{return <section className="card p-5"><h2 className="font-bold text-base mb-5">{title}</h2><div className="space-y-4">{children}</div></section>}
function Field({label,children}:{label:string;children:React.ReactNode}):JSX.Element{return <label><span className="label">{label}</span>{children}</label>}
function Toggle({label,value,onChange}:{label:string;value:boolean;onChange:(value:boolean)=>void}):JSX.Element{return <label className="flex justify-between items-center"><span className="text-sm">{label}</span><input className="accent-violet-600 w-5 h-5" type="checkbox" checked={value} onChange={(event)=>onChange(event.target.checked)}/></label>}
