# written by gpt-5, may contain hallucins

import ee
import datetime

# Initialize Earth Engine
ee.Initialize(project='moonlit-haven-467613-q1')

# Time range: monthly images from 2019-01 through 2021-12 (end is exclusive)
start = '2019-01-01'
end   = '2022-01-01'

# VIIRS monthly nighttime lights (Black Marble VCMCFG)
col_base = (
    ee.ImageCollection('NOAA/VIIRS/DNB/MONTHLY_V1/VCMCFG')
      .filterDate(start, end)
      .select(['avg_rad'])
      .map(lambda img: img.toFloat())
      .sort('system:time_start')
)

# Pull the monthly images and timestamps once (client-side lists)
n = col_base.size().getInfo()
if n == 0:
    raise RuntimeError('No images found in the specified date range.')

imgs_all = col_base.toList(n)
times_ms = col_base.aggregate_array('system:time_start').getInfo()  # list of epoch ms

# Format month tags client-side to avoid repeated getInfo calls
tags = []
for ms in times_ms:
    dt = datetime.datetime.utcfromtimestamp(int(ms) / 1000)
    tags.append(f"{dt.year:04d}_{dt.month:02d}")

# 10 cities worldwide including at least 1 US city (New York)
# radius_km defines the buffer radius around the city center
cities = [
    {'name': 'New York',   'tag': 'NYC', 'lon': -74.0060,  'lat': 40.7128,  'radius_km': 35},  # US city
    {'name': 'London',     'tag': 'LON', 'lon': -0.1278,   'lat': 51.5074,  'radius_km': 35},
    {'name': 'Paris',      'tag': 'PAR', 'lon': 2.3522,    'lat': 48.8566,  'radius_km': 30},
    {'name': 'Tokyo',      'tag': 'TYO', 'lon': 139.6917,  'lat': 35.6895,  'radius_km': 40},
    {'name': 'Delhi',      'tag': 'DEL', 'lon': 77.2090,   'lat': 28.6139,  'radius_km': 40},
    {'name': 'Shanghai',   'tag': 'SHA', 'lon': 121.4737,  'lat': 31.2304,  'radius_km': 40},
    {'name': 'Jakarta',    'tag': 'JKT', 'lon': 106.8456,  'lat': -6.2088,  'radius_km': 40},
    {'name': 'Lagos',      'tag': 'LOS', 'lon': 3.3792,    'lat': 6.5244,   'radius_km': 40},
    {'name': 'Cairo',      'tag': 'CAI', 'lon': 31.2357,   'lat': 30.0444,  'radius_km': 35},
    {'name': 'Sao_Paulo',  'tag': 'SAO', 'lon': -46.6333,  'lat': -23.5505, 'radius_km': 40},
]

def buffer_geom(lon, lat, radius_km):
    # Use a buffered circle as the AOI; region can accept this geometry directly
    return ee.Geometry.Point([lon, lat]).buffer(radius_km * 1000.0)

# Export settings
folder_name = 'BlackMarble_WorldCities'
scale_m = 500
max_pixels = 1e13

# Create Drive export tasks per image per city
for city in cities:
    geom = buffer_geom(city['lon'], city['lat'], city['radius_km'])

    for i in range(n):
        image = ee.Image(imgs_all.get(i)).clip(geom)
        tag = tags[i]

        task = ee.batch.Export.image.toDrive(
            image=image,
            description=f"{city['tag']}_BlackMarble_{tag}",
            folder=folder_name,
            fileNamePrefix=f"{city['tag']}_BM_{tag}",
            region=geom,
            scale=scale_m,
            maxPixels=max_pixels,
            fileFormat='GeoTIFF'
        )
        task.start()
        print('Started', city['tag'], tag)

print(f'Queued {n * len(cities)} exports. Note: Earth Engine limits concurrent tasks; you may need to run in batches.')
