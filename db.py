import sqlite3

DB = "data.db"

def db():
    return sqlite3.connect(DB)


def init_db():
    conn = db()
    c = conn.cursor()

    # 用户
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        credits INTEGER DEFAULT 0
    )
    """)

    # API KEY
    c.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        api_key TEXT,
        status TEXT DEFAULT 'active'
    )
    """)

    # 请求日志（🔥 V2新增）
    c.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        endpoint TEXT,
        cost INTEGER,
        created_at REAL
    )
    """)

    # 充值记录（🔥 V2新增）
    c.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        credits_added INTEGER,
        provider TEXT,
        created_at REAL
    )
    """)

    conn.commit()
    conn.close()