import { Bot, Clock3, History, Home, RefreshCw, Settings, Upload, Users, Video, WandSparkles } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { useStore } from '@/lib/store';
import { useI18n, type TranslationKey } from '@/i18n';

const links: ReadonlyArray<readonly [string, typeof Home, TranslationKey]> = [
  ['/', Home, 'dashboard'], ['/upload', Upload, 'single'], ['/channel', Users, 'channel'], ['/sync', RefreshCw, 'sync'],
  ['/clipper', Bot, 'clipper'], ['/pending', Clock3, 'pending'], ['/history', History, 'history'], ['/settings', Settings, 'settings']
];

export function Sidebar(): JSX.Element {
  const account = useStore((state) => state.auth?.account);
  const { t } = useI18n();
  return <aside className="fixed inset-y-0 left-0 rtl:left-auto rtl:right-0 w-[224px] border-r rtl:border-r-0 rtl:border-l border-[#292b38] bg-[#101116] p-3 flex flex-col z-20 shadow-2xl shadow-black/30">
    <div className="flex items-center gap-3 px-2 h-14"><div className="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-500 to-blue-600 grid place-items-center shadow-lg shadow-violet-900/40"><WandSparkles size={19}/></div><div><b className="text-sm">VioletCut</b><span className="block text-[9px] tracking-widest text-zinc-500">AI VIDEO STUDIO</span></div></div>
    <div className="px-3 mt-5 mb-2 text-[9px] font-bold tracking-[.18em] text-zinc-600">WORKSPACE</div>
    <nav className="space-y-1">{links.slice(0,5).map(([to, Icon, key]) => <NavLink key={to} to={to} className={({ isActive }) => `group flex items-center gap-3 rounded-lg px-3 py-2.5 text-xs transition ${isActive ? 'bg-gradient-to-r from-violet-600/35 to-blue-600/10 text-white border border-violet-500/25' : 'text-zinc-500 border border-transparent hover:bg-[#1a1b24] hover:text-zinc-200'}`}><Icon size={17}/><span>{t(key)}</span></NavLink>)}</nav>
    <div className="px-3 mt-6 mb-2 text-[9px] font-bold tracking-[.18em] text-zinc-600">PUBLISH</div>
    <nav className="space-y-1">{links.slice(5).map(([to, Icon, key]) => <NavLink key={to} to={to} className={({ isActive }) => `flex items-center gap-3 rounded-lg px-3 py-2.5 text-xs ${isActive ? 'bg-[#282039] text-white' : 'text-zinc-500 hover:bg-[#1a1b24] hover:text-zinc-200'}`}><Icon size={17}/>{t(key)}</NavLink>)}</nav>
    <div className="mt-auto rounded-xl border border-[#292b38] bg-[#15161e] p-3 flex items-center gap-3">{account?.pictureUrl ? <img src={account.pictureUrl} className="w-9 h-9 rounded-lg"/> : <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-[#292b38] to-[#1b1c24] grid place-items-center"><Video size={15}/></div>}<div className="min-w-0"><div className="text-xs font-semibold truncate">{account?.channelName ?? account?.name}</div><div className="text-[9px] text-zinc-600 truncate">{account?.email}</div></div></div>
  </aside>;
}
