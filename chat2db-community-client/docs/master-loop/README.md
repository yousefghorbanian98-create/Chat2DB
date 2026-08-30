# Master Loop — Motion Package Switcher

فایل اجرای حلقهی یکپارچهسازی سوییچ پکیج موشن در پروژهی واقعی.

این فایل فقط آماده شده است.

حلقه با فرمان صریح زیر شروع میشود:

```
لوپ را شروع کن
```

تا آن زمان هیچ گیتی اجرا نمیشود.

## شروع حلقه

```bash
yarn install
node scripts/master-loop/run-loop.cjs
node scripts/master-loop/run-loop.cjs --list
node scripts/master-loop/run-loop.cjs --status
node scripts/master-loop/run-loop.cjs --phase typecheck
node scripts/master-loop/run-loop.cjs --continue-on-error
```

معنای کدهای خروجی:

```
0
```

همهی گیتهای اجراشده پاس شدند.

```
1
```

یک گیت شکست خورد.

```
2
```

خطای استفاده.

## نقشهی فازها

هر فاز یک گیت است؛ بدون پاس شدن آن، حلقه به فاز بعدی نمیرود.

| گیت | فرمان | تضمین |
|---|---|---|
| G1 | static | ۸ نقطهی اتصال سر جایشاناند؛ ایمپورت ممنوع در ماژول نیست؛ کلاسهای دمو نشتی ندارند |
| G2 | i18n-keys | هر ۱۱ کلید در هر ۵ فایل لوکال موجود است؛ placeholder ناخواسته نیست |
| G3 | typecheck | تایپها با tsconfig پروژه سازگارند |
| G4 | i18n-validate | اعتبارسنج رسمی i18n پاس است |
| G5 | build | تستهای prebuild و umi build و تأیید باندل موفق است |
| G6 | visual | سکشن باز میشود، سوییچ کار میکند، انتخاب ماندگار است |

جزئیات هر گیت:

```
G1
```

بازرسی استاتیک:

- هر دو layout شامل mount شدن

```
MotionPackageProvider
```

- منوی تنظیمات شامل آیتم

```
motionPackage
```

- فایلهای ماژول

```
src/motion-package/
```

موجودند.

```
G2
```

اسکن پنج فایل لوکال:

```
src/i18n/en-US/setting.ts
src/i18n/zh-CN/setting.ts
src/i18n/ja-JP/setting.ts
src/i18n/ko-KR/setting.ts
src/i18n/es-ES/setting.ts
```

```
G3
```

اجرای:

```
npx tsc --noEmit
```

```
G4
```

اجرای:

```
node scripts/validate-i18n.cjs
```

```
G5
```

اجرای:

```
yarn build:web:community
```

شامل بیست تست واحد پیش از build و تأیید باندل production.

```
G6
```

سرو خروجی production بیلد (ساختهشده در G5) روی پورت ۸۸۸۹ توسط:

```
scripts/master-loop/serve-dist.cjs
```

و سپس اسکریپت:

```
scripts/master-loop/verify-switch.mjs
```

دلیل استفاده از بیلد production بهجای سرور توسعه: سرور وبپک حدود ۲.۷ گیگابایت رم مصرف میکند و در کنار کرومیوم در سندباکسِ حدوداً ۴ گیگابایتی توسط هسته کشته میشود؛ سرو استاتیک سبک است و آرتیفکت واقعی را هم میسنجد.

تأییدهای بصری:

- دو کارت پکیج رندر میشوند.
- کلیک روی

```
Hyperreal

```

کارت فعال را عوض میکند.

- مقدار

```
chat2db.motionPackage
```

در localStorage نوشته میشود.

- متغیر

```
--mp-accent
```

روی root تغییر میکند.

- انتخاب بعد از ریلود میماند.

وضعیت هر گیت در این فایل ذخیره میشود:

```
scripts/master-loop/loop-state.json
```

## نقطههای اتصال

| فایل | نقش |
|---|---|
| src/motion-package/types.ts | تایپها و متادیتای دو پکیج و کلید ذخیرهسازی |
| src/motion-package/MotionPackageProvider.tsx | Provider گلوبال و اعمال CSS vars و ماندگاری |
| src/motion-package/MotionPackageSetting.tsx | سکشن تنظیمات با دو کارت |
| src/motion-package/motion-package.css | استایل اسکوپشدهی سکشن |
| src/layouts/GlobalLayout/CommunityLayout.tsx | mount شدن Provider در ادیشن community |
| src/layouts/GlobalLayout/index.tsx | mount شدن Provider در سایر ادیشنها |
| src/blocks/Setting/index.tsx | آیتم منوی motionPackage در گروه عمومی |
| src/i18n/<locale>/setting.ts | یازده کلید در هر پنج زبان |

## فازهای بعدی

پس از پاس شدن G1 تا G6:

- نصب وابستگیهای موشن طبق نقشهی

```
PLAN_VERBATIM.md
```

- اتصال کامپوننتهای واقعی هر پکیج (بخش B لودینگ و لندینگ، بخش C ادیتور، بخش D استایل).
- هر فاز بعدی نیز با گیت تأیید بصری و تایپچک بسته میشود.

## مرجعهای دمو

```
docs/master-loop/reference-PkgProvider.tsx
docs/master-loop/reference-SettingsPanel.tsx
docs/master-loop/reference-pkg.css
docs/master-loop/MOTION_AUDIT.md
```

این چهار فایل، سورس دموی تأییدشده هستند و مبنای انتقال کامپوننتها در فازهای بعدیاند.


## ورکفلو (CI)

فایل:

```
.github/workflows/master-loop.yml
```

در ریشهی مخزن قرار دارد و همین شش گیت را خودکار اجرا میکند.

محرکها:

```
push
```

به شاخهی

```
arena/01a05327-chat2db
```

(فقط وقتی فایلهای src یا ابزار حلقه تغییر کنند) و

```
workflow_dispatch
```

(اجرای دستی از تب

```
Actions

```

با دکمهی

```
Run workflow

```

).

مراحل ورکفلو:

- نصب وابستگیها با

```
yarn install --frozen-lockfile
```

با fallback به

```
registry.npmjs.org

```

اگر mirror در دسترس نبود.

- نصب

```
playwright

```

فقط برای گیت بصری (بدون تغییر در

```
package.json

```

یا

```
yarn.lock

```

).

- اجرای

```
node scripts/master-loop/run-loop.cjs
```

با

```
MASTER_LOOP_REQUIRE_PLAYWRIGHT=1

```

تا گیت بصری بهجای skip در نبود مرورگر fail شود.

- انتشار پچ تفاضلی بهصورت خودکار بهعنوان آرتیفکت:

```
master-loop-patch
```

پچ از diff بین

```
merge-base

```

با

```
origin/main

```

و

```
HEAD

```

روی مسیرهای یکپارچهسازی ساخته میشود.

دستور اجرای دستی از سندباکس:

```
gh workflow run "Master Loop — Motion Package Switcher"
```
