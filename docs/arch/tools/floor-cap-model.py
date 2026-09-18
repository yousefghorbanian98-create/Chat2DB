# -*- coding: utf-8 -*-
"""سقفِ واقعی: ۳ طبقه رویِ پیلوت. نسبت‌ها از طرحِ اول استخراج شده (تأییدشده)."""
import math
LAND, COV80, DEEP = 542.42, 0.80*542.42, 10.70
# --- کالیبراسیون با طرحِ اول: زیربنای ۲۴۱.۵ m² → ۲ واحدِ ۷۶.۲ بسته + ۲ ایوانِ ۱۵.۷ ---
R_UNIT, R_BALC = 152.4/241.5, 31.4/241.5        # ۰.۶۳۱ و ۰.۱۳۰
C_RES, C_PIL, C_BSM = 0.070, 0.030, 0.050
P_RES, K_COM, P_BALC, P_PARK = 120.0, 2.4, 0.50, 0.96
SPACE, RAMP, F_FAR, F_PK = 25.0, 3.5*2.70/0.17, 0.008, 0.15

def ev(name, nf, foot, upf, shops=0, bsm=False, pil=True):
    encl, balc = foot*R_UNIT, foot*R_BALC
    cnt   = encl + 0.5*balc                     # زیربنای مشمولِ تراکم
    com   = shops*44.9
    gfa   = nf*cnt + com
    ua    = encl/upf
    tot_u = upf*nf
    cap   = COV80 if (pil or bsm) else 0.0
    have  = int(max(0.0, cap - (RAMP if bsm else 0))/SPACE)
    need  = tot_u + (math.ceil(com/25) if com else 0)
    bal, exc = have-need, max(0.0, gfa-1.80*LAND)
    cost  = nf*foot*C_RES + (COV80*C_PIL if pil else 0) + (COV80*C_BSM if bsm else 0) + com*C_RES
    rev   = (tot_u*ua*P_RES + nf*balc*P_RES*P_BALC + com*P_RES*K_COM
             + max(0,bal)*P_PARK*0.5)/1000.0
    fine  = exc*F_FAR + max(0,-bal)*F_PK
    h     = (2.60 if pil and not shops else 5.40) + nf*2.90 + 1.00
    return dict(name=name, nf=nf, units=tot_u, ua=ua, foot=foot, width=foot/DEEP,
                height=h, far=gfa/LAND*100, have=have, need=need, bal=bal, exc=exc,
                rev=rev, cost=cost, fine=fine, net=rev-cost-fine)

def foot_for(nf, base, shops=0):
    return min(COV80, max(0.0, (base*LAND - shops*44.9)/nf)/0.935)

rows = [
 ev("الف) پیلوت + ۳ طبقه · تراکمِ پایه ۱۸۰٪",       3, foot_for(3,1.80), 2),
 ev("ب) پیلوت + ۳ طبقه · تراکمِ پایه ۱۲۰٪",         3, foot_for(3,1.20), 2),
 ev("ج) پیلوت + ۳ طبقه · پهنای کامل (تراکم ۲۲۴٪)",  3, COV80, 3),
 ev("د) همکفِ مغازه + ۳ طبقه + زیرزمین · ۱۸۰٪",     3, foot_for(3,1.80,3), 2, shops=3, bsm=True, pil=False),
 ev("ه‍) طرحِ اولِ فعلی (۵ طبقه + ۳ مغازه)",          5, 241.5, 2, shops=3, pil=False),
]
print(f"{'طرح':<46}{'طبقه':>5}{'واحد':>5}{'متراژ':>7}{'عرض':>7}{'ارتفاع':>8}{'تراکم':>7}"
      f"{'پارکینگ':>9}{'مازاد':>7}{'درآمد':>8}{'ساخت':>8}{'خالص':>8}")
print("="*120)
for r in sorted(rows, key=lambda r:-r['net']):
    print(f"{r['name']:<46}{r['nf']:>5}{r['units']:>5}{r['ua']:>7.0f}{r['width']:>6.1f}m"
          f"{r['height']:>7.2f}m{r['far']:>6.1f}%{r['have']:>5}/{r['need']:<3}{r['exc']:>7.0f}"
          f"{r['rev']:>8.1f}{r['cost']:>8.1f}{r['net']:>8.1f}")
print("="*120)
a=[r for r in rows if r['name'].startswith('الف')][0]
c=[r for r in rows if r['name'].startswith('ج')][0]
print(f"\nپهن‌تر ساختن (۳۳→۴۱ متر عرض) و پذیرفتنِ مازادِ تراکم: {c['net']-a['net']:+.1f} میلیارد")
print(f"کُلیِّ سقفِ طبقه: طرحِ اول {[r for r in rows if r['name'].startswith('ه‍')][0]['net']:.1f}"
      f" در برابرِ بهترینِ قانونی {a['net']:.1f} میلیارد")
