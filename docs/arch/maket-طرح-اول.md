# پرامپتِ Maket.ai — طرح اول (مختلط: ۴ مغازه + ۳ طبقهٔ مسکونی)

این فایلِ مرجعِ گفت‌وگو با Maket است. همهٔ اعداد از `tools/plan_schemes.py` استخراج
شده‌اند، پس اگر خروجیِ Maket با جدولِ «معیارهایِ راستی‌آزمایی» در این فایل نخواند،
همان را با پرامپتِ اصلاحیِ بخشِ ۴ برگردانید.

---

## ۰) دو نکته قبل از چسباندن

1. Maket رویِ ورودیِ **انگلیسی** خیلی بهتر کار می‌کند؛ پرامپت‌ها را عیناً به انگلیسی
   بچسبانید. واحد را در خودِ پرامپت متر نوشته‌ایم تا متریک بماند.
2. در پلنِ رایگان فقط **یک طبقه** ساخته می‌شود (۵۰ کردیت). برایِ هر چهار تراز، یا
   چهار پروژهٔ تک‌طبقه بسازید، یا پلنِ پولی (multi-floor). اگر رایگان کار کرد،
   از «پرامپتِ نسخهٔ تک‌صفحه‌ای» (بخش ۵) استفاده کنید.
3. «zoning check» که Maket نشان می‌دهد بر مبنایِ ضوابطِ آمریکاست. ضوابطِ اصفهان
   (مادهٔ ۱۰۰، تراکم ۱۸۰٪، پس‌رفت ۲٫۶۷ m) را **هرگز** از آن نپرسید و به خروجی‌اش
   در این مورد اعتماد نکنید.

---

## ۱) پرامپتِ اصلی — نسخهٔ کامل (پروژهٔ چهارتراز)

