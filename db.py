import threading
import pymysql.cursors

from datetime import datetime
from contextlib import contextmanager


# 数据库连接参数 (请替换为你自己的设置)
DB_CONFIG = {
    'host': 'localhost',    # 例如 'localhost' 或 127.0.0.1
    'user': 'root',        # 您的数据库用户名
    'password': '1',    # 您的数据库密码
    'db': 'sys',     # 要连接的数据库名称
    'charset': 'utf8mb4',           # 推荐使用 utf8mb4 字符集
    'cursorclass': pymysql.cursors.DictCursor, # 返回字典形式的结果，更方便
    'autocommit': True
}


_local = threading.local()

# --- 辅助函数：获取连接对象 ---
def db():
    """获取线程本地的 MariaDB 连接对象，并确保它被存储"""
    if not hasattr(_local, 'conn'):
        # 1. 创建连接
        conn = pymysql.connect(**DB_CONFIG)
        # 2. 存储连接对象，并开启自动提交（可选，但推荐）
        conn.autocommit = True 
        _local.conn = conn
        # 3. 存储游标对象 (默认游标)
        _local.cursor = conn.cursor() # <-- 关键！
    return _local.conn



# index
def index():
    db()
    _local.cursor.execute("SELECT * FROM topics ORDER BY id DESC LIMIT 50")
    result = _local.cursor.fetchall()
    return result


# count all status
def count_all_status():
    db()
    _local.cursor.execute("SELECT status, COUNT(*) as count FROM topics GROUP BY status")
    result = _local.cursor.fetchall()
    return result

# get
def get(hash: str):
    db()
    _local.cursor.execute("SELECT * FROM topics WHERE hash = %s", (hash,))
    result = _local.cursor.fetchall()
    return result


# update
def update(id, answer, status, raw):
    db()

    print("Updating id:", id, "with status:", status)
    # This UPDATE will change multiple not just one if id is not limit 1
    _local.cursor.execute("""
        UPDATE topics
        SET status = %s, answer = %s, ai_date = %s, raw_answer = %s
        WHERE id = %s
    """, (
        status,
        answer,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        raw,
        id,
    ))
    result = _local.cursor.fetchall()
    return True


# insert
def insert(data):
    db()

    _local.cursor.execute("""
        INSERT INTO topics (hash, status, date, question)
        VALUES (%s, 0, %s, %s)
        RETURNING id
    """, (
        data['hash'],
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        data['question']
    ))

    result = _local.cursor.fetchone()
    inserted_id = result.get('id')
    return inserted_id


