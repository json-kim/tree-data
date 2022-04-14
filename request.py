import requests

# 데이터 요청 url
url = 'http://openapi.seoul.go.kr:8088/576d706166746b6436364e55784655/json/GeoInfoOfRoadsideTreeW/1/5/중구';

# get 요청
res = requests.get(url);

# 데이터 파싱
jsonData = res.json();

treeList = jsonData['GeoInfoOfRoadsideTreeW']['row'];

for tree in treeList:
    print(tree);