import apsw
import threading
from datetime import datetime


_local = threading.local()


# get sqlite version
def get_sqlite_version():
    return apsw.sqlitelibversion()


def db() -> apsw.Connection:
    if not hasattr(_local, 'cursor'):
        conn = apsw.Connection('database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = WAL")
        cursor.execute("PRAGMA synchronous = NORMAL")
        cursor.execute("PRAGMA read_uncommitted = 1")
        cursor.setrowtrace(create_dict_row_factory)
        # _local.connection = conn
        _local.cursor = cursor
    return _local.cursor

# index
def index():
    db().execute("SELECT * FROM topics ORDER BY id DESC LIMIT 50")
    rows = db().fetchall()
    return rows


# count all status
def count_all_status():

    db().execute("""
        SELECT status, COUNT(*) as count
        FROM topics
        GROUP BY status
    """)
    rows = db().fetchall()
    return rows

# get
def get(hash: str):
    db().execute("SELECT * FROM topics WHERE hash = ?", (hash,))
    rows = db().fetchall()
    return rows


# update
def update(id, answer, status, raw):

    # This UPDATE will change multiple not just one if id is not limit 1
    db().execute("""
        UPDATE topics
        SET status = ?, answer = ?, ai_date = ?, raw_answer = ?
        WHERE id = ?
    """, (
        status,
        answer,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        raw,
        id,
    ))
    return True


# insert
def insert(data):

    result = db().execute("""
        INSERT INTO topics (hash, date, question)
        VALUES (?, ?, ?)
        RETURNING id
    """, (
        data['hash'],
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        data['question']
    ))
    inserted_id = result.fetchone().get('id')
    return inserted_id



# create_dict_row_factory
def create_dict_row_factory(cursor, row):
    column_names = [description[0] for description in cursor.getdescription()]
    return dict(zip(column_names, row))
