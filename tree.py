from dotenv import load_dotenv
import os
import pymysql

load_dotenv()
host = os.environ.get("HOST")
user = os.environ.get("DBUSER")
password = os.environ.get("DBPW")
db = os.environ.get("DB")
charset = os.environ.get("CHARSET")

# db 연결
conn = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)

# 커서 생성(쿼리 실행, 결과 반환 객체_
cur = conn.cursor()

# 쿼리문 작성
query = 'select count(*) as count from tree'

# 쿼리문 수행
cur.execute(query)
result = cur.fetchone()

# 커밋 수행
conn.commit()

print(result[0])

# 연결 종료
conn.close()