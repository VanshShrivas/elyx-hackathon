from flask import Flask, request, jsonify, send_file
from generator.journey import generate_full_journey
import tempfile
import os
import json
from flask_cors import CORS
from generator.prompts import summarize_chat

app = Flask(__name__)
CORS(app , resources={r"/*": {"origins": "http://localhost:5173"}})
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    print("📩 /generate POST request received:", data)
    name = data.get("name")
    if not name:
        return jsonify({"error": "Member name is required"}), 400
    
    condition = data.get("condition", "none")
    start_year = data.get("start_year", 2024)
    start_month = data.get("start_month", 8)
    months = data.get("months", 8)

    try:
        journey = generate_full_journey(
            member_name=name,
            condition=condition,
            start_year=start_year,
            start_month=start_month,
            months=months
        )
        return jsonify(journey)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/generate/download", methods=["POST"])
def generate_and_download():
    """Generate JSON and return as downloadable file."""
    data = request.get_json(force=True)
    print("📩 /generate POST request received:", data)
    name = data.get("name")
    if not name:
        return jsonify({"error": "Member name is required"}), 400
    
    condition = data.get("condition", "none")
    start_year = data.get("start_year", 2024)
    start_month = data.get("start_month", 8)
    months = data.get("months", 8)

    try:
        print("➡️ Starting journey generation...")
        journey = generate_full_journey(
            member_name=name,
            condition=condition,
            start_year=start_year,
            start_month=start_month,
            months=months
        )
        print("Done")
        # Save into temp file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        with open(tmp.name, "w", encoding="utf-8") as f:
            json.dump(journey, f, ensure_ascii=False, indent=2)

        filename = f"{name.replace(' ', '_')}_journey.json"
        print("8-month chat data generated and saved to chat_data.json")
        return send_file(tmp.name, as_attachment=True, download_name=filename, mimetype="application/json")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/visualize", methods=["POST"])
def visualize():
    try:
        chat_data = request.get_json(force=True)
        episodes = summarize_chat(chat_data)
        return jsonify(episodes)   # ✅ returns array, not wrapped string
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)