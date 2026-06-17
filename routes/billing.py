from flask import Blueprint, request, jsonify
from db import db

billing_bp = Blueprint("billing", __name__)


@billing_bp.route("/add-credits", methods=["POST"])
def add_credits():

    user_id = request.json.get("user_id")
    amount = request.json.get("amount", 10)

    conn = db()
    c = conn.cursor()

    c.execute("""
        UPDATE users SET credits = credits + ?
        WHERE id=?
    """, (amount, user_id))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "ok",
        "added": amount
    })