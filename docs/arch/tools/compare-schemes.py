# -*- coding: utf-8 -*-
"""مقایسهٔ اقتصادیِ طرح اول و گزینه‌های طرح دوم — زمین ۵۴۲٫۳۸ m² اصفهان
مبالغ میلیارد تومان (۱۴۰۵). فرض‌ها صریح‌اند و همه در تحلیلِ حساسیت آزموده شده‌اند.
"""
import math
LAND, COV80, UNIT, PER_FLOOR = 542.42, 0.80*542.42, 92.0, 190.5
SPACE_AREA, RAMP_AREA = 25.0, 3.5*2.70/0.17

# ---- فرض‌های مرکزی (واحد: میلیارد تومان، به‌جز P_R که میلیون تومان بر متر است) ----
P_R, K_C, P_S = 50.0, 2.4, 0.40
C_AB, C_BS = 0.025, 0.018
F_FAR, F_PK = 0.008, 0.15
DISC = 0.02          # تخفیفِ فروش‌پذیری: ۲٪ به‌ازای هر فضایِ پارکینگِ کمبود (سقف ۲۰٪)

def scheme(name, nf, shops, mezz, stor, park_now, gfa, height,
           P_R=P_R, K_C=K_C, P_S=P_S, C_AB=C_AB, C_BS=C_BS,
           F_FAR=F_FAR, F_PK=F_PK, DISC=DISC, bsm_on=True, bsm_full=False):
    units, res = nf*2, nf*2*UNIT
    need = units + (math.ceil(shops*44.9/25) if shops else 0)
    bsm = (COV80 if bsm_full else min(COV80, need*SPACE_AREA + RAMP_AREA)) if (bsm_on and need) else 0.0
    have = park_now + int(max(0.0, bsm - RAMP_AREA)/SPACE_AREA)
    bal, exc = have - need, max(0.0, gfa - 1.80*LAND)
    disc = min(0.20, DISC*max(0, -bal)) if bal < 0 else 0.0
    rev = (res*P_R*(1-disc) + shops*44.9*P_R*K_C + mezz*P_R*0.6 + stor*P_R*0.5
           + max(0, bal)*P_S*0.5)/1000.0
    cost, fine = gfa*C_AB + bsm*C_BS, exc*F_FAR + max(0, -bal)*F_PK
    return dict(name=name, units=units, res=res, height=height, gfa=gfa,
                far=gfa/LAND*100, bsm=bsm, have=have, need=need, bal=bal,
                exc=exc, disc=disc, rev=rev, cost=cost, fine=fine,
                net=rev-cost-fine)

def variants(bsm_full=False):
    return [
        dict(a=("طرح اول (۳ مغازه + ۵ طبقه)", 5, 3, 80.9, 40, 6, 1179.9, 20.90), bsm_on=False),
        dict(a=("دوم-الف: ۵ طبقه + زیرزمین",  5, 0, 0, 0, 0, 5*PER_FLOOR, 16.40)),
        dict(a=("دوم-ب: ۶ طبقه + زیرزمین",    6, 0, 0, 0, 0, 6*PER_FLOOR, 19.30)),
        dict(a=("دوم-ج: ۷ طبقه + زیرزمین",    7, 0, 0, 0, 0, 7*PER_FLOOR, 22.20)),
        dict(a=("دوم-ب بدون زیرزمین",         6, 0, 0, 0, 0, 6*PER_FLOOR, 19.30), bsm_on=False),
    ]

def run(**kw):
    return [scheme(*v['a'], bsm_on=v.get('bsm_on', True), **kw) for v in variants()]

print("="*124)
print(f"{'طرح':<30}{'واحد':>5}{'ارتفاع':>8}{'تراکم':>8}{'زیرزمین':>9}{'پارکینگ':>10}"
      f"{'کسری':>6}{'تخفیف':>8}{'مازاد':>7}{'درآمد':>8}{'ساخت':>7}{'جریمه':>7}{'خالص':>8}")
print("="*124)
for r in run():
    print(f"{r['name']:<30}{r['units']:>5}{r['height']:>7.2f}m{r['far']:>7.1f}%"
          f"{r['bsm']:>8.0f}m²{r['have']:>5}/{r['need']:<4}{max(0,-r['bal']):>6}"
          f"{r['disc']*100:>7.0f}%{r['exc']:>7.0f}{r['rev']:>8.1f}{r['cost']:>7.1f}"
          f"{r['fine']:>7.1f}{r['net']:>8.1f}")
print("="*124)

def top(**kw):
    ss = sorted(run(**kw), key=lambda r: -r['net'])
    return ss[0]['name'], ss[0]['net'], ss[0]['net']-ss[1]['net']

