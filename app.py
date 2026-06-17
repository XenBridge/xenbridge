from flask import Flask
from db import init_db

from routes.chat import chat_bp
from routes.auth import auth_bp
from routes.billing import billing_bp
from routes.webhooks import webhook_bp

app = Flask(__name__)

init_db()

app.register_blueprint(chat_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(billing_bp)
app.register_blueprint(webhook_bp)


@app.route("/")
def home():
    return {"status": "XenBridge V2 running"}


if __name__ == "__main__":
    app.run(debug=True)