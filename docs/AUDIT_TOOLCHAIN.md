# استک ممیزی نهایی — ابزارهای اوپن‌سورس و کاملاً رایگان

> هدف: یک بار ممیزی کامل پروژه (بک‌اند + فرانت‌اند): سیم‌کشی‌ها، موتورها/ورک‌فلوها، خروجی توابع و پارامترها، همبستگی کلی و جزئی، انیمیشن‌ها و اینترکشن‌ها، تک‌تک دکمه‌ها و سرچ‌بارها، کد تکراری، ساده‌سازی توابع، کد مرده، و تست/استرس نهایی.
>
> همه‌ی داده‌های زیر (ستاره، لایسنس، آخرین کامیت) در **۲۰۲۶‑۱۱‑۱۸** از GitHub API / PyPI / Hugging Face API گرفته شده‌اند.
>
> **هیچ ابزار واحدی همه‌ی این کارها را با هم نمی‌کند.** راه‌حل واقعی، ترکیب لایه‌ای زیر است که با یک `Makefile` یا یک GitHub Action هماهنگ می‌شود.

---

## ۰) نگاشت سریع: خواسته ← ابزار

| خواسته‌ی شما | ابزار اصلی | مکمل |
|---|---|---|
| مستندسازی خط‌به‌خط + دیاگرام | repowise | DeepWiki‑Open، OpenWiki، GitDiagram |
| انتقال context به نشست AI بعدی | repowise (SessionStart hook + AGENTS.md خودکار) | OpenWiki، mattpocock/skills (Handoff) |
| «کدی روی کد دیگری نیفتاده باشد» | jscpd | PMD CPD، SonarQube duplication، MegaLinter COPYPASTE |
| کد مرده | knip (TS/React) + repowise dead code | dependency‑cruiser، madge |
| همبستگی کلی و جزئی | repowise call graph + ArchUnit | jQAssistant، dependency‑cruiser، import‑linter |
| سیم‌کشی‌ها / ورک‌فلوها / خروجی توابع | Schemathesis + Keploy + ArchUnit | Hurl، Prism |
| ساده‌سازی توابع | OpenRewrite (مکانیکی) + repowise refactoring plans | lizard (پیدا کردن توابع پیچیده)، ESLint `--fix` |
| تست «تک تک توابع و پارامترها» | Hypothesis / fast‑check / Randoop (property‑based) | JUnit + JaCoCo، Vitest |
| «اورلود» تست‌ها (آیا واقعاً باگ می‌گیرند؟) | PIT (Java) + Stryker (TS) — mutation testing | mutmut / cosmic‑ray (Python) |
| انیمیشن‌ها، اینترکشن‌ها، تک‌تک دکمه‌ها | Storybook (play/test‑runner) + Playwright | BackstopJS، Playwright `toHaveScreenshot` |
| سرچ‌بار و فرم‌ها | Playwright + fast‑check | Hypothesis برای منطق سمت سرور |
| کلاس جهانی: پرفورمنس/a11y/SEO | Lighthouse CI + axe‑core | web‑vitals، webpack‑bundle‑analyzer |
| بار و استرس واقعی | k6 | Locust، Gatling، oha، Toxiproxy |
| امنیت و رازها | Trivy + Gitleaks | Semgrep، Bandit، ZAP |
| یک دستور برای کل ممیزی | MegaLinter | reviewdog، pre‑commit |
| اجرای اصلاحات با AI رایگان | OpenHands + Qwen3‑Coder روی Ollama | aider |

---

