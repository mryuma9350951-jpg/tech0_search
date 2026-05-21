import sqlite3
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

# SQLite 接続
sqlite_conn = sqlite3.connect("tech0_search.db")
sqlite_cursor = sqlite_conn.cursor()

# Azure MySQL 接続
mysql_conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=3306,
    ssl={"ssl": {}}
)

mysql_cursor = mysql_conn.cursor()

# テーブル作成
mysql_cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    url TEXT
)
""")

# SQLite からデータ取得
sqlite_cursor.execute("SELECT id, title, url FROM pages")
rows = sqlite_cursor.fetchall()

# Azure MySQL へINSERT
for row in rows:
    mysql_cursor.execute("""
    INSERT INTO documents (id, title, url)
    VALUES (%s, %s, %s)
    """, row)

mysql_conn.commit()

print(f"{len(rows)}件のデータ移行完了！")

sqlite_conn.close()
mysql_conn.close()