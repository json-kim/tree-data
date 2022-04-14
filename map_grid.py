import math

# 확대/축소 (zoom)
zoom = 16

# 타일의 수 = 2**zoom * 2**zoom
tiles = int(math.pow(2, zoom) * math.pow(2, zoom))

# 서울 좌표 (위도, 경도)
lat = 37.5627216
lng = 126.9983663

# 16 수준에서의 위도 경도의 타일 좌표 구하는 공식
sinLat = math.sin(lat * math.pi / 180)

pixelX = ((lng + 180) / 360) * tiles * math.pow(2, zoom)
tileX = math.floor(pixelX / tiles)

pixelY = (0.5 - math.log((1 + sinLat) / (1 - sinLat)) / (4 * math.pi)) * tiles * math.pow(2, zoom)
tileY = math.floor(pixelY / tiles)

print(tileX)
print(tileY)