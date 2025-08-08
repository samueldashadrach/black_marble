2025-08-08

# README

WIP


```
for f in data/*.tif; do base=$(basename "$f" .tif); gdal_translate -of KMLSUPEROVERLAY -co FORMAT=JPEG "$f" "kmz/$base.kmz"; done
```