print("\n── ۱) حساسیت به ارزشِ مغازه (k = قیمتِ تجاری ÷ مسکونی) ──")
for k in (1.0, 1.5, 2.0, 2.4, 3.0):
    n, v, d = top(K_C=k)
    print(f"   k={k:>4.1f} → {n:<30} خالص {v:>5.1f}   (برتری {d:+.1f})")
print("\n── ۲) حساسیت به شدتِ جریمهٔ فروش‌پذیریِ بی‌پارکینگی ──")
for d in (0.0, 0.01, 0.02, 0.03, 0.05):
    n, v, _ = top(DISC=d)
    print(f"   {d*100:>4.1f}% به‌ازای هر فضای کمبود → {n:<30} خالص {v:>5.1f}")
print("\n── ۳) حساسیت به هزینهٔ ساخت (نسبت به قیمتِ فروش) ──")
for c in (0.35, 0.50, 0.70):
    n, v, _ = top(C_AB=P_R*c/1000, C_BS=P_R*c*0.72/1000)
    print(f"   ساخت = {c*100:>3.0f}% قیمتِ فروش → {n:<30} خالص {v:>5.1f}")
print("\n── ۴) اگر زیرزمینِ کامل (۴۳۴ m²) بسازیم نه به‌اندازهٔ نیاز ──")
for r in run():
    if r['bsm'] > 0:
        rf = scheme(*[v['a'] for v in variants() if v['a'][0]==r['name']][0], bsm_full=True)
        print(f"   {r['name']:<30} زیرزمینِ کامل: هزینه {rf['cost']-r['cost']:+.1f} · خالص {rf['net']:>5.1f} (به‌جای {r['net']:.1f})")

print("\n" + "="*124)
print("ترکیب‌هایِ بیشتر — آیا می‌توان مغازه را نگه داشت و پارکینگ را هم حل کرد؟")
print("="*124)
H = [
  dict(name="اول + زیرزمین (۳ مغازه + ۵ طبقه + زیرزمین کامل)", nf=5, shops=3, mezz=80.9,
       stor=40, park_now=6, gfa=1179.9, height=20.90, bsm_on=True, bsm_full=True),
  dict(name="دوم + ۲ مغازه (۶ طبقه + ۲ مغازه + زیرزمین)", nf=6, shops=2, mezz=53.9,
       stor=0, park_now=0, gfa=6*PER_FLOOR, height=19.30, bsm_on=True),
  dict(name="دوم + ۳ مغازه (۶ طبقه + ۳ مغازه + زیرزمین)", nf=6, shops=3, mezz=80.9,
       stor=0, park_now=0, gfa=6*PER_FLOOR+20, height=19.30, bsm_on=True),
]
allr = run() + [scheme(h['name'], h['nf'], h['shops'], h['mezz'], h['stor'],
                       h['park_now'], h['gfa'], h['height'],
                       bsm_on=h.get('bsm_on', True), bsm_full=h.get('bsm_full', False))
                for h in H]
print(f"{'طرح':<48}{'واحد':>5}{'ارتفاع':>8}{'تراکم':>8}{'پارکینگ':>10}{'کسری':>6}"
      f"{'تخفیف':>7}{'درآمد':>8}{'ساخت':>7}{'جریمه':>7}{'خالص':>8}")
print("-"*124)
for r in sorted(allr, key=lambda r: -r['net']):
    print(f"{r['name']:<48}{r['units']:>5}{r['height']:>7.2f}m{r['far']:>7.1f}%"
          f"{r['have']:>5}/{r['need']:<4}{max(0,-r['bal']):>6}{r['disc']*100:>6.0f}%"
          f"{r['rev']:>8.1f}{r['cost']:>7.1f}{r['fine']:>7.1f}{r['net']:>8.1f}")
print("-"*124)
b = sorted(allr, key=lambda r: -r['net'])[0]
print(f"برترین: {b['name']} → خالص {b['net']:.1f} میلیارد تومان")
print("\nنقطهٔ بی‌تفاوتی: مغازه باید چند برابرِ آپارتمان بفروشد تا «طرح اول» از «۷ طبقه+زیرزمین» بهتر شود؟")
for k in (1.6,1.8,1.9,2.0,2.2):
    a=[r for r in run(K_C=k) if 'اول' in r['name']][0]['net']
    c=[r for r in run(K_C=k) if 'دوم-ج' in r['name']][0]['net']
    print(f"   k={k:.1f}: طرح اول {a:>5.1f} | هفت‌طبقه {c:>5.1f} | {'طرح اول' if a>c else 'هفت‌طبقه'}")
