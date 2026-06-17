from flask import Blueprint, request, jsonify
from middleware.auth import verify_key
from services.openai import ask_openai
from db import db
import time

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/v1/chat", methods=["POST"])
def chat():

    api_key = request.headers.get("x-api-key")
    data = request.get_json()

    message = data.get("message")

    user = verify_key(api_key)

    if not user:
        return {"error": "invalid key"}, 401

    if user["credits"] <= 0:
        return {"error": "no credits"}, 402

    # AI
    reply = ask_openai(message)

    # 扣费（1 request = 1 credit）
    new_balance = user["credits"] - 1

    conn = db()
    c = conn.cursor()

    c.execute("UPDATE users SET credits=? WHERE id=?",
              (new_balance, user["user_id"]))

    # 记录请求（🔥 V2新增）
    c.execute("""
        INSERT INTO requests (user_id, endpoint, cost, created_at)
        VALUES (?, '/v1/chat', 1, ?)
    """, (user["user_id"], time.time()))

    conn.commit()
    conn.close()

    return {
        "reply": reply,
        "credits_left": new_balance
    }