## ۱) مستندسازی، دیاگرام، و انتقال context بین نشست‌ها

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [repowise‑dev/repowise](https://github.com/repowise-dev/repowise) | AGPL‑3.0 · ⭐8,171 · امروز | ایندکس محلی کدبیس: گراف فراخوانی با AST کامل در ۲۸ زبان (Java با دقت javac ≈0.90–1.00)، **ویکی برای هر فایل/سمبل/زیرسیستم/API contract/چرخه‌ی وابستگی/فایل زیرساخت**، نقشه‌ی معماری، نمای C4، خروجی Structurizr، **کد مرده**، **health score ۱–۱۰ هر فایل از ۵۳ دتکتور قطعی**، blast radius، hotspots، ownership، doc drift، استخراج تصمیم‌ها از ADR/کامنت `# WHY:`/کامیت/PR/**ترنسکریپت نشست ایجنت**، و ۱۰ ابزار MCP. بدون API key و با صفر تماس LLM کار می‌کند. `AGENTS.md` و `.claude/CLAUDE.md` را خودش می‌نویسد و به‌روز نگه می‌دارد. خروجی markdown با `repowise export`. |
| [AsyncFuncAI/deepwiki‑open](https://github.com/AsyncFuncAI/deepwiki-open) | MIT · ⭐18,454 · ۲۰۲۶‑۱۱‑۱۵ | آدرس مخزن GitHub/GitLab/Bitbucket (حتی private) را می‌گیرد و ویکی چندصفحه‌ای با **دیاگرام Mermaid خودکار** (معماری، جریان داده، sequence) + پنل «Ask» با RAG + حالت Deep Research می‌سازد. خروجی Markdown/JSON که قابل کامیت در `docs/` است. با Ollama کاملاً رایگان/آفلاین. |
| [langchain‑ai/openwiki](https://github.com/langchain-ai/openwiki) | MIT · ⭐18,012 · امروز | CLI که **مستندات مخصوص ایجنت** را برای مخزن می‌نویسد و **نگه می‌دارد**: ویکی می‌سازد و بعد به `AGENTS.md`/`CLAUDE.md` شما ارجاع به آن ویکی اضافه می‌کند تا ایجنت به‌جای بلعیدن صد صفحه، فقط چیزی را که لازم دارد بازیابی کند. |
| [ahmedkhaleel2004/gitdiagram](https://github.com/ahmedkhaleel2004/gitdiagram) | MIT · ⭐18,981 · ۲۰۲۶‑۱۱‑۱۷ | از هر مخزن گیت‌هاب یک **دیاگرام معماری تعاملی** می‌سازد (کلیک روی هر جزء ← پرش به فایل/دایرکتوری مربوطه)، خروجی PNG یا Mermaid، و یک ویدیوی توضیحی ~۱ دقیقه‌ای. در URL گیت‌هاب کلمه‌ی `hub` را با `diagram` عوض کنید. Self‑host با کلید خودتان. |
| [oraios/serena](https://github.com/oraios/serena) | GPL‑3.0‑or‑later · ⭐31,493 · ۲۰۲۶‑۱۱‑۱۵ | ابزار MCP برای دسترسی **سطح سمبل** به کد (find symbol / references / rename / replace body) با زبان‌سرور ۴۰+ زبان. مستند نمی‌سازد؛ مصرف توکن ایجنت را به‌شدت پایین می‌آورد. |
| [yamadashy/repomix](https://github.com/yamadashy/repomix) | MIT · ⭐29,309 · امروز | کل مخزن را در **یک فایل AI‑friendly** بسته‌بندی می‌کند (با شمارش توکن و فیلتر). برای پروژه‌های کوچک/متوسط یا برای دادن کل context در یک پیام. |
| [coderamp‑labs/gitingest](https://github.com/coderamp-labs/gitingest) | MIT · ⭐16,151 · امروز | در URL گیت‌هاب `hub` را با `ingest` عوض کنید → prompt آماده‌ی LLM از کل مخزن. |
| [mufeedvh/code2prompt](https://github.com/mufeedvh/code2prompt) | MIT · ⭐7,768 · ۲۰۲۶‑۱۱‑۰۶ | CLI برای تبدیل کدبیس به یک prompt واحد، با قالب‌های آماده و شمارش توکن. |
| [The‑Pocket/PocketFlow‑Tutorial‑Codebase‑Knowledge](https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge) | MIT · ⭐12,764 · ۲۰۲۶‑۰۵‑۳۱ | خط‌لوله‌ی LLM که مخزن را می‌خزد، انتزاع‌های هسته‌اش را پیدا می‌کند و یک **آموزش گام‌به‌گام markdown** می‌نویسد (خروجی = فایل، قابل کامیت). |
| [mattpocock/skills](https://github.com/mattpocock/skills) | MIT · ⭐327,168 · امروز | مجموعه skill برای ایجنت‌های کدنویس؛ مهم‌ترینش برای شما **Handoff**: نشست فعلی را به یک markdown ساختاریافته فشرده می‌کند تا در نشست/ایجنت دیگر ادامه دهید. |

---

## ۲) ارکستراتور و دروازه‌ی کیفیت

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [oxsecurity/megalinter](https://github.com/oxsecurity/megalinter) | AGPL‑3.0 · ⭐2,658 · امروز | **یک دستور، ۱۲۴ لینتر**: ۶۸ زبان + ۲۳ فرمت + ۲۲ فرمت ابزار. شامل لینتر **COPYPASTE** (زیرش jscpd) برای کد تکراری، ESLint/Stylelint/CSS/HTML/Markdown/SPELL و… خروجی SARIF + HTML. اجرای محلی با `docker run` یا به‌صورت GitHub Action. دارای LLM Advisor و ساب‌ایجنت‌های `megalinter-check` / `megalinter-fix`. |
| [SonarSource/sonarqube](https://github.com/SonarSource/sonarqube) | LGPL‑3.0 · ⭐11,195 · دیروز | Community Edition رایگان و self‑host: code smell، **duplication**، پیچیدگی، پوشش تست، security hotspot و **Quality Gate** (قبول/رد خودکار بیلد). |
| [reviewdog/reviewdog](https://github.com/reviewdog/reviewdog) | MIT · ⭐9,751 · امروز | خروجی هر ابزار تحلیلی را به **کامنت روی خطِ PR** تبدیل می‌کند؛ یعنی گزارش ممیزی دقیقاً روی همان خط کد. |
| [pre‑commit/pre‑commit](https://github.com/pre-commit/pre-commit) | MIT · ⭐15,703 · ۲۰۲۶‑۱۱‑۰۹ | قاب مدیریت hookهای چندزبانه؛ ممیزی را قبل از هر کامیت اجرا می‌کند تا کد کثیف وارد تاریخچه نشود. |
| [The‑PR‑Agent/pr‑agent](https://github.com/The-PR-Agent/pr-agent) | Apache‑2.0 · ⭐16,366 · امروز | بازبین خودکار PR اوپن‌سورس (`/review`, `/describe`, `/improve`)؛ برای بازبینی پاس‌های ریفکتور بزرگ. |

---

## ۳) معماری، همبستگی و گراف وابستگی

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [TNG/ArchUnit](https://github.com/TNG/ArchUnit) | Apache‑2.0 · ⭐3,901 · دیروز | قوانین معماری Java را به **تست JUnit** تبدیل می‌کند: «لایه‌ی controller نباید مستقیم به mapper دسترسی داشته باشد»، «هیچ چرخه‌ای بین پکیج‌ها نباشد»، «همه‌ی سرویس‌ها `@Transactional` داشته باشند». نقض ← تست قرمز. |
| [jQAssistant/jqassistant](https://github.com/jQAssistant/jqassistant) | GPL‑3.0 · ⭐301 · امروز | کل کدبیس Java (کلاس‌ها، متدها، وابستگی‌ها، pom، SQL schema) را به گراف **Neo4j** می‌ریزد؛ بعد با Cypher هر سؤال جزئی را می‌پرسید و قانون معماری را به‌عنوان constraint تعریف می‌کنید. |
| [sverweij/dependency‑cruiser](https://github.com/sverweij/dependency-cruiser) | MIT · ⭐7,440 · امروز | برای JS/TS: اعتبارسنجی وابستگی‌ها با **قواعد دلخواه شما**، تشخیص چرخه، و مصورسازی گراف (dot/mermaid/html). |
| [pahen/madge](https://github.com/pahen/madge) | MIT · ⭐10,186 · ۲۰۲۶‑۰۱‑۲۱ | گراف وابستگی ماژول‌های JS/TS و فهرست **چرخه‌های وابستگی** (`madge --circular src`). |
| [import‑linter/import‑linter](https://github.com/import-linter/import-linter) | BSD‑2‑Clause · ⭐1,267 · امروز | همان ArchUnit برای **پایتون**: لایه‌بندی و ممنوعیت import را به قانون قابل تست تبدیل می‌کند. |
| [CoatiSoftware/Sourcetrail](https://github.com/CoatiSoftware/Sourcetrail) | GPL‑3.0 · ⭐16,454 · **آرشیو (۲۰۲۱)** | کاوشگر بصری تعاملی کد (کلاس/فراخوانی/ارجاع). نگهداری نمی‌شود؛ فقط برای گشت‌وگذار دستی مفید است. |

---

## ۴) کد مرده، کد تکراری، پیچیدگی، باگ‌های الگویی

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [webpro‑nl/knip](https://github.com/webpro-nl/knip) | ISC · ⭐12,692 · امروز | **کد مرده‌ی JS/TS/React**: فایل‌های استفاده‌نشده، export‌های بی‌مصرف، وابستگی‌های بلااستفاده، typeهای مرده. با `--fix` بخشی را خودش پاک می‌کند. |
| [kucherenko/jscpd](https://github.com/kucherenko/jscpd) | MIT · ⭐6,574 · امروز | **تشخیص کپی/پیست در ۲۲۰+ زبان** با موتور Rust؛ همزمان Java و TypeScript را می‌بیند. خروجی HTML/SARIF/console و آستانه‌ی درصد تکرار. |
| [terryyin/lizard](https://github.com/terryyin/lizard) | ⭐2,604 · امروز | پیچیدگی cyclomatic و طول توابع در چند زبان (Java, C/C++, Python, JS, …)؛ فهرست توابعی که باید ساده شوند (`lizard -C 15 -T cyclomatic_complexity=15`). |
| [pmd/pmd](https://github.com/pmd/pmd) | ⭐5,534 · امروز | تحلیلگر ایستا چندزبانه + **CPD** (تشخیص کد تکراری برای Java/Kotlin/JS/…) و قواعد «خدای کلاس»، پارامتر زیاد، متد طولانی. |
| [spotbugs/spotbugs](https://github.com/spotbugs/spotbugs) | LGPL‑2.1 · ⭐3,968 · دیروز | جانشین FindBugs؛ باگ‌های الگویی JVM (منابع بسته‌نشده، NPE محتمل، همزمانی نادرست). |
| [google/error‑prone](https://github.com/google/error-prone) | Apache‑2.0 · ⭐7,274 · امروز | اشتباهات رایج Java را **در زمان کامپایل** به خطا تبدیل می‌کند (پلاگین javac). |
| [semgrep/semgrep](https://github.com/semgrep/semgrep) | LGPL‑2.1 · ⭐17,794 · امروز | تحلیل الگویی سبک برای چند زبان؛ عالی برای قواعد سفارشی «این الگو در کد من ممنوع» و hotspotهای امنیتی. |
| [astral‑sh/ruff](https://github.com/astral-sh/ruff) | MIT · ⭐51,288 · امروز | لینتر + فرمتر فوق‌سرع پایتون (Rust)؛ اگر بخشی از پروژه پایتون است. |
| [rubik/radon](https://github.com/rubik/radon) | MIT · ⭐2,045 · ۲۰۲۴‑۱۰‑۲۰ (کم‌فعال) | متریک‌های پیچیدگی و maintainability index برای پایتون. |

---

## ۵) ساده‌سازی و ریفکتور خودکارِ امن

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [openrewrite/rewrite](https://github.com/openrewrite/rewrite) | Apache‑2.0 · ⭐3,993 · امروز | **ریفکتور انبوه خودکار** روی Java/Kotlin/TS/XML/YAML با حفظ معنا: ساده‌سازی، مهاجرت نسخه، یکدست‌سازی الگو، حذف کد مرده‌ی قطعی. تغییرات مکانیکی و قابل بازگشت، نه حدس LLM. |
| ESLint `--fix` + Prettier | MIT | پاس یکدست‌سازی سبک و اصلاح خودکار مسائل قابل‌رفع در فرانت‌اند. |
| repowise `REFACTORING` | AGPL‑3.0 | برنامه‌ی ریفکتور مشخص (Extract Method / Extract Class / Move Method / Split File / **Break Cycle**) با نام دقیق سمبل‌هایی که جابه‌جا می‌شوند — آماده‌ی تحویل به ایجنت. |

---

## ۶) تست: پوشش، property‑based، و «اورلود» تست‌ها با mutation

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [jacoco/jacoco](https://github.com/jacoco/jacoco) | ⭐4,618 · دیروز | اندازه‌گیری پوشش تست Java (خط/شاخه/متد)؛ ورودی لازم برای mutation testing و Quality Gate. |
| [vitest‑dev/vitest](https://github.com/vitest-dev/vitest) | MIT · ⭐17,393 · امروز | فریمورک تست واحد/یکپارچگی فرانت‌اند با پوشش داخلی و سرعت Vite. |
| [hcoles/pitest](https://github.com/hcoles/pitest) | Apache‑2.0 · ⭐1,893 · دیروز | **Mutation testing روی JVM**: باگ مصنوعی در بایت‌کد تزریق می‌کند و می‌سنجد تست‌هایتان چند درصد را می‌گیرند. تنها معیار واقعی «تست‌ها کار می‌کنند». |
| [stryker‑mutator/stryker‑js](https://github.com/stryker-mutator/stryker-js) | Apache‑2.0 · ⭐3,391 · دیروز | همان mutation testing برای JavaScript/TypeScript/React. |
| [boxed/mutmut](https://github.com/boxed/mutmut) | BSD‑3‑Clause · ⭐1,547 · امروز | mutation testing برای پایتون. |
| [sixty‑north/cosmic‑ray](https://github.com/sixty-north/cosmic-ray) | MIT · ⭐667 · امروز | mutation testing موازی و توزیع‌شده برای پایتون. |
| [HypothesisWorks/hypothesis](https://github.com/HypothesisWorks/hypothesis) | MPL‑2.0 · ⭐9,186 · امروز | **property‑based testing** پایتون: به‌جای مثال دستی، ویژگیِ تابع را می‌گویید و خودش هزاران ورودی (شامل حالات لبه) تولید می‌کند. |
| [dubzzz/fast‑check](https://github.com/dubzzz/fast-check) | MIT · ⭐5,283 · دیروز | property‑based برای JS/TS — مناسب «تک تک توابع و پارامترها» و منطق سرچ‌بار/فرم‌ها. |
| [randoop/randoop](https://github.com/randoop/randoop) | MIT · ⭐602 · امروز | تولید خودکار تست بازخوردمحور برای Java (کشف crash و استثنا بدون نوشتن تست دستی). |
| [EvoSuite/evosuite](https://github.com/EvoSuite/evosuite) | LGPL‑3.0 · ⭐924 · **رکود از ۲۰۲۵‑۰۲** | تولید خودکار سوئیت JUnit با الگوریتم ژنتیک. فقط به‌عنوان مرجع. |

---

## ۷) API و سیم‌کشی‌ها: قرارداد، mock، فازی، ضبط ترافیک، DAST

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [schemathesis/schemathesis](https://github.com/schemathesis/schemathesis) | MIT · ⭐3,786 · دیروز | از روی **OpenAPI/GraphQL** خودش تست می‌سازد و endpointها را می‌کوبد: 500، crash، نقض قرارداد، نوع اشتباه، پاسخ نامعتبر. «Catch API bugs before your users do». |
| [keploy/keploy](https://github.com/keploy/keploy) | Apache‑2.0 · ⭐19,885 · امروز | **ترافیک واقعی API را ضبط** و به تست‌های رگرسیون + mock وابستگی‌ها تبدیل می‌کند. بهترین راه برای «سیم‌کشی‌ها و ورک‌فلوها یک بار تست شوند» بدون نوشتن تست دستی. |
| [Orange‑OpenSource/hurl](https://github.com/Orange-OpenSource/hurl) | Apache‑2.0 · ⭐19,330 · امروز | نوشتن و اجرای تست HTTP با فایل متنی ساده + assert روی وضعیت/هدر/JSON؛ سریع، بدون وابستگی، مناسب CI. |
| [stoplightio/prism](https://github.com/stoplightio/prism) | Apache‑2.0 · ⭐5,072 · ۲۰۲۶‑۱۱‑۱۳ | از روی OpenAPI یک سرور mock می‌سازد و درخواست‌ها را **اعتبارسنجی** می‌کند (contract validation بین فرانت و بک‌اند). |
| [zaproxy/zaproxy](https://github.com/zaproxy/zaproxy) | Apache‑2.0 · ⭐16,220 · امروز | اسکن پویا (DAST) برنامه‌ی در حال اجرا: تزریق، XSS، تنظیمات ناامن، کشف خودکار مسیرها. |
| [apiaryio/dredd](https://github.com/apiaryio/dredd) | MIT · ⭐4,210 · **آرشیو (۲۰۲۴)** | تست API نسبت به spec — جایگزین زنده: Schemathesis / Hurl. |

---

## ۸) فرانت‌اند: کامپوننت، اینترکشن، انیمیشن، بصری، دسترس‌پذیری، پرفورمنس

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [microsoft/playwright](https://github.com/microsoft/playwright) | Apache‑2.0 · ⭐100,478 · امروز | E2E چندمرورگری؛ `toHaveScreenshot()` برای **رگرسیون بصری**، Trace Viewer برای دیدن ثانیه‌به‌ثانیه‌ی انیمیشن، و تستی که روی **تک‌تک دکمه‌ها/ورودی‌ها** کلیک کند و خطای کنسول و درخواست شکست‌خورده‌ی شبکه را بگیرد. کاملاً رایگان. |
| [storybookjs/storybook](https://github.com/storybookjs/storybook) | MIT · ⭐91,624 · امروز | کارگاه ایزوله‌ی کامپوننت‌ها + **play functions و test‑runner**: هر کامپوننت در هر state (hover/focus/disabled/loading/error) مستند و تست می‌شود. نزدیک‌ترین ابزار به «تک تک دکمه‌ها و انیمیشن‌ها». |
| [garris/BackstopJS](https://github.com/garris/BackstopJS) | MIT · ⭐7,205 · ۲۰۲۶‑۱۰‑۱۰ | رگرسیون بصری مبتنی بر سناریو (کلیک/اسکرول/viewport مختلف) با گزارش diff تصویری. |
| [dequelabs/axe‑core](https://github.com/dequelabs/axe-core) | MPL‑2.0 · ⭐7,849 · دیروز | موتور تست دسترس‌پذیری (قابل اجرا داخل Playwright/Storybook). |
| [pa11y/pa11y](https://github.com/pa11y/pa11y) | LGPL‑3.0 · ⭐4,602 · دیروز | تست خودکار دسترس‌پذیری صفحات با خروجی CI‑پسند. |
| [microsoft/accessibility‑insights‑web](https://github.com/microsoft/accessibility-insights-web) | MIT · ⭐965 · ۲۰۲۶‑۱۱‑۰۳ | ممیزی a11y با راهنمای رفع و اسکن خودکار صفحه. |
| [GoogleChrome/lighthouse‑ci](https://github.com/GoogleChrome/lighthouse-ci) | Apache‑2.0 · ⭐7,154 · دیروز | Lighthouse روی هر کامیت + **بودجه‌ی پرفورمنس**: اگر باندل بزرگ‌تر شد یا LCP/accessibility افت کرد، بیلد قرمز. |
| [GoogleChrome/web‑vitals](https://github.com/GoogleChrome/web-vitals) | Apache‑2.0 · ⭐8,693 · ۲۰۲۶‑۱۱‑۱۲ | اندازه‌گیری متریک‌های واقعی کاربر (LCP/INP/CLS) از داخل برنامه. |
| [webpack/webpack‑bundle‑analyzer](https://github.com/webpack/webpack-bundle-analyzer) | MIT · ⭐12,656 · دیروز | نقشه‌ی تعاملی حجم باندل؛ پیدا کردن وابستگی‌های سنگین و تکراری. |
| [SeleniumHQ/selenium](https://github.com/SeleniumHQ/selenium) | Apache‑2.0 · ⭐34,595 · امروز | اتوماسیون مرورگر کلاسیک؛ فقط اگر زیرساخت تست قدیمی دارید (وگرنه Playwright). |
| [lost‑pixel/lost‑pixel](https://github.com/lost-pixel/lost-pixel) | MIT · ⭐1,679 · **آرشیو شده** | جایگزین Percy/Chromatic — استفاده نکنید؛ Playwright/BackstopJS کافی است. |

---

## ۹) بار، استرس و آشوب («اورلود» واقعی برنامه)

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [grafana/k6](https://github.com/grafana/k6) | AGPL‑3.0 · ⭐32,345 · امروز | تست بار با سناریوی JavaScript، آستانه‌گذاری (`p95 < 300ms`)، خروجی CI و داشبورد. |
| [locustio/locust](https://github.com/locustio/locust) | MIT · ⭐28,295 · ۲۰۲۶‑۱۱‑۱۶ | تست بار توزیع‌شده با پایتون خالص + UI زنده. |
| [gatling/gatling](https://github.com/gatling/gatling) | Apache‑2.0 · ⭐6,964 · دیروز | Load Testing as Code روی JVM؛ گزارش‌های تحلیلی قوی. |
| [apache/jmeter](https://github.com/apache/jmeter) | Apache‑2.0 · ⭐9,608 · ۲۰۲۶‑۱۱‑۰۵ | ابزار کلاسیک تست بار/عملکرد برای HTTP، JDBC، صف‌ها. |
| [hatoo/oha](https://github.com/hatoo/oha) | MIT · ⭐10,693 · امروز | بارگذار HTTP سبک با TUI و نمودار زنده؛ برای چک سریع یک endpoint. |
| [mcollina/autocannon](https://github.com/mcollina/autocannon) | MIT · ⭐8,544 · دیروز | بنچمارک سریع HTTP/1.1 در Node.js. |
| [Shopify/toxiproxy](https://github.com/Shopify/toxiproxy) | MIT · ⭐12,538 · دیروز | پروکسی TCP برای شبیه‌سازی latency/قطعی/محدودیت پهنای باند؛ تست رفتار برنامه زیر شبکه‌ی خراب. |

---

## ۱۰) امنیت، رازها و وابستگی‌ها

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [aquasecurity/trivy](https://github.com/aquasecurity/trivy) | Apache‑2.0 · ⭐39,496 · امروز | اسکن CVE در وابستگی‌ها، ایمیج داکر، IaC و misconfiguration + تولید SBOM + کشف رازها. |
| [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | MIT · ⭐31,155 · ۲۰۲۶‑۱۰‑۲۸ | پیدا کردن کلید/توکن/راز در working tree و **کل تاریخچه‌ی git**. |
| [PyCQA/bandit](https://github.com/PyCQA/bandit) | Apache‑2.0 · ⭐8,393 · ۲۰۲۶‑۱۱‑۰۹ | مسائل امنیتی رایج پایتون. |
| repowise `SECURITY` | AGPL‑3.0 | رازها و فراخوانی‌های پرخطر در درخت کاری و تاریخچه + pre‑commit check + گیت CI. |

---

## ۱۱) ایجنت اوپن‌سورس + مدل رایگان برای اجرای اصلاحات

| پروژه | لایسنس / ستاره / آخرین کامیت | چه می‌کند |
|---|---|---|
| [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) | MIT · ⭐93,723 · امروز | ایجنت توسعه‌ی خودران:issue را می‌گیرد، کد می‌نویسد، کامند اجرا می‌کند و PR می‌دهد. مناسب پاس‌های تکراری ریفکتور با مدل محلی. |
| [Aider‑AI/aider](https://github.com/Aider-AI/aider) | Apache‑2.0 · ⭐50,164 · ۲۰۲۶‑۰۵‑۲۲ | جفت‌برنامه‌نویسی در ترمینال، git‑native؛ ریفکتور چندفایلی با کامیت خودکار. |
| [plandex‑ai/plandex](https://github.com/plandex-ai/plandex) | MIT · ⭐15,922 · ۲۰۲۵‑۱۰‑۰۳ (نیمه‌رکود) | ایجنت کدنویس مخصوص پروژه‌های بزرگ با diff کنترل‌شده. |
| [Qwen/Qwen3‑Coder‑30B‑A3B‑Instruct](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) | Apache‑2.0 · ~1.94M دانلود | مدل کُد بازِ روی Hugging Face؛ با GGUF (`unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF`) روی ~24GB VRAM یا CPU اجرا می‌شود → **پاس‌های ریفکتور نامحدود و رایگان** از طریق Ollama/vLLM. |
| [qodo‑ai/qodo‑cover](https://github.com/qodo-ai/qodo-cover) | AGPL‑3.0 · ⭐5,689 · **no longer maintained از ۲۰۲۵‑۰۶‑۱۵** | تولید تست با AI که فقط تستی را نگه می‌دارد که پوشش را واقعاً بالا ببرد. به‌عنوان **مرجع الگو** ارزشمند است، نه به‌عنوان وابستگی. |

> **نقش Hugging Face:** آنجا ابزار ممیزی پیدا نمی‌کنید؛ مدل رایگان برای پاسِ اصلاح پیدا می‌کنید. الگوی درست = ممیزی با ابزارهای قطعی (لایه‌های ۲ تا ۱۰) + اصلاح با مدل محلی (لایه‌ی ۱۱).

---

## ۱۲) هسته‌ی حداقلی برای پروژه‌ی شما (Java 17 / Spring Boot / React‑TS)

اگر فقط ده ابزار نصب کنید، این‌ها:

1. **repowise** — نقشه، کد مرده، health، blast radius، AGENTS.md خودکار، تحویل به نشست بعد
2. **MegaLinter** — ۱۲۴ لینتر + کد تکراری با یک `docker run`
3. **SonarQube Community** — Quality Gate دائمی
4. **ArchUnit** — قوانین معماری بک‌اند به‌صورت تست
5. **knip** — کد مرده‌ی فرانت‌اند
6. **PIT + Stryker** — mutation testing: آیا تست‌ها واقعاً باگ می‌گیرند؟
7. **Schemathesis (+ Keploy)** — کوبیدن API از روی spec / ضبط ترافیک واقعی
8. **Playwright + Storybook** — تک‌تک دکمه‌ها، اینترکشن‌ها، انیمیشن‌ها، رگرسیون بصری
9. **Lighthouse CI + axe‑core** — پرفورمنس و دسترس‌پذیری در سطح کلاس جهانی
10. **k6** — بار و استرس

به‌علاوه برای پاس اصلاح: **OpenRewrite** (ریفکتور مکانیکی Java) و **Trivy + Gitleaks** (امنیت).

### Makefile پیشنهادی

```makefile
AUDIT := .audit
.PHONY: audit map lint dup dead-fe quality mutate api ui load refactor

audit: map lint dup dead-fe quality mutate api ui load   ## ممیزی کامل

map:      ## نقشه + کد مرده + health (بدون API key)
	repowise init --yes --no-prose && repowise export --format markdown

lint:     ## ۱۲۴ لینتر + کد تکراری
	docker run --rm -v "$$(pwd)":/tmp/lint oxsecurity/megalinter:latest

dup:      ## کپی/پیست بین Java و TS
	npx jscpd --threshold 3 --reporters html,consoleFull --output $(AUDIT)/jscpd .

dead-fe:  ## کد مرده‌ی فرانت
	npx knip --reporter json > $(AUDIT)/knip.json

quality:  ## دروازه‌ی کیفیت
	docker compose -f docker/sonar.yml up -d && mvn sonar:sonar

mutate:   ## اورلودِ تست‌ها — حتماً قبل از ریفکتور
	mvn org.pitest:pitest-maven:mutationCoverage
	npx stryker run stryker.conf.json

api:      ## کوبیدن API از روی spec
	st run --checks all http://localhost:8080/v3/api-docs

ui:       ## فرانت: E2E + بصری + a11y + Lighthouse
	npx playwright test && npx @lhci/cli autorun

load:     ## استرس
	k6 run perf/scenarios.js

refactor: ## ساده‌سازی مکانیکی، فقط وقتی همه‌چیز سبز است
	mvn -Prewrite rewrite:run && npx knip --fix
```

### ترتیب حیاتی

1. اول **mutation testing** (قدم ۶) — اگر تست‌ها باگ مصنوعی را نگیرند، هر «ساده‌سازی» یعنی شکستن بی‌صدای برنامه.
2. بعد **ریفکتور** (قدم ۱۰) با diff کوچک، تست سبز، و یک کامیت به ازای هر پاس.
3. هر یافته را در `docs/audit/findings-<date>.md` با اولویت (P0 بلاکر / P1 پیش از انتشار / P2 بدهی) ثبت کنید تا نشست AI بعدی از همان‌جا ادامه دهد.

---

## ۱۳) از این‌ها استفاده نکنید (آرشیو/رکود)

`lost-pixel/lost-pixel` (آرشیو) · `apiaryio/dredd` (آرشیو) · `CoatiSoftware/Sourcetrail` (آرشیو ۲۰۲۱) · `jeremylong/DependencyCheck` (مخزن منتقل/آرشیو — Trivy جایگزین) · `qodo-ai/qodo-cover` (unmaintained) · `EvoSuite/evosuite` (رکود از ۲۰۲۵‑۰۲) · `danvk/source-map-explorer` (رکود از ۲۰۲۳ — webpack‑bundle‑analyzer جایگزین).
