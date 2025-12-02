import sqlite3
from datetime import datetime

def index():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM topics")
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return rows

def get(hash: str):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM topics WHERE hash = ?", (hash,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update(hash, answer):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE topics
        SET status = 1, answer = ?, ai_date = ?
        WHERE hash = ?
    """, (
        answer, 
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
        hash
    ))

    conn.commit()
    conn.close()

def insert(data):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO topics (hash, date, question)
        VALUES (?, ?, ?)
    """, (
        data['hash'],
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        data['question']
    ))

    conn.commit()
    conn.close()
