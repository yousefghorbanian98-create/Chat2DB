# Muscle Paradise × n8n Workflows Bridge
## Extracted from Zie619 collection for gym OS automation

**Source catalog (browse):** https://zie619.github.io/n8n-workflows/  
**Source repo:** https://github.com/Zie619/n8n-workflows  
**Collection license:** MIT (repo LICENSE)  
**n8n runtime:** separate product — check https://github.com/n8n-io/n8n license (Sustainable Use / fair-code); self-host carefully  

**Map version:** pairs with `ENGINEERING_MAP_FULL_v1.md` **v1.2+** §12.8  

---

## 0. What this source is (honest)

| Fact | Detail |
|------|--------|
| Size | **4,343+** workflow JSON templates, **15–16** categories, **268–365** integrations |
| UI | Search + category + complexity + trigger filters |
| Format | Standard n8n export JSON → import into any n8n instance |
| Gym-specific? | **No dedicated “gym OS” pack** — patterns are general (CRM, WhatsApp, SMS, PDF, RAG, cron, backup) |
| Value for MP | **Automation blueprints** for *optional* side processes around the local core — not a replacement for JP7 / SQLite / Studio |

### Critical architecture rule (same as OmniRoute / SocratiCode)

```
MP Core (FastAPI :8751, offline-first)  ←── always works alone
        │
        │  OPTIONAL webhook events (member.expiring, payment.created, …)
        ▼
n8n (self-host LAN or owner PC)  ←── import JSON from Zie619 catalog
        │
        ├── Telegram / WhatsApp / SMS (Iran adapters)
        ├── Email PDF receipt
        ├── Scheduled expiry digests
        ├── RAG chat over public KB (not private medical by default)
        └── Backup to Nextcloud/Git (ops, not athlete PII dump)
```

- **Do not** make n8n required for check-in, JP7, or Client login.  
- **Do not** send full injury dossiers / national IDs to cloud nodes without explicit OWNER consent + redact.  
- Prefer **local n8n** + local Ollama nodes when AI is involved.

---

## 1. MP needs → n8n pattern map

| MP product need (from engineering map) | n8n pattern to steal | Priority | How to wire |
|----------------------------------------|----------------------|----------|-------------|
| Membership expiry reminder (۷ / ۳ / ۱ روز) | Scheduled cron + filter + multi-channel notify | **P0** | MP job emits `membership.expiring` → n8n webhook **or** n8n cron polls `GET /api/v1/reports/expiring` |
| Absence N days alert (retention) | Schedule + HTTP + Telegram/SMS | **P0** | `GET /reports/inactive-members` |
| Payment received → receipt PDF → send | Webhook + HTML/PDF + Gmail/Telegram | **P0** | `payment.created` webhook from MP |
| Invoice / accounting export | Invoice email / OCR / sheets append | **P1** | Nightly export CSV/PDF to Drive/Sheets (OWNER only) |
| Coach↔member messaging bridge | WhatsApp / Telegram business bots | **P0 optional** | Bridge only; core messages stay in MP DB |
| AI Q&A on public exercise KB | RAG + Ollama/OpenAI + vector store | **P1** | Feed **Knowledge Pack public chunks only**, not member PHI |
| Ollama local chat ops | Ollama Chat workflows | **P1** | Same host as MP AI runtime |
| Calendar: PT sessions / classes | Google Calendar agent / create event | **P2** | If gym uses Google Calendar for classes |
| Backup automation | Backup to Nextcloud / Git / Bitbucket | **P1 ops** | Backup **encrypted MP packs** only |
| SSL / health monitoring | SSL expiry + URL pinger | **P2 ops** | Monitor MP API `:8751/health` |
| Progress photo pipeline | Image edit / Drive / vision OCR | **P2** | Optional; keep photos local-first |
| Lead capture (new gym marketing) | Sheets list builder / CRM | **P3** | Outside core membership |
| Error SMS when automation fails | Twilio/SMS on workflow error | **P1** | Ops reliability |
| “What to eat” style meal tip | Cron + HTTP content | **P3** | Fun Client push — not clinical nutrition |

