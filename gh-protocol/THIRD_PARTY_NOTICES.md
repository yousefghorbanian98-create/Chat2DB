# Third-party notices — Gh Protocol (Android)

This file records every external asset or code fragment that ships inside the APK, with its
upstream source, license and where it is actually used. Anything imported must appear here
**and** be visible on a real screen (requirement 7: no decorative imports that no user sees).

---

## 1. DefyxVPN — vector icons, logo and Compose motion code

- **Upstream:** <https://github.com/UnboundTechCo/defyxVPN> (checked 2026-10-26, not archived,
  ~880 stars)
- **License:** **MIT** — "Copyright (c) 2025 UnboundTechCo"
  (<https://github.com/UnboundTechCo/defyxVPN/blob/main/LICENSE>)
- **How it is used here:** the shield/connection button, the header section, the radial glow
  buttons and the main-screen background are Kotlin/Compose ports of the upstream Flutter
  widgets; `defyx_logo.png` and the `ic_defyx_*` vectors are converted copies of
  `assets/icons/*.svg`.

| file | upstream | where it is displayed |
|---|---|---|
| `app/src/main/res/drawable/defyx_logo.png` | `assets/logo.png` | `MotionComponents.kt` header (HomeScreen §1) |
| `app/src/main/res/drawable/ic_defyx_shield.xml`, `ic_defyx_shield_solid.xml` | `assets/icons/Shield.svg` | `MotionComponents.kt` connection button |
| `app/src/main/res/drawable/ic_defyx_vpn_cloud.xml`, `ic_defyx_speed.xml` | `assets/icons/*.svg` | HomeScreen §3 (radar / ping buttons) |
| `app/src/main/res/drawable/ic_defyx_check.xml`, `_check_circle`, `_copy`, `_loading`, `_reload`, `_standby`, `_wifi`, `_arrow_left` | `assets/icons/*.svg` | Live-log + status components |
| `app/src/main/java/com/ghprotocol/app/ui/MotionComponents.kt` | `main_screen.dart`, `connection_button.dart`, `header_section.dart`, `main_screen_background.dart`, `app_colors.dart` | HomeScreen (port) |

Every remaining `ic_defyx_*` file has at least one `R.drawable.ic_defyx_*` reference in
`app/src/main/java`; assets with no reference were removed in this change
(`ic_defyx_error`, `ic_defyx_import_api`, `ic_defyx_info`, `ic_defyx_no_wifi`,
`ic_defyx_settings`, `ic_defyx_share`, `defyx_messages.png`, `defyx_splash_dark_logo.png`),
verified with a repository-wide grep before deletion.

### MIT license text (as distributed by the upstream project)

```
MIT License

Copyright (c) 2025 UnboundTechCo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 2. Serverless-for-Iran subscription templates

- **Upstream:** <https://github.com/patterniha/Serverless-for-Iran>
  (`Subscription/Serverless-for-Iran.json`, profiles `Serverless-v52-fragA` / `fragB`)
- **License:** see the upstream repository's own terms; the JSON is embedded **unmodified** as
  a fallback (`domain/Subscription.kt`, `EMBEDDED_FALLBACK_JSON`) and every runtime change is
  applied by `core/ConfigPatcher.kt` at start-up, never by editing the template.
- **Attribution:** shown in the app's profile list (`remarks`) and in `README.md`.

---

## 3. Xray-core

- **Upstream:** <https://github.com/XTLS/Xray-core>, license **MPL-2.0**.
- The Android arm64/x86_64 binaries are **not** committed (`app/src/main/jniLibs` and
  `assets/xray` are gitignored); `ci-fetch-xray.sh` downloads them from a pinned GitHub release
  and verifies SHA-256 before the build (`d81604f3…` arm64, `58546b1a…` amd64).
