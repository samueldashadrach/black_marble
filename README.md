2025-08-08

# README

WIP

```
earthengine authenticate

# activate env

python3 ee_export.py
```

convert TIF to KMZ
```
for f in *.tif; do base=$(basename "$f" .tif); gdal_translate -of KMLSUPEROVERLAY -co FORMAT=JPEG "$f" "$base.kmz"; done
```

then open google earth pro, file -> open -> select all



---

```
tokyo 2019-06 black marble has no nightlight, but previous and succeeding months have nightlight. why?
```

gpt-5 says

```
Short answer: it’s a data artifact, not that Tokyo went dark.

Why it happens
- Cloudy/rainy season: June is the start of Japan’s tsuyu (rainy) season. Black Marble monthly composites include only clear‑sky, nighttime observations. If nearly all nights are cloudy, there may be zero valid samples.
- Stray light season: Around the Northern Hemisphere summer solstice, the VIIRS Day/Night Band suffers from solar stray‑light contamination at mid‑latitudes. The Black Marble pipeline filters those scenes out. Combined with clouds, this can leave no usable data.
- Processing/version issues: Earlier Black Marble versions occasionally had gaps in certain months/regions. Later reprocessing (V2) reduces these gaps.

How to confirm and what to do
- Check the QA/observation-count layer for June 2019 at Tokyo; if the number of clear observations is 0, that’s the reason.
- Look at the daily product for June 2019; you’ll likely see most nights flagged cloudy/straylight.
- If you need a value for that month, use the gap-filled variant (if available), the reprocessed V2 monthly, or fill from May/July (median of ±1–2 months).

If you tell me which exact dataset/version and viewer you’re using (e.g., NASA VNP46A3 v1/v2, NOAA VCMSLCFG, Earth Engine, Worldview), I can point you to the specific QA band and a quick check.
```

gpt-5 says
```
Thanks—so you’re looking at the NOAA EOG monthly VIIRS product VCMCFG.

Why April 2020 looks dimmer than May 2020 over Tokyo in VCMCFG
- Fewer usable observations in April: The composite uses only cloud‑free, nighttime observations. Spring fronts and haze often reduce April’s “cloud‑free coverage” (cf_cvg) around Tokyo. With fewer samples, the monthly average (avg_rad) can skew low.
- Stray‑light season handling: From roughly April through August at 35°N, VIIRS DNB is affected by solar stray light. VCMCFG screens contaminated scenes out; depending on geometry, April can lose many scenes. Some May months, however, retain more usable scenes or may have residual contamination that biases radiance upward. For these months, VCMSLCFG (the stray‑light–corrected composite) is the recommended variant.
- Real‑world change in lighting: Tokyo’s COVID‑19 state of emergency started Apr 7, 2020. Many commercial lights and activity diminished through April, with partial rebound by late May (emergency lifted May 25). That genuine change often shows up in the monthly lights.

How to confirm in VCMCFG
- Check the cf_cvg band for 2020‑04 vs 2020‑05 at your AOI. If April’s cf_cvg is lower, that explains much of the dimming.
- If you can, compare against VCMSLCFG for the same months. If May’s brightness drops relative to VCMCFG, stray‑light contamination was likely boosting VCMCFG in May.

Recommendations
- Prefer VCMSLCFG for months in stray‑light season (roughly Apr–Aug at Tokyo’s latitude), or use the newer EOG VNL v2 monthly or NASA Black Marble VNP46A3 v2 which include more robust corrections.
- Always use cf_cvg (observation count) to weight or filter monthly comparisons; avoid interpreting months with very low cf_cvg.
```