---

## 2. Concrete workflow JSON links (from Zie619/main)

> Import path in n8n: **⋯ → Import from File** → paste/download JSON.  
> Always **re-bind credentials** and rewrite URLs to `http://127.0.0.1:8751`.  
> Re-test with synthetic members only.

### 2.1 Messaging (Client notifications)

| Template | Raw JSON |
|----------|----------|
| WhatsApp starter workflow | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Whatsapp/2030_Whatsapp_Respondtowebhook_Automate_Webhook.json |
| AI Customer-Support Assistant · WhatsApp Ready | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Whatsapp/1521_Whatsapp_Stickynote_Automation_Webhook.json |
| Business WhatsApp AI RAG Chatbot | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Webhook/1561_Webhook_Respondtowebhook_Automate_Webhook.json |
| WhatsApp business bot (scheduled) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Wait/1572_Wait_Schedule_Automate_Scheduled.json |
| Telegram AI-bot | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Openai/0248_Openai_Telegram_Automate_Triggered.json |
| Telegram AI-bot (alt) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Openai/1685_Openai_Telegram_Automate_Triggered.json |
| Academic Assistant Chatbot (Telegram + OpenAI) | search in repo under `workflows/Telegram/` — file name contains `Academic Assistant` |
| RSS → Telegram (pattern for digests) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Noop/0748_Noop_Telegram_Automation_Scheduled.json |

**Iran note:** replace Twilio/global SMS with **Kavenegar / IPPanel / Ghasedak** HTTP nodes; keep template structure (cron → query → send).

### 2.2 SMS primitives

| Template | Raw JSON |
|----------|----------|
| A workflow with the Twilio node | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Manual/0949_Manual_Twilio_Automate_Triggered.json |
| Monitoring and alerting (Twilio cron) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Twilio/0842_Twilio_Cron_Send_Scheduled.json |
| Send SMS when a workflow fails | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Error/1036_Error_Twilio_Send_Triggered.json |
| Send an SMS using MSG91 | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Manual/0986_Manual_Msg91_Send_Triggered.json |
| Sending an SMS using sms77 | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Manual/1199_Manual_Sms77_Send_Triggered.json |
| Sending an SMS with MessageBird | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Manual/1166_Manual_Messagebird_Send_Triggered.json |

### 2.3 PDF / invoice / receipt

| Template | Raw JSON |
|----------|----------|
| Html2Pdf-style webhook PDF | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Webhook/0813_Webhook_Respondtowebhook_Process_Webhook.json |
| Get PDF with JSReport | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Http/1883_HTTP_Form_Import_Webhook.json |
| New invoice email notification | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Slack/1194_Slack_Emailreadimap_Create.json |
| Colombian Invoices Processing | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Code/1765_Code_Filter_Process_Triggered.json |
| OCR receipts from Google Drive | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Code/1839_Code_Manual_Automation_Webhook.json |
| Merge PDFs | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Manual/1547_Manual_HTTP_Automation_Webhook.json |
| pdf to text | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Manual/1545_Manual_Code_Automation_Triggered.json |
| Expense Tracker App | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Http/1030_HTTP_Typeform_Monitor_Webhook.json |

**MP mapping:** Prefer generating PDF **inside MP** (deterministic), then n8n only **delivers** the file bytes via Telegram/Email.

### 2.4 Schedule / expiry / calendar

| Template | Raw JSON |
|----------|----------|
| SSL Expiry Alert (pattern for membership expiry cron) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Schedule/1614_Schedule_HTTP_Send_Webhook.json |
| URL Pinger (pattern for `/health` monitor) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Http/1447_HTTP_Schedule_Automation_Webhook.json |
| 🤖 Calendar Agent | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Googlecalendartool/1792_Googlecalendartool_Executeworkflow_Automation_Triggered.json |
| Google Calendar + tools (complex) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Splitout/1297_Splitout_GoogleCalendar_Automation_Webhook.json |
| Standup Bot – Worker (cron fan-out pattern) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Webhook/0066_Webhook_Cron_Automate_Scheduled.json |
| What To Eat (cron content tip pattern) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Http/0084_HTTP_Cron_Automation_Webhook.json |