```
Generate a four-level residential-over-commercial building in Isfahan, Iran.
Units: METRES throughout. Do not convert to feet.

SITE AND ENVELOPE
- Land: 40.57 m (east-west) x 13.37 m (north-south), 542.38 m2, flat, dry soil.
- Front (south) setback 2.67 m is a veranda/ balcony zone; the north line is a
  shared boundary wall with a 6.00 m rear lane behind it.
- Building footprint per floor: 40.55 m x 10.70 m = 433.9 m2 (80% site coverage,
  the maximum allowed). The footprint must be identical on all four levels.
- Floor heights: ground floor (shops) 4.50 m clear-to-clear; levels 1-3 2.90 m;
  parapet 1.00 m. Total height 14.20 m.
- Structural grid: 0.30 m perimeter walls, 0.20 m party walls between flats,
  0.10 m internal partitions. Floor slab 0.30 m.

VERTICAL CIRCULATION — ONE CORE ONLY
- Single core at the WEST end of the plan: 4.20 m wide x 5.10 m deep = 21.4 m2,
  containing one 1050 kg passenger lift (car 1.10 x 1.60 m, shaft 2.20 x 2.40 m)
  and one pressurised escape stair, 1.20 m clear width, 17 risers of 17 cm,
  straight run with one half-landing. The core runs continuously from ground to
  roof and must align exactly on every level. No second core.

ACCESS CORRIDOR — SINGLE-LOADSIDE
- One straight corridor along the NORTH side: 1.30 m clear width, spanning from
  the core to the east end, 47.3 m2. Every flat and every shop opens onto it.
  No secondary corridors, no galleries, no atrium.

LEVEL G — GROUND FLOOR (COMMERCIAL), z = 0.00
- 4 identical shop units, each 9.09 m wide x 6.00 m deep = 54.5 m2, lined along
  the SOUTH facade, party walls at 9.09 m centres, each with a fully glazed
  shopfront (2.40 m high) facing the veranda, each with its own entrance.
- Behind the shops, along the north edge, a rear service strip 4.70 m deep used as:
  one shared WC + one storage room per shop, one electrical/ meter room,
  one lift/stair lobby, and a shop back-of-house access corridor.
- The veranda in front of the shops (40.55 x 2.67 m) stays open to the sky and is
  used as pavement; do not enclose it.
- Level G floor sits 0.90 m above the pilotis slab, so the basement ceiling stays
  within 0.90 m of natural grade (the rule that keeps the basement non-countable).

LEVELS 1, 2 AND 3 — IDENTICAL RESIDENTIAL FLOORS, 4 FLATS PER FLOOR
- 4 flats per level, in a single row along the south side, each flat 9.09 m wide
  x 7.20 m deep = 65.4 m2 net enclosed area (this is the hard target).
- Each flat opens with a single door onto the north corridor and has this
  day/ night arrangement:
  * Living + dining: south, full width of the flat, min 24 m2, one 2.4 m wide
    sliding glazed door onto the veranda.
  * Kitchen: open to the living space with a 1.2 m break bar, along the party
    wall, min 8 m2, with a service flue to the roof.
  * Bedroom 1 (master): north-east of the flat, min 12 m2, window to the corridor
    light-well or to the north if the lot allows.
  * Bedroom 2: min 9.5 m2.
  * Bathroom: min 3.5 m2, WC + washbasin + shower 0.90 x 0.90 m, no window needed
    (mechanical extract through the core wall).
  * Entry hall / corridor inside the flat: max 4 m2, no wasted circulation.
  * In-unit washing niche 0.80 x 0.60 m next to the bathroom.
- South of every flat a covered veranda ("eyvan"): 9.09 m x 2.20 m deep = 20 m2,
  roofed, open on the south face, 1.10 m solid parapet, counted as balcony not as
  enclosed area. Every flat gets exactly one, aligned vertically on all floors.
- Total per floor: 261.8 m2 enclosed flats + 21.4 m2 core + 47.3 m2 corridor +
  23.5 m2 walls + 79.9 m2 verandas = 433.9 m2.

ROOF
- Flat roof, parapet 1.00 m, one 2.80 m high stair/lift overrun housing.
- Reserved zones: 4 split-unit condensers along the north parapet, one 1000 l
  solar water heater bank, one 2 x 3 m water tank room. Keep the south half clear.

STYLE AND OUTPUT
- Contemporary Iranian apartment, massing-driven, horizontal balcony bands,
  white/ light-grey render with dark window frames, no ornament.
- Produce dimensioned plans for each level with wall thicknesses, room labels and
  areas, then a simple 3D massing view. Keep all four levels in plan.

NON-NEGOTIABLE RULES FOR THE SOLVER
- Identical footprint and identical core position on every level.
- Exactly 4 flats per residential floor, exactly 65.4 m2 each, exactly 4 shops
  of 54.5 m2 on the ground floor.
- Corridor only on the north side, single-loaded, 1.30 m clear.
- No flat without a south veranda; no room without a window except bathrooms.
- No room deeper than 7.20 m from facade to facade.
- Total enclosed area per floor must not exceed 433.9 m2.
```

---

## ۲) پرامپتِ کوتاه — اگر ورودیِ شما کاراکترِ محدود دارد

```
4-level mixed-use building, Isfahan, all dimensions in METRES.
Lot 40.57 x 13.37 m. Footprint 40.55 x 10.70 m = 433.9 m2 on every level,
south setback 2.67 m kept as open veranda, total height 14.20 m.
Ground: 4 shops, each 9.09 x 6.00 m = 54.5 m2, glazed shopfronts to the south,
rear service strip 4.70 m deep (WC, storage, meter room, back corridor).
Levels 1-3 identical: 4 flats per floor, each 9.09 x 7.20 m = 65.4 m2 net
(living+dining 24 m2 south with sliding door to veranda, open kitchen 8 m2,
bedroom 12 m2, bedroom 9.5 m2, bathroom 3.5 m2, hall 4 m2, washing niche),
plus a covered 9.09 x 2.20 m veranda per flat on the south face.
One single core only at the west end: 4.20 x 5.10 m, 1 lift (1050 kg) +
1 escape stair 1.20 m wide, aligned on all levels. One straight 1.30 m wide
single-loaded corridor along the north side, 47.3 m2, no other circulation.
Walls: 0.30 m perimeter, 0.20 m party, 0.10 m partitions, slab 0.30 m.
Floor heights: ground 4.50 m, typical 2.90 m, parapet 1.00 m.
Flat roof with 1.00 m parapet + 2.80 m overrun; 4 condenser pads, solar bank and
a 2 x 3 m tank room on the north half.
Contemporary Iranian apartment, horizontal balcony bands, light render, dark frames.
Output dimensioned plans for each level + 3D massing.
```

