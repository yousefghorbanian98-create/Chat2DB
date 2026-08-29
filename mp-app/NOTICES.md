# MP third-party notices (stub — Phase 0)

Map §20 requires an About screen listing OSS licenses. This is the seed list for
what Phase 0 actually pulls in; it must grow with every dependency.

## Runtime (shipped inside the product)

| Package | Version | License | Used for |
|---------|---------|---------|----------|
| fastapi | 0.141.1 | MIT | local HTTP core |
| uvicorn | 0.52.4 | BSD-3 | ASGI server on :8751 |
| starlette | 1.6.0 | BSD-3 | (fastapi dependency) |
| sqlalchemy | 2.0.52 | MIT | SQLite access |
| pydantic | 2.13.5 | MIT | validation |
| reportlab | 5.0.1 | BSD-3 | PDF assessment reports |
| react | 18.3.1 | MIT | Studio renderer |
| react-dom | 18.3.1 | MIT | Studio renderer |
| framer-motion | 12.x | MIT | motion system |

## Dev-only (never shipped inside the gym binary)

| Package | Version | License |
|---------|---------|---------|
| pytest | 9.1.1 | MIT |
| httpx | 0.28.1 | BSD-3 |
| pyyaml | 6.x | MIT |
| vitest | 3.2.7 | MIT |
| vite | 6.4.3 | MIT |
| typescript | 5.9.x | Apache-2.0 |
| jsdom | 25.x | MIT |
| @testing-library/* | — | MIT |

## Design assets

| Asset | License | Source |
|-------|---------|--------|
| UI/UX Pro Max Skill | MIT | github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| Vazirmatn font | OFL | github.com/rastikerdar/vazirmatn |
| Barlow / Barlow Condensed | OFL | Google Fonts |
| Lucide icons (Phase 1) | ISC | lucide.dev |

## Policy reminders (map C9 / §12.6)

- **No AGPL code linked into the app process.** wger (AGPL) = ideas/data only.
  SocratiCode / OSS Compass stay on the dev machine.
- Prefer MIT/Apache/BSD/ISC/OFL inside the binary.