### 2.5 RAG / local AI (Knowledge Pack side)

| Template | Raw JSON |
|----------|----------|
| 🗨️ Ollama Chat | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Stickynote/1691_Stickynote_Automation_Triggered.json |
| 🗨️ Ollama Chat (alt) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Stickynote/2048_Stickynote_Automation_Triggered.json |
| Agent Milvus tool | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Splitout/1243_Splitout_Limit_Automation_Webhook.json |
| Telegram RAG pdf | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Stopanderror/1061_Stopanderror_Telegram_Automation_Triggered.json |
| SHEETS RAG | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Postgres/1144_Postgres_Code_Automation_Triggered.json |
| Adaptive RAG | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Summarize/1829_Summarize_Respondtowebhook_Automation_Webhook.json |
| Make OpenAI Citation for File Retrieval RAG | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Splitout/1059_Splitout_Code_Automation_Webhook.json |
| LLM Chaining examples | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Splitout/0958_Splitout_Webhook_Automation_Webhook.json |
| Voice RAG Chatbot (ElevenLabs + OpenAI) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Webhook/1887_Webhook_Respondtowebhook_Automate_Webhook.json |

**MP mapping:** Core program generation stays in **MP brain (rules ⊕ Ollama)**; n8n RAG is for **optional coach assistant** over public exercise/nutrition literature packs.

### 2.6 Backup / ops

| Template | Raw JSON |
|----------|----------|
| Example – Backup n8n to Nextcloud | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Functionitem/1067_Functionitem_Manual_Export_Webhook.json |
| Backup workflows to git repository | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Code/0628_Code_Schedule_Export_Scheduled.json |
| Backup n8n Workflows to Bitbucket | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Wait/0567_Wait_Code_Export_Webhook.json |
| Restore your workflows from GitHub | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Splitout/1760_Splitout_GitHub_Automate_Webhook.json |
| Restore your credentials from GitHub | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Splitout/1147_Splitout_GitHub_Automation_Webhook.json |
| Tools / Backup Gitlab | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Manual/0200_Manual_Executecommand_Export_Scheduled.json |
| Clockify Backup Template | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Stopanderror/1896_Stopanderror_Splitout_Export_Scheduled.json |

**MP mapping:** Schedule call to `POST /api/v1/backup/export` → store **encrypted** artifact to USB/Nextcloud; never plain-text DB to public git.

### 2.7 Spreadsheet / light CRM

| Template | Raw JSON |
|----------|----------|
| List Builder (Google Sheets) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Manual/1739_Manual_GoogleSheets_Create_Triggered.json |
| 🤖 Contact Agent (Airtable) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Executeworkflow/1793_Executeworkflow_Airtabletool_Automation_Triggered.json |
| 🤖 Email Agent | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Gmailtool/1795_Gmailtool_Executeworkflow_Send_Triggered.json |
| Shopify + Mautic (funnel pattern) | https://raw.githubusercontent.com/Zie619/n8n-workflows/main/workflows/Mautic/1526_Mautic_Webhook_Automation_Webhook.json |

### 2.8 Search the live catalog yourself

Open: https://zie619.github.io/n8n-workflows/  

Suggested search queries for MP:
```
whatsapp reminder
telegram schedule
invoice pdf
ollama
rag pdf
backup nextcloud
google calendar
twilio cron
expiry
subscription
webhook respond
```

---

## 3. Recommended MP ↔ n8n event contract

Emit from MP Core (optional module `automation_webhooks`):

