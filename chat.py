from flask import Blueprint, request, jsonify
from auth import verify_key
from db import db
from services.openai_service import ask_openai
import time

chat_bp = Blueprint("chat", __name__)

# 简单防刷
last_request = {}


def rate_limit(key):
    now = time.time()
    if key in last_request:
        if now - last_request[key] < 1:
            return False
    last_request[key] = now
    return True


@chat_bp.route("/chat", methods=["POST"])
def chat():

    # ① 读取 key
    api_key = request.headers.get("x-api-key")
    data = request.get_json()

    message = data.get("message")

    if not message:
        return jsonify({"error": "missing message"}), 400

    # ② 验证 key
    user = verify_key(api_key)

    if not user:
        return jsonify({"error": "invalid api key"}), 401

    # ③ 限流
    if not rate_limit(api_key):
        return jsonify({"error": "too fast"}), 429

    # ④ 检查余额
    if user["credits"] <= 0:
        return jsonify({"error": "no credits"}), 402

    # ⑤ 调 OpenAI
    reply = ask_openai(message)

    # ⑥ 扣费
    new_balance = user["credits"] - 1

    conn = db()
    c = conn.cursor()

    c.execute("UPDATE users SET credits=? WHERE id=?",
              (new_balance, user["user_id"]))

    conn.commit()
    conn.close()

    # ⑦ 返回
    return jsonify({
        "reply": reply,
        "credits_left": new_balance
    })