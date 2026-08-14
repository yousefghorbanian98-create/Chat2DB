import { useCallback, useEffect, useMemo, useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
import {
  AlertTriangle,
  Check,
  ChevronLeft,
  KeyRound,
  Link2,
  ListChecks,
  Loader2,
  LogOut,
  Pause,
  Play,
  RefreshCw,
  Search,
  ShieldCheck,
  Trash2,
  Youtube,
} from "lucide-react";

export type AutopilotCopy = Record<string, string>;

type ChannelInfo = { id: string; title: string; thumbnail: string; subscriberCount: string; videoCount: string; uploadsPlaylist: string };
type SourceVideo = { id: string; title: string; publishedAt: string; thumbnail: string; durationLabel: string; durationSeconds: number; creativeCommons: boolean };
type JobState = "pending" | "downloading" | "clipping" | "uploading" | "done" | "failed" | "skipped";
type Job = { id: string; sourceVideoId: string; sourceChannelId: string; title: string; state: JobState; attempts: number; error?: string | null; targetVideoId?: string | null; progress: number };
type Status = { configured: boolean; connected: boolean; channel: ChannelInfo | null; uploadsRemaining: number; quotaSpent: number; dailyQuota: number; paused: boolean; jobs: Job[]; ytDlpAvailable: boolean };
type Listing = { channel: ChannelInfo; videos: SourceVideo[]; isOwnChannel: boolean; acknowledged: boolean };
type Privacy = "private" | "unlisted" | "public";
type Progress = { jobId: string; state: JobState; progress: number; message?: string | null };

const errorText = (error: unknown) => (typeof error === "string" ? error : error instanceof Error ? error.message : String(error));

export default function Autopilot({ t, dir }: { t: AutopilotCopy; dir: "rtl" | "ltr" }) {
  const [status, setStatus] = useState<Status | null>(null);
  const [clientId, setClientId] = useState("");
  const [clientSecret, setClientSecret] = useState("");
  const [showSetup, setShowSetup] = useState(false);
  const [link, setLink] = useState("");
  const [listing, setListing] = useState<Listing | null>(null);
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const [filter, setFilter] = useState("");
  const [busy, setBusy] = useState<string | null>(null);
  const [message, setMessage] = useState<{ ok: boolean; text: string } | null>(null);
  const [privacy, setPrivacy] = useState<Privacy>("private");
  const [dryRun, setDryRun] = useState(true);
  const [titleTemplate, setTitleTemplate] = useState("{title}");
  const [needsAck, setNeedsAck] = useState(false);
  const [liveProgress, setLiveProgress] = useState<Record<string, Progress>>({});

  const refresh = useCallback(async () => {
    try {
      setStatus(await invoke<Status>("autopilot_status"));
    } catch (error) {
      setMessage({ ok: false, text: errorText(error) });
    }
  }, []);

  useEffect(() => { void refresh(); }, [refresh]);

  useEffect(() => {
    const unlisten = listen<Progress>("autopilot-progress", (event) => {
      setLiveProgress((current) => ({ ...current, [event.payload.jobId]: event.payload }));
      if (event.payload.state === "done" || event.payload.state === "failed") void refresh();
    });
    return () => { void unlisten.then((off) => off()); };
  }, [refresh]);

  const saveCredentials = async () => {
    setBusy("credentials"); setMessage(null);
    try {
      await invoke("autopilot_save_credentials", { clientId, clientSecret });
      setShowSetup(false); setClientSecret("");
      setMessage({ ok: true, text: t.credentialsSaved });
      await refresh();
    } catch (error) { setMessage({ ok: false, text: errorText(error) }); }
    finally { setBusy(null); }
  };

  const connect = async () => {
    setBusy("connect"); setMessage(null);
    try {
      const channel = await invoke<ChannelInfo>("autopilot_connect");
      setMessage({ ok: true, text: `${t.connectedAs} ${channel.title}` });
      await refresh();
    } catch (error) { setMessage({ ok: false, text: errorText(error) }); }
    finally { setBusy(null); }
  };

  const disconnect = async () => {
    setBusy("disconnect");
    try { await invoke("autopilot_disconnect"); setListing(null); await refresh(); }
    catch (error) { setMessage({ ok: false, text: errorText(error) }); }
    finally { setBusy(null); }
  };

  const loadSource = async () => {
    setBusy("source"); setMessage(null); setListing(null);
    try {
      const result = await invoke<Listing>("autopilot_load_source", { link, maxVideos: 200 });
      setListing(result);
      setSelected({});
      setNeedsAck(!result.isOwnChannel && !result.acknowledged);
    } catch (error) { setMessage({ ok: false, text: errorText(error) }); }
    finally { setBusy(null); }
  };

  const acknowledge = async () => {
    if (!listing) return;
    try {
      await invoke("autopilot_acknowledge", { channelId: listing.channel.id });
      setNeedsAck(false);
    } catch (error) { setMessage({ ok: false, text: errorText(error) }); }
  };

  const enqueue = async () => {
    if (!listing) return;
    const videos = listing.videos.filter((video) => selected[video.id]);
    if (videos.length === 0) { setMessage({ ok: false, text: t.selectSomething }); return; }
    setBusy("enqueue"); setMessage(null);
    try {
      const added = await invoke<number>("autopilot_enqueue", { request: { channelId: listing.channel.id, videos } });
      setMessage({ ok: true, text: `${added} ${t.queued}` });
      setSelected({});
      await refresh();
    } catch (error) { setMessage({ ok: false, text: errorText(error) }); }
    finally { setBusy(null); }
  };

  const runJob = async (job: Job) => {
    setBusy(job.id); setMessage(null);
    try {
      await invoke<string>("autopilot_run_job", {
        jobId: job.id,
        options: {
          privacy,
          titleTemplate,
          descriptionTemplate: `{title}\n\nOriginal: https://youtu.be/{id}`,
          tags: [],
          categoryId: "22",
          dryRun,
          rateLimit: null,
        },
      });
      setMessage({ ok: true, text: dryRun ? t.dryRunDone : t.uploadDone });
      await refresh();
    } catch (error) { setMessage({ ok: false, text: errorText(error) }); }
    finally { setBusy(null); }
  };

  const removeJob = async (job: Job) => {
    try { await invoke("autopilot_remove_job", { jobId: job.id }); await refresh(); }
    catch (error) { setMessage({ ok: false, text: errorText(error) }); }
  };

  const togglePause = async () => {
    if (!status) return;
    try { await invoke("autopilot_set_paused", { paused: !status.paused }); await refresh(); }
    catch (error) { setMessage({ ok: false, text: errorText(error) }); }
  };

  const selfTest = async () => {
    setBusy("selftest");
    try {
      const result = await invoke<{ details: string[] }>("autopilot_self_test");
      setMessage({ ok: true, text: result.details.join(" · ") });
    } catch (error) { setMessage({ ok: false, text: errorText(error) }); }
    finally { setBusy(null); }
  };

  const visible = useMemo(() => {
    if (!listing) return [];
    const needle = filter.trim().toLowerCase();
    return needle ? listing.videos.filter((v) => v.title.toLowerCase().includes(needle)) : listing.videos;
  }, [listing, filter]);

  const selectedCount = Object.values(selected).filter(Boolean).length;

  if (!status) return <div className="content page"><div className="ap-loading"><Loader2 className="ap-spin" size={22}/>{t.loading}</div></div>;

  return <div className="content page" dir={dir}>
    <div className="page-title">
      <div><span>AUTOPILOT</span><h1>{t.title}</h1></div>
      <button className="ap-ghost" disabled={busy === "selftest"} onClick={selfTest}><ShieldCheck size={16}/>{t.selfTest}</button>
    </div>

    {message && <div className={`ap-message ${message.ok ? "ok" : "bad"}`}>{message.ok ? <Check size={16}/> : <AlertTriangle size={16}/>}<p>{message.text}</p></div>}

    {!status.ytDlpAvailable && <div className="ap-message bad"><AlertTriangle size={16}/><p>{t.noYtDlp}</p></div>}

    {/* ---- connection ---- */}
    <section className="ap-card">
      <div className="ap-card-head"><div className="ap-icon"><Youtube size={19}/></div><div><h3>{t.account}</h3><p>{t.accountSub}</p></div></div>

      {!status.configured || showSetup ? <div className="ap-setup">
        <label>{t.clientId}<input value={clientId} onChange={(e) => setClientId(e.target.value)} placeholder="xxxxx.apps.googleusercontent.com" dir="ltr"/></label>
        <label>{t.clientSecret}<input value={clientSecret} type="password" onChange={(e) => setClientSecret(e.target.value)} placeholder="GOCSPX-..." dir="ltr"/></label>
        <button className="ap-primary" disabled={busy === "credentials"} onClick={saveCredentials}><KeyRound size={16}/>{t.saveCredentials}</button>
        <details className="ap-guide"><summary>{t.guideTitle}</summary>
          <ol>
            <li>{t.guide1}</li><li>{t.guide2}</li><li>{t.guide3}</li><li>{t.guide4}</li><li>{t.guide5}</li>
          </ol>
        </details>
      </div> : status.connected && status.channel ? <div className="ap-account">
        {status.channel.thumbnail && <img src={status.channel.thumbnail} alt=""/>}
        <div><b>{status.channel.title}</b><span>{status.channel.subscriberCount} {t.subscribers} · {status.channel.videoCount} {t.videos}</span></div>
        <button className="ap-ghost" onClick={() => setShowSetup(true)}><KeyRound size={15}/></button>
        <button className="ap-ghost" disabled={busy === "disconnect"} onClick={disconnect}><LogOut size={15}/>{t.disconnect}</button>
      </div> : <div className="ap-connect">
        <button className="ap-primary" disabled={busy === "connect"} onClick={connect}>
          {busy === "connect" ? <><Loader2 className="ap-spin" size={16}/>{t.waitingBrowser}</> : <><Youtube size={17}/>{t.signIn}</>}
        </button>
        <button className="ap-ghost" onClick={() => setShowSetup(true)}><KeyRound size={15}/>{t.editCredentials}</button>
      </div>}
    </section>

    {/* ---- quota ---- */}
    {status.connected && <section className="ap-quota">
      <div><b>{status.uploadsRemaining}</b><span>{t.uploadsLeft}</span></div>
      <div className="ap-quota-bar"><span style={{ width: `${Math.min(100, (status.quotaSpent / status.dailyQuota) * 100)}%` }}/></div>
      <p>{t.quotaNote}</p>
    </section>}

    {/* ---- source ---- */}
    {status.connected && <section className="ap-card">
      <div className="ap-card-head"><div className="ap-icon"><Link2 size={19}/></div><div><h3>{t.source}</h3><p>{t.sourceSub}</p></div></div>
      <div className="ap-source-row">
        <input value={link} onChange={(e) => setLink(e.target.value)} placeholder="https://www.youtube.com/@channel" dir="ltr"/>
        <button className="ap-primary" disabled={busy === "source" || !link.trim()} onClick={loadSource}>
          {busy === "source" ? <Loader2 className="ap-spin" size={16}/> : <Search size={16}/>}{t.load}
        </button>
      </div>

      {listing && <>
        <div className="ap-channel">
          {listing.channel.thumbnail && <img src={listing.channel.thumbnail} alt=""/>}
          <div><b>{listing.channel.title}</b><span>{listing.videos.length} {t.videosFound}</span></div>
          {listing.isOwnChannel && <span className="ap-badge ok"><Check size={12}/>{t.ownChannel}</span>}
        </div>

        {needsAck && <div className="ap-warning">
          <AlertTriangle size={18}/>
          <div>
            <b>{t.warnTitle}</b>
            <p>{t.warnBody}</p>
            <label><input type="checkbox" onChange={(e) => { if (e.target.checked) void acknowledge(); }}/>{t.warnAccept}</label>
          </div>
        </div>}

        <div className="ap-list-controls">
          <input value={filter} onChange={(e) => setFilter(e.target.value)} placeholder={t.filter}/>
          <button className="ap-ghost" onClick={() => setSelected(Object.fromEntries(visible.map((v) => [v.id, true])))}>{t.selectAll}</button>
          <button className="ap-ghost" onClick={() => setSelected({})}>{t.clear}</button>
        </div>

        <div className="ap-video-list">
          {visible.map((video) => <label key={video.id} className={`ap-video ${selected[video.id] ? "on" : ""}`}>
            <input type="checkbox" checked={!!selected[video.id]} disabled={needsAck} onChange={(e) => setSelected((s) => ({ ...s, [video.id]: e.target.checked }))}/>
            {video.thumbnail && <img src={video.thumbnail} alt=""/>}
            <div><b dir="auto">{video.title}</b><span>{video.durationLabel} · {video.publishedAt.slice(0, 10)}</span></div>
            <span className={`ap-badge ${video.creativeCommons ? "ok" : "warn"}`}>{video.creativeCommons ? t.ccLicence : t.stdLicence}</span>
          </label>)}
        </div>

        <div className="ap-actions">
          <label className="ap-inline">{t.privacy}
            <select value={privacy} onChange={(e) => setPrivacy(e.target.value as Privacy)}>
              <option value="private">{t.private}</option><option value="unlisted">{t.unlisted}</option><option value="public">{t.public}</option>
            </select>
          </label>
          <label className="ap-inline">{t.titleTemplate}<input value={titleTemplate} onChange={(e) => setTitleTemplate(e.target.value)} dir="ltr"/></label>
          <button className="ap-primary" disabled={busy === "enqueue" || selectedCount === 0 || needsAck} onClick={enqueue}>
            <ListChecks size={16}/>{t.addToQueue} ({selectedCount})
          </button>
        </div>
      </>}
    </section>}

    {/* ---- queue ---- */}
    {status.jobs.length > 0 && <section className="ap-card">
      <div className="ap-card-head">
        <div className="ap-icon"><ListChecks size={19}/></div>
        <div><h3>{t.queue}</h3><p>{status.jobs.length} {t.jobs}</p></div>
        <button className="ap-ghost" onClick={togglePause}>{status.paused ? <><Play size={15}/>{t.resume}</> : <><Pause size={15}/>{t.pause}</>}</button>
        <label className="ap-inline"><input type="checkbox" checked={dryRun} onChange={(e) => setDryRun(e.target.checked)}/>{t.dryRun}</label>
      </div>

      {status.jobs.map((job) => {
        const live = liveProgress[job.id];
        const state = live?.state ?? job.state;
        const percent = live?.progress ?? job.progress;
        return <div className="ap-job" key={job.id}>
          <div className="ap-job-main">
            <b dir="auto">{job.title}</b>
            <span className={`ap-state ${state}`}>{t[state] ?? state}</span>
          </div>
          {(state === "downloading" || state === "uploading") && <div className="ap-progress"><span style={{ width: `${percent}%` }}/></div>}
          {job.error && <p className="ap-error">{job.error}</p>}
          {job.targetVideoId && <a className="ap-link" href={`https://youtu.be/${job.targetVideoId}`} target="_blank" rel="noreferrer">youtu.be/{job.targetVideoId}<ChevronLeft size={13}/></a>}
          <div className="ap-job-actions">
            <button className="ap-ghost" disabled={busy === job.id || status.paused} onClick={() => runJob(job)}>
              {busy === job.id ? <Loader2 className="ap-spin" size={14}/> : <RefreshCw size={14}/>}{state === "failed" ? t.retry : t.run}
            </button>
            <button className="ap-ghost" onClick={() => removeJob(job)}><Trash2 size={14}/></button>
          </div>
        </div>;
      })}
    </section>}
  </div>;
}
