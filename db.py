import apsw
from datetime import datetime


# index
def index():
    conn = apsw.Connection('database.db')
    cursor = conn.cursor()
    cursor.setrowtrace(create_dict_row_factory)

    cursor.execute("SELECT * FROM topics")
    rows = cursor.fetchall()

    conn.commit()
    conn.close()
    return rows


# get
def get(hash: str):
    conn = apsw.Connection('database.db')
    cursor = conn.cursor()
    cursor.setrowtrace(create_dict_row_factory)

    cursor.execute("SELECT * FROM topics WHERE hash = ?", (hash,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# update
def update(hash, answer, status, raw):
    conn = apsw.Connection('database.db')
    cursor = conn.cursor()
    cursor.setrowtrace(create_dict_row_factory)

    # This UPDATE will change multiple not just one if hash is not limit 1
    cursor.execute("""
        UPDATE topics
        SET status = ?, answer = ?, ai_date = ?, raw_answer = ?
        WHERE hash = ?
    """, (
        status,
        answer,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        raw,
        hash,
    ))

    conn.close()


# insert
def insert(data):
    conn = apsw.Connection('database.db')
    cursor = conn.cursor()
    cursor.setrowtrace(create_dict_row_factory)

    cursor.execute("""
        INSERT INTO topics (hash, date, question)
        VALUES (?, ?, ?)
    """, (
        data['hash'],
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        data['question']
    ))

    conn.close()


# create_dict_row_factory
def create_dict_row_factory(cursor, row):
    column_names = [description[0] for description in cursor.getdescription()]
    return dict(zip(column_names, row))
