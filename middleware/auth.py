from db import db

def verify_key(api_key):

    if not api_key:
        return None

    conn = db()
    c = conn.cursor()

    c.execute("""
        SELECT users.id, users.credits
        FROM api_keys
        JOIN users ON users.id = api_keys.user_id
        WHERE api_keys.api_key=? AND api_keys.status='active'
    """, (api_key,))

    row = c.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "user_id": row[0],
        "credits": row[1]
    }