---

## ۳) پرامپتِ تک‌صفحه‌ای (برایِ پلنِ رایگان) — هر طبقه جدا

سه‌تا پروژهٔ جدا بسازید و بعد با «پرامپتِ الحاقِ طبقه» کنارِ هم بچینید.

**الف) همکف**
```
Ground floor plan of a mixed-use building, metres. Plot 40.57 x 13.37 m,
building 40.55 x 10.70 m. South edge open 2.67 m veranda (leave unenclosed).
Four retail units in a row facing south: each 9.09 m wide x 6.00 m deep = 54.5 m2,
glazed shopfront 2.40 m high, private entrance, party walls 0.20 m.
Behind them a 4.70 m deep service strip: shared WC, one storage per shop,
meter room, lift lobby. At the west end a 4.20 x 5.10 m core with one 1050 kg
lift and one 1.20 m straight escape stair. Ceiling 4.50 m. Produce the plan with
dimensions and areas.
```

**ب) طبقهٔ نمونه (این را برایِ سه تکرار بسازید)**
```
Typical residential floor plan, metres, one single-storey level.
Building envelope 40.55 x 10.70 m. Along the north edge a straight 1.30 m wide
single-loaded access corridor from the west core to the east wall.
Four flats in one row on the south side, each exactly 9.09 m x 7.20 m = 65.4 m2 net:
living+dining 24 m2 with a 2.4 m sliding glazed door to the south veranda,
open kitchen 8 m2 with bar, bedroom 12 m2, bedroom 9.5 m2, bathroom 3.5 m2
(WC, basin, 0.90 x 0.90 shower), hall 4 m2, washing niche 0.80 x 0.60 m.
At the west end a 4.20 x 5.10 m core with one lift and one 1.20 m escape stair.
South of each flat a covered veranda 9.09 x 2.20 m with 1.10 m parapet.
Walls 0.30 m perimeter, 0.20 m party, 0.10 m partitions. Floor-to-floor 2.90 m.
No rooms deeper than 7.20 m. Show dimensions, room names and areas.
```

**پ) پیلوت/پارکینگ (اگر خواستید پارکینگ را هم ببینید)**
```
Pilotis level under a residential building, metres. Open floor 40.55 x 10.70 m
on a 0.40 x 0.40 m column grid at 7.30 m spans, clear height 2.60 m under beam.
13 diagonal bays of 2.50 m pitch, 5.00 m deep, in one band along the south
(veranda side) edge, bays at 45 degrees with a 6.00 m manoeuvre aisle behind them.
Ramp 3.50 m wide, straight, maximum 15% slope, from the north lane.
Manoeuvre aisle 6.00 m. The west 4.20 x 5.10 m core (lift + stair) continues down.
Show the marking layout with dimensions.
```

---

## ۴) پرامپت‌هایِ اصلاحیِ ترتیبی (بعد ازِ نسلِ اول، یکی‌یکی بفرستید)

```
1. Lock the core: move it to the west end, 4.20 x 5.10 m, and keep the exact same
   position on every level. Do not add a second stair or a second lift.
2. Make the corridor single-loaded on the north side only, 1.30 m clear, straight,
   and delete any other circulation space inside the flats.
3. Force every flat to be 9.09 m wide x 7.20 m deep, net 65.4 m2. Split the
   difference by shrinking the living room, never the bedrooms.
4. Reduce each unit count to exactly 4 flats per residential floor and 4 shops
   on the ground floor.
5. Give every flat one covered south veranda 9.09 x 2.20 m, vertically aligned on
   all three floors, 1.10 m parapet. It must not be counted as enclosed area.
6. Put the shopfronts fully on the south face, 6.00 m deep shops only, and move
   all back-of-house (WC, storage, meters) to the north service strip.
7. Keep the footprint identical on all four levels and total 433.9 m2. If you
   exceed it, trim corridor width to 1.30 m, not the flats.
8. Show me the area schedule per level: enclosed flats, veranda, core, corridor,
   walls, total. Numbers in m2.
```

اگر عددِ ۸ را اجرا نکرد، این را بفرستید:
```
Produce a table with one row per level and columns: enclosed flat area, veranda
area, core, corridor, wall area, total. Values in m2, one decimal. Do not redraw
the plan.
```

---

## ۵) پرامپتِ رندر/استایلِ Maket (بعد ازِ تأییدِ پلان)

```
Render this building as a contemporary Iranian apartment block, morning light.
Four levels: glazed shopfronts at ground floor under a 2.67 m deep open veranda,
three residential floors with continuous horizontal balcony bands and 1.10 m
solid parapets, single dark glazed core on the west end running full height,
flat roof with a 1.00 m parapet. Light grey and off-white smooth render, dark
anthracite window frames and balcony soffits, no ornament, no arches.
Street view from the south-west corner at eye level, warm dry climate, dusty
plane trees on the pavement, a low concrete kerb, a couple of parked cars,
clear sky. Photorealistic architectural visualisation, 35 mm lens, soft shadows.
```

نمایِ دومِ پیشنهادی (هوایی، برایِ نشان‌دادنِ بام):
```
Aerial three-quarter view from the south-east, 45 m above ground, showing the flat
roof layout: 4 condenser pads along the north parapet, solar water heater bank,
2 x 3 m tank room, and the west stair overrun. Same building and materials as before.
```

---

## ۶) معیارهایِ راستی‌آزمایی — خروجی را با این‌ها بسنجید

| آنچه باید درِ خروجیِ Maket باشد | مقدارِ مرجع | اگر نبود |
|---|---|---|
| زیربنایِ هر تراز | 433.9 m² (± ۲٪) | پرامپتِ اصلاحیِ ۷ |
| مساحتِ واحدِ مفید | 65.4 m² | اصلاحیِ ۳ |
| تعدادِ واحدِ هر طبقه | ۴ | اصلاحیِ ۴ |
| تعدادِ مغازه در همکف | ۴ × 54.5 m² | اصلاحیِ ۶ |
| عرضِ راهرو | 1.30 m، یک‌طرفه، شمالی | اصلاحیِ ۲ |
| هسته | یک‌دانه، غربی، 4.20 × 5.10 m | اصلاحیِ ۱ |
| ایوان | 2.20 m عمق، هر واحد، هم‌تراز | اصلاحیِ ۵ |
| بلندیِ کل | 14.20 m (۴ تراز + پاراپت) | — |
| تراکمِ به‌دست‌آمده | ≤ 1399.9 m² | اصلاحیِ ۷ |

سه خطِ قرمزِ که Maket نمی‌فهمد و خودتان باید چک کنید:

1. **پس‌رفت وِ مشاعات.** Maket نمی‌داند ایوانِ باز در اصفهان مشمولِ تراکم نیست؛ اگر
   آن را سرپوشیدهٔ شیشه‌ای کرد، ۸۰ m² در هر طبقه به تراکم اضافه شده و جریمه می‌رود.
2. **ترازِ بام وِ خطِ برق.** حریمِ خط را خودش لحاظ نمی‌کند.
3. **پارکینگ.** Maket معمولاً پارکینگ را درِ پیلوت نمی‌چیند؛ خودتان چک کنید ۱۳ فضا
   و رمپِ ۳٫۵ m بماند، وگرنه طبقِ تبصرهٔ ۵ِ مادهٔ ۱۰۰ جریمه‌اش اجباری است.

---

## ۷) مسیرِ برگشت بهِ فایل‌هایِ خودی

خروجیِ Maket را که پسندیدید، **DXF** بگیرید و درِ `docs/arch/` بگذارید؛ با اسکریپتِ
`tools/render_schemes.py` می‌توانید همان را رویِ برگهٔ A3ِ خودی بنشانید، و مدلِ
`scene.blend` را هم با جعبه‌هایِ جدیدِ `tools/make_blender_schemes.py` بازسازی کرد.
یادتان باشد مرجعِ قانونیِ اعدادِ ما همچنان `tools/plan_schemes.py` است؛ Maket ابزارِ
مقایسه است، نه ابزارِ تولیدِ نقشهٔ اجرایی.
