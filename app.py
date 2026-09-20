import os

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

WHATSAPP_GROUP_LINK = "https://chat.whatsapp.com/Hdxzv4Lr0R24hKDCEglSJx"


@app.route("/")
def index():
    return render_template("index.html", whatsapp_group_link=WHATSAPP_GROUP_LINK)


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
