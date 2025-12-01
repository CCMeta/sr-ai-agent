import sqlite3
from datetime import datetime

def get():
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    data = {
        'hash': 'abc123def456',
        'status': 0,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'question': '什么是人工智能？',
        'answer': '人工智能是模拟人类智能的技术...'
    }

    cursor.execute("""
        INSERT INTO topics (hash, status, date, question, answer)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data['hash'],
        data['status'], 
        data['date'],
        data['question'],
        data['answer']
    ))

    cursor.execute("SELECT * FROM topics")
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return rows