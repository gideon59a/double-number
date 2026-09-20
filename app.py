import base64
import os

from dotenv import load_dotenv
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB max upload

# Falls back to a local SQLite file when DATABASE_URL isn't set, so the app
# still runs out of the box. Set DATABASE_URL (e.g. to a Render Postgres
# instance) to use a real, persistent database instead.
database_url = os.environ.get("DATABASE_URL", "sqlite:///local.db")
if database_url.startswith("postgres://"):
    # Render/Heroku give out "postgres://" URLs; SQLAlchemy's driver needs "postgresql://"
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/Hdxzv4Lr0R24hKDCEglSJx"
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/gif", "image/webp"}


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_data_url = db.Column(db.Text, nullable=True)
    text = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html", whatsapp_group_link=WHATSAPP_GROUP_LINK)


@app.route("/provider", methods=["GET", "POST"])
def provider():
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        link = request.form.get("link", "").strip()
        image_file = request.files.get("image")

        if not text or not link:
            flash("Text and link are both required.")
            return redirect(url_for("provider"))

        image_data_url = None
        if image_file and image_file.filename:
            if image_file.mimetype not in ALLOWED_IMAGE_TYPES:
                flash("Image must be PNG, JPEG, GIF, or WebP.")
                return redirect(url_for("provider"))
            encoded = base64.b64encode(image_file.read()).decode("ascii")
            image_data_url = f"data:{image_file.mimetype};base64,{encoded}"

        db.session.add(Entry(image_data_url=image_data_url, text=text, link=link))
        db.session.commit()
        return redirect(url_for("provider"))

    entries = Entry.query.order_by(Entry.created_at.desc()).all()
    return render_template("provider.html", entries=entries)


@app.route("/api/double", methods=["POST"])
def double():
    data = request.get_json(silent=True) or {}
    try:
        number = float(data["number"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "A valid 'number' is required."}), 400
    return jsonify({"result": number * 2})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
