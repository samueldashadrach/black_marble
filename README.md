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
for f in data/*.tif; do base=$(basename "$f" .tif); gdal_translate -of KMLSUPEROVERLAY -co FORMAT=JPEG "$f" "kmz/$base.kmz"; done
```

then open google earth pro, file -> open -> select all

