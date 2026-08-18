import {Bell,Cloud,Languages,Moon,Search,Sun} from 'lucide-react';
import {useLocation} from 'react-router-dom';
import {useStore} from '@/lib/store';

export function TopBar():JSX.Element {
  const location=useLocation();const settings=useStore(s=>s.settings);const setSettings=useStore(s=>s.setSettings);
  const update=async(patch:Parameters<typeof window.api.settings.set>[0])=>setSettings(await window.api.settings.set(patch));
  const title=location.pathname==='/'?'Creative dashboard':location.pathname==='/clipper'?'AI editing workspace':location.pathname.slice(1).replace('-',' ');
  return <header className="app-topbar fixed top-0 left-[224px] right-0 h-14 border-b border-[#292b38] bg-[#0d0e13eF] backdrop-blur-xl flex items-center justify-between px-5 z-20"><div className="flex items-center gap-4"><b className="text-xs capitalize">{title}</b><div className="hidden xl:flex items-center gap-2 rounded-lg border border-[#292b38] bg-[#111218] px-3 py-1.5 text-zinc-600"><Search size={13}/><span className="text-[10px]">Search tools and projects</span><kbd className="ml-12 text-[8px] border border-[#343643] rounded px-1">Ctrl K</kbd></div></div><div className="flex items-center gap-2"><div className="mr-2 flex items-center gap-2 text-[9px] text-emerald-400"><Cloud size={13}/><span>LOCAL ENGINE READY</span></div><button className="btn !p-2" aria-label="Change language" onClick={()=>void update({language:settings?.language==='fa'?'en':'fa'})}><Languages size={15}/></button><button className="btn !p-2" aria-label="Toggle theme" onClick={()=>void update({theme:settings?.theme==='light'?'dark':'light'})}>{settings?.theme==='light'?<Moon size={15}/>:<Sun size={15}/>}</button><button className="btn !p-2" aria-label="Notifications"><Bell size={15}/></button></div></header>;
}
