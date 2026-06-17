from flask import Blueprint, request
from db import db
import time

webhook_bp = Blueprint("webhook", __name__)


@webhook_bp.route("/paypal-success", methods=["POST"])
def paypal_success():

    data = request.get_json()

    user_id = data.get("user_id")
    amount = 5

    credits = 100

    conn = db()
    c = conn.cursor()

    # 加 credits
    c.execute("""
        UPDATE users SET credits = credits + ?
        WHERE id=?
    """, (credits, user_id))

    # 记录充值
    c.execute("""
        INSERT INTO payments (user_id, amount, credits_added, provider, created_at)
        VALUES (?, ?, ?, 'paypal', ?)
    """, (user_id, amount, credits, time.time()))

    conn.commit()
    conn.close()

    return {"status": "ok"}