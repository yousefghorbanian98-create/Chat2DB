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
| arabic-reshaper | 3.0.1 | MIT | Persian letter-joining for PDFs |
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
| PersianSans-Regular.ttf (bundled) | Bitstream Vera / public-domain DejaVu | see note below |
| Barlow / Barlow Condensed | OFL | Google Fonts |
| Lucide icons (Phase 1) | ISC | lucide.dev |

## Policy reminders (map C9 / §12.6)

- **No AGPL code linked into the app process.** wger (AGPL) = ideas/data only.
  SocratiCode / OSS Compass stay on the dev machine.
- Prefer MIT/Apache/BSD/ISC/OFL inside the binary.

### Font provenance (read before claiming "Vazirmatn")

`mp-app/assets/fonts/PersianSans-Regular.ttf` is **DejaVu Sans 2.37**, *not*
Vazirmatn. It was found already present in the workspace
(`youtube-auto-uploader/resources/fonts/`, mislabelled `Vazirmatn-Regular.ttf`)
and verified with fontTools to cover every Arabic/Persian codepoint and
presentation form the reshaped report text needs (zero missing glyphs). It is
used because the sandbox cannot reach the Vazirmatn release artifacts; drop a
real Vazirmatn TTF next to it and set `MP_PERSIAN_FONT` to switch — the code
references the font only through `app/core/persian.PERSIAN_FONT`.

Deliberately **not** used: `python-bidi` (LGPL-3.0). C11 restricts the product to
permissive licenses, so RTL reordering is done by a small in-house UAX #9 subset
(`app/core/persian._display`, MIT) oracle-verified against python-bidi during
development, keeping `arabic-reshaper` (MIT) as the only runtime shaping dep.
