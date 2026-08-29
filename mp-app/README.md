# Muscle Paradise (MP) — `mp-app/`

Local-first Gym OS. Spec: `../docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md`.
Loop contract: FINN-LOOP v3.0 — state in [`LOOP_STATE.md`](./LOOP_STATE.md).

```
mp-app/
  backend/     FastAPI + SQLite core, port 8751
  studio/      Electron + React coach shell
  openapi.yaml generated from the running app
  LOOP_STATE.md DESIGN_SYSTEM.md ERRORS.log CHANGELOG.md NOTICES.md
```

## Run the core

```bash
cd mp-app/backend
python3 -m venv ../../.venv-mp && ../../.venv-mp/bin/pip install -r requirements.txt

# first run: create the gym + OWNER (PIN comes from the env, never argv)
MP_OWNER_USER=owner MP_OWNER_PIN=1234 ../../.venv-mp/bin/python -m app.bootstrap

./run.sh                      # uvicorn --factory on 127.0.0.1:8751
curl -s localhost:8751/health # {"status":"ok","db":{"schema_version":"0001_core", ...}}

# then log in and use the API
TOKEN=$(curl -s -X POST localhost:8751/api/v1/auth/pin \
  -H 'content-type: application/json' \
  -d '{"username":"owner","pin":"1234"}' | python3 -c 'import json,sys;print(json.load(sys.stdin)["token"])')
curl -s localhost:8751/api/v1/members -H "authorization: Bearer $TOKEN"
```

Migrations run automatically on startup. `MP_DB_PATH`, `MP_PORT`, `MP_HOST`,
`MP_CORS_ORIGINS`, `MP_GYM_NAME` are the only knobs.

## Run the Studio

```bash
cd mp-app/studio
npm install
npm run dev        # http://localhost:5173 (proxies /api + /health to :8751)
npm run build      # tsc --noEmit && vite build -> dist/
npm run test       # vitest
npm run gate       # typecheck + tests + build (FINN-LOOP gate)
```

Electron: `MP_DEV=1 npm run electron:dev` after `npm i electron`
(this repo installs with `ELECTRON_SKIP_BINARY_DOWNLOAD=1` to stay light).

## Tests

```bash
cd mp-app/backend && ../../.venv-mp/bin/python -m pytest      # 73 passed
cd mp-app/backend && ../../.venv-mp/bin/python -m pytest -m golden   # JP7 fixtures
```

## Regenerate openapi.yaml

```bash
cd mp-app/backend
../../.venv-mp/bin/python -m app.export_openapi | python3 -c \
  "import json,sys,yaml; yaml.safe_dump(json.load(sys.stdin), sys.stdout, sort_keys=False)" \
  > ../openapi.yaml
```

## Guardrails

- Never edit `ce-app/**` or `docs/CuttingEdge/**` (map C3).
- JP7, TDEE, macros = code only; the LLM never invents measurements (C6).
- Every new feature ships with a measurable test (C12).