```json
{
  "v": 1,
  "event": "membership.expiring",
  "gym_id": "ulid…",
  "at": "2026-08-29T12:00:00+03:30",
  "member": {
    "id": "ulid…",
    "display_name": "Ali R.",
    "phone_e164": "+98…",
    "telegram_chat_id": null,
    "days_left": 3,
    "package": "monthly"
  },
  "links": {
    "client_deep_link": "mp://renew",
    "studio_url": "http://127.0.0.1:8751/…"
  },
  "privacy": { "phi": false, "redacted": true }
}
```

Other events: `payment.created`, `attendance.absent_streak`, `program.approved`, `assessment.saved` (no raw skinfolds in webhook by default), `backup.completed`, `ai.job.failed`.

Settings toggles in Studio:
- [ ] Enable automation bridge  
- [ ] n8n base URL (default `http://127.0.0.1:5678`)  
- [ ] Shared HMAC secret for webhooks  
- [ ] Allow channels: Telegram / WhatsApp / SMS / Email  
- [ ] Forbid PHI in outbound payloads (default ON)

---

## 4. First five workflows to implement for a real gym

| # | Name | Trigger | Action |
|---|------|---------|--------|
| 1 | `mp-expiry-d3` | Cron daily 09:00 | HTTP GET expiring in 3d → Telegram/SMS FA template |
| 2 | `mp-expiry-d0` | Cron | Same day freeze QR if policy says so + notify |
| 3 | `mp-payment-receipt` | Webhook `payment.created` | Attach MP PDF → Email/Telegram |
| 4 | `mp-absent-7d` | Cron weekly | List inactive → coach Telegram digest |
| 5 | `mp-backup-nightly` | Cron 02:00 | Call backup export → copy encrypted file to folder/Nextcloud |

Clone structure from SSL Expiry / Twilio cron / invoice email / backup Nextcloud templates above; replace nodes with MP HTTP + Iranian SMS.

---

## 5. Local install (optional owner machine)

```bash
# A) Browse catalog only
open https://zie619.github.io/n8n-workflows/

# B) Clone catalog for offline search
git clone --depth 1 https://github.com/Zie619/n8n-workflows.git
cd n8n-workflows
pip install -r requirements.txt
python run.py
# local UI often http://localhost:8000

# C) Run n8n itself (separate)
docker run -it --rm \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
# Editor: http://localhost:5678
```

Import selected JSON → set credentials → point HTTP Request nodes at MP `:8751`.

---

## 6. License & compliance checklist

- [ ] Zie619 collection: MIT — keep attribution in `docs/MuscleParadise` / About **automation** page  
- [ ] Individual workflows may embed third-party brand names — verify before commercial redistribution of *modified* JSON packs  
- [ ] n8n engine license reviewed for your distribution model (self-host OK for internal gym use typically; embedding engine in paid SaaS may need commercial terms)  
- [ ] No athlete medical PHI in n8n cloud nodes  
- [ ] Secrets in n8n credentials store, not in workflow JSON committed to git  

---

## 7. What n8n does **not** replace in MP

| Still native in MP |
|--------------------|
| JP7 math + golden tests |
| Injury hard-filters |
| Client RBAC field masking |
| Offline check-in QR verify |
| Rule ⊕ Ollama program race/judge |
| Local SQLite source of truth |
| Electron delta updater |

n8n = **optional nervous system for notifications & ops**, not the skeleton.

---

## 8. Agent bootstrap add-on

```
When implementing optional automation for Muscle Paradise:
- Read docs/MuscleParadise/N8N_AUTOMATION_BRIDGE.md
- Prefer webhook events from MP Core over polling when possible
- Import patterns from Zie619 JSON links; rewrite to local :8751
- Never require n8n for core offline gym operations
- Never send PHI to third-party AI nodes by default
```

---

## 9. Primary links (copy block)

```
Catalog UI:     https://zie619.github.io/n8n-workflows/
GitHub repo:    https://github.com/Zie619/n8n-workflows
This bridge doc:https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/N8N_AUTOMATION_BRIDGE.md
Engineering map:https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md
n8n project:    https://github.com/n8n-io/n8n
n8n docs import:https://docs.n8n.io/workflows/export-import/
```

---

**END N8N_AUTOMATION_BRIDGE**
