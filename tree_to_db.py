from dotenv import load_dotenv
import os
import requests
import pymysql
import math

# db 접속 변수
load_dotenv()
host = os.environ.get("HOST")
user = os.environ.get("DBUSER")
password = os.environ.get("DBPW")
db = os.environ.get("DB")
charset = os.environ.get("CHARSET")

# 확대/축소 (zoom)
zoom = 16

# 타일의 수 = 2**zoom * 2**zoom
zoomPow = int(math.pow(2, zoom))
tiles = int(zoomPow * zoomPow)

# db 연결
conn = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)

# 커서 생성(쿼리 실행, 결과 반환 객체_
cur = conn.cursor()

# 데이터 요청 url
url = 'http://openapi.seoul.go.kr:8088/576d706166746b6436364e55784655/json/GeoInfoOfRoadsideTreeW/';
guName = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구' ,'양천구', '영등포구', '용산구', '은평구', '중구', '중랑구']

for gu in guName:
    
    # total_list 요청
    countRes = requests.get(url + '1/5/' + gu);

    # 데이터 파싱
    jsonData = countRes.json();

    # 총 개수
    list_total_count = jsonData['GeoInfoOfRoadsideTreeW']['list_total_count']

    for i in range(0, list_total_count // 100):
        getUrl = url + str(i * 100 + 1) + '/' + str((i+1) * 100) + '/' + gu
        res = requests.get(getUrl)
        treeJson = res.json()
        treeList = treeJson['GeoInfoOfRoadsideTreeW']['row']
        
        for tree in treeList:
            try:
                _id = int(tree['OBJECTID'])
                lng = float(tree['LNG'])
                lat = float(tree['LAT'])
                wood_name = str(tree['WDPT_NM'])
                gu_name = str(tree['GU_NM'])
                street_name = str(tree['WIDTH_NM'])
                
                # 16 수준에서의 위도 경도의 타일 좌표 구하는 공식
                sinLat = math.sin(lat * math.pi / 180)

                pixelX = ((lng + 180) / 360) * tiles * zoomPow
                tile_x = math.floor(pixelX / tiles)

                pixelY = (0.5 - math.log((1 + sinLat) / (1 - sinLat)) / (4 * math.pi)) * tiles * zoomPow
                tile_y = math.floor(pixelY / tiles)
                
                # 쿼리문 작성
                query = 'insert into tree (_id, lat, lng, tile_x, tile_y, wood_name, gu_name, street_name) values(%s, %s, %s, %s, %s, %s, %s, %s)';
                values = (_id, lat, lng, tile_x, tile_y, wood_name, gu_name, street_name)
                # 쿼리문 수행
                cur.execute(query, values);
            except Exception as e:
                print(_id)
                print(e)

        # 커밋 수행
        conn.commit();



# 연결 종료
conn.close();