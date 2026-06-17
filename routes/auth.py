from flask import Blueprint, request, jsonify
from db import db
import secrets
import time

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/create-user", methods=["POST"])
def create_user():

    name = request.json.get("name")

    conn = db()
    c = conn.cursor()

    # 创建用户
    c.execute("INSERT INTO users (name, credits) VALUES (?, 10)", (name,))
    user_id = c.lastrowid

    # 生成 API Key
    api_key = "xb_" + secrets.token_hex(16)

    c.execute("""
        INSERT INTO api_keys (user_id, api_key, created_at)
        VALUES (?, ?, ?)
    """, (user_id, api_key, time.time()))

    conn.commit()
    conn.close()

    return jsonify({
        "user_id": user_id,
        "api_key": api_key
    })