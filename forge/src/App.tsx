import { useCallback, useEffect, useState } from 'react'
import { motion } from 'motion/react'
import {
  api,
  runStream,
  type HealthResponse,
  type SettingsView,
  type UpdateCheck,
} from './lib/api.ts'
import type { Agent, Command, Message, Session } from './lib/types.ts'
import Icon from './components/Icon.tsx'
import StatusPills from './components/StatusPills.tsx'
import SessionList from './components/SessionList.tsx'
import ChatStream, { type TraceEntry } from './components/ChatStream.tsx'
import Composer from './components/Composer.tsx'
import CommandPalette from './components/CommandPalette.tsx'
import SidePanel from './components/SidePanel.tsx'
import Welcome from './components/Welcome.tsx'
import SetupSheet from './components/SetupSheet.tsx'
import SettingsSheet from './components/SettingsSheet.tsx'
import UpdateChip from './components/UpdateChip.tsx'

type Theme = 'forge-studio' | 'forge-studio-dark'

const THEME_KEY = 'forge.theme'

/** تم انتخابی باید پس از بستن و باز کردنِ برنامه هم بماند */
function initialTheme(): Theme {
  try {
    const saved = localStorage.getItem(THEME_KEY)
    if (saved === 'forge-studio' || saved === 'forge-studio-dark') return saved
  } catch {
    // localStorage در دسترس نیست (مثلاً حالتِ خصوصی) — پیش‌فرض کافی است
  }
  return 'forge-studio'
}

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [sessions, setSessions] = useState<Session[]>([])
  const [activeId, setActiveId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [commands, setCommands] = useState<Command[]>([])
  const [agents, setAgents] = useState<Agent[]>([])

  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)
  const [trace, setTrace] = useState<TraceEntry[]>([])
  const [skills, setSkills] = useState<string[]>([])
  const [palette, setPalette] = useState(false)
  const [setup, setSetup] = useState(false)
  const [settings, setSettingsOpen] = useState(false)
  const [appSettings, setAppSettings] = useState<SettingsView | null>(null)
  const [focusSignal, setFocusSignal] = useState(0)
  const [theme, setTheme] = useState<Theme>(initialTheme)
  const [update, setUpdate] = useState<UpdateCheck | null>(null)

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    try {
      localStorage.setItem(THEME_KEY, theme)
    } catch {
      // ذخیره نشد؛ برنامه بی‌صدا ادامه می‌دهد
    }
  }, [theme])

  const refreshSessions = useCallback(async () => {
    try {
      setSessions(await api.sessions())
    } catch {
      setSessions([])
    }
  }, [])

  useEffect(() => {
    api.health().then(setHealth).catch(() => setHealth(null))
    api.commands().then(setCommands).catch(() => setCommands([]))
    api.agents().then(setAgents).catch(() => setAgents([]))
    api.updateCheck().then(setUpdate).catch(() => setUpdate(null))
    api.settings().then(setAppSettings).catch(() => setAppSettings(null))
    refreshSessions()
  }, [refreshSessions])

  // میانبرِ سراسری: Ctrl+K فهرستِ دستورها
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        setPalette((p) => !p)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  const loadSession = useCallback(async (id: string) => {
    setActiveId(id)
    try {
      const s = await api.session(id)
      setMessages(s.messages)
    } catch {
      setMessages([])
    }
  }, [])

  const newSession = async () => {
    const s = await api.createSession('نشست جدید')
    setActiveId(s.id)
    setMessages([])
    setTrace([])
    setSkills([])
    await refreshSessions()
  }

  const send = async () => {
    const prompt = input.trim()
    if (!prompt || busy) return

    let sessionId = activeId
    if (!sessionId) {
      const s = await api.createSession(prompt.slice(0, 48))
      sessionId = s.id
      setActiveId(s.id)
      await refreshSessions()
    }

    // نمایشِ خوش‌بینانه‌ی پیامِ کاربر
    setMessages((prev) => [
      ...prev,
      { id: `tmp-${Date.now()}`, role: 'user', text: prompt, at: new Date().toISOString() },
    ])
    setInput('')
    setBusy(true)
    setTrace([])
    setSkills([])

    let finalText = ''

    runStream(prompt, sessionId, (ev) => {
      if (ev.type === 'stage' && ev.stage) {
        setTrace((prev) => [...prev, { stage: ev.stage!, text: ev.text }])
      }
      if (ev.type === 'skills' && ev.skills) {
        setSkills(ev.skills)
      }
      if (ev.type === 'result') {
        finalText = ev.text ?? ''
      }
      if (ev.type === 'error') {
        finalText = `خطا: ${ev.text ?? 'نامشخص'}`
      }
      if (ev.type === 'done') {
        setBusy(false)
        // سرور منبعِ حقیقت است؛ پیام‌ها از آن بازخوانی می‌شوند تا تکراری نشوند
        if (sessionId) {
          api
            .session(sessionId)
            .then((s) => setMessages(s.messages))
            .catch(() => {
              if (finalText) {
                setMessages((prev) => [
                  ...prev,
                  {
                    id: `local-${Date.now()}`,
                    role: 'agent',
                    text: finalText,
                    at: new Date().toISOString(),
                  },
                ])
              }
            })
          refreshSessions()
        }
      }
    })
  }

  return (
    <div className="flex h-full flex-col bg-canvas">
      <header className="flex items-center justify-between border-b border-hairline bg-canvas-soft px-6 py-4">
        <div className="flex items-center gap-3">
          <span
            className="flex size-9 items-center justify-center rounded-control border border-hairline bg-surface-strong"
            style={{ color: 'var(--color-brand)' }}
          >
            <Icon name="sparkles" size={17} />
          </span>
          <div className="flex flex-col">
            <h1 className="text-display-sm leading-none text-ink">Forge</h1>
            <span className="mt-1 text-body-sm leading-none text-muted">
              کنسولِ عامل‌های کدنویسی
            </span>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <UpdateChip check={update} />
          <StatusPills health={health} onOpenSetup={() => setSetup(true)} />
          <div className="flex items-center gap-1.5 border-r border-hairline pr-3">
            <button
              onClick={() => setSettingsOpen(true)}
              aria-label="تنظیمات"
              title="تنظیمات (پوشه‌ی پروژه و مدل)"
              className="rounded-control border border-hairline p-2 text-muted transition-colors hover:bg-surface hover:text-ink"
            >
              <Icon name="wrench" size={15} />
            </button>
            <button
              onClick={() => setSetup(true)}
              aria-label="راهنمای وصل‌کردنِ ابزارها"
              title="راهنمای وصل‌کردنِ ابزارها"
              className="rounded-control border border-hairline p-2 text-muted transition-colors hover:bg-surface hover:text-ink"
            >
              <Icon name="plug" size={15} />
            </button>
            <button
              onClick={() => setTheme(theme === 'forge-studio' ? 'forge-studio-dark' : 'forge-studio')}
              aria-label="تغییرِ تم"
              title="تغییرِ تم"
              className="rounded-control border border-hairline p-2 text-muted transition-colors hover:bg-surface hover:text-ink"
            >
              <Icon name={theme === 'forge-studio' ? 'moon' : 'sun'} size={15} />
            </button>
          </div>
        </div>
      </header>

      <div className="flex min-h-0 flex-1">
        <SessionList
          sessions={sessions}
          activeId={activeId}
          onSelect={loadSession}
          onNew={newSession}
          onDeleted={(id) => {
            if (activeId === id) {
              setActiveId(null)
              setMessages([])
              setTrace([])
              setSkills([])
            }
            void refreshSessions()
          }}
        />

        <main className="flex min-w-0 flex-1 flex-col">
          {messages.length === 0 && !busy ? (
            <Welcome
              health={health}
              brainReady={Boolean(appSettings?.provider && appSettings?.workspaceDir)}
              onOpenSettings={() => setSettingsOpen(true)}
              onOpenSetup={() => setSetup(true)}
              onPick={(prompt) => {
                setInput(prompt)
                setFocusSignal((n) => n + 1)
              }}
            />
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
              className="flex min-h-0 flex-1 flex-col"
            >
              <ChatStream messages={messages} trace={trace} busy={busy} skills={skills} />
            </motion.div>
          )}

          <Composer
            value={input}
            onChange={setInput}
            onSubmit={send}
            busy={busy}
            onOpenPalette={() => setPalette(true)}
            focusSignal={focusSignal}
          />
        </main>

        <SidePanel
          query={input}
          commands={commands}
          onPickCommand={(slug) => setInput(`/${slug} ${input}`)}
        />
      </div>

      <CommandPalette
        open={palette}
        onClose={() => setPalette(false)}
        commands={commands}
        agents={agents}
        onPick={(slug) => setInput(`/${slug} `)}
      />

      <SetupSheet open={setup} onClose={() => setSetup(false)} health={health} />

      <SettingsSheet
        open={settings}
        onClose={() => setSettingsOpen(false)}
        onSaved={() => {
          // سلامت و تنظیمات باید دوباره خوانده شوند تا وضعیتِ مدل تازه شود
          api.health().then(setHealth).catch(() => setHealth(null))
          api.settings().then(setAppSettings).catch(() => setAppSettings(null))
        }}
      />
    </div>
  )
}
