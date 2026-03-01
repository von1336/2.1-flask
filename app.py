from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  # кириллица в ответах без \uXXXX

ads = {}
AD_FIELDS = ("title", "description", "owner")


def ad_to_dict(ad_id, ad):
    return {
        "id": ad_id,
        "title": ad["title"],
        "description": ad["description"],
        "created_at": ad["created_at"],
        "owner": ad["owner"],
    }


@app.route("/")
def index():
    return jsonify({
        "message": "REST API объявлений",
        "endpoints": {
            "GET /advertisement": "список объявлений",
            "POST /advertisement": "создать (JSON: title, description, owner)",
            "GET /advertisement/{id}": "получить объявление",
            "PATCH /advertisement/{id}": "обновить",
            "DELETE /advertisement/{id}": "удалить",
        },
    })


@app.route("/advertisement", methods=["POST"])
def create_ad():
    data = request.get_json() or {}
    if not all(k in data for k in AD_FIELDS):
        return jsonify({"error": "Missing fields: title, description, owner"}), 400
    ad_id = str(uuid.uuid4())
    ads[ad_id] = {
        "title": data["title"],
        "description": data["description"],
        "owner": data["owner"],
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    return jsonify(ad_to_dict(ad_id, ads[ad_id])), 201


@app.route("/advertisement/<ad_id>", methods=["GET"])
def get_ad(ad_id):
    if ad_id not in ads:
        return jsonify({"error": "Not found"}), 404
    return jsonify(ad_to_dict(ad_id, ads[ad_id]))


@app.route("/advertisement/<ad_id>", methods=["PATCH"])
def update_ad(ad_id):
    if ad_id not in ads:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json() or {}
    for key in ("title", "description", "owner"):
        if key in data:
            ads[ad_id][key] = data[key]
    return jsonify(ad_to_dict(ad_id, ads[ad_id]))


@app.route("/advertisement/<ad_id>", methods=["DELETE"])
def delete_ad(ad_id):
    if ad_id not in ads:
        return jsonify({"error": "Not found"}), 404
    del ads[ad_id]
    return "", 204


@app.route("/advertisement", methods=["GET"])
def list_ads():
    return jsonify([ad_to_dict(i, a) for i, a in ads.items()])


@app.route("/favicon.ico")
def favicon():
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
