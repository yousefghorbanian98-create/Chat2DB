# Page override — Jackson-Pollock 7 Assessment

## Layout (3 columns ≥1200px)
1. Athlete profile card (photo, age, sex, last check-in)
2. 7 numeric inputs + body silhouette with site markers
3. Results: BF%, LBM, FM, density, classification badge

Bottom full-width: BF% time series (Recharts line)

## UX rules
- Inputs `inputMode="decimal"`, `dir="ltr"`, tabular nums, font-size 16px
- Validate on blur; block Calculate if any site empty or ≤0
- Show protocol tip per site (coach guidance) in side drawer
- Injury banner if active limitation on measured regions
- Primary CTA: Calculate → then Save Assessment
- Always store both Siri & Brozek; display primary preference in Settings

## A11y
- Silhouette markers have text alternatives in the form labels (not color-only)
- Error summary at top of form on failed calculate
