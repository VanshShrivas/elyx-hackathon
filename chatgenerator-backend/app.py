from flask import Flask, request, jsonify, send_file
from generator.journey import generate_full_journey
import tempfile
import os
import json
from flask_cors import CORS
from generator.prompts import summarize_chat

test_reports = [
  {
    "test_id": "test_2024_11",
    "date": "2024-11-12",
    "member": "Rohan Patel",
    "general_health": {
      "clinical_history": "Reports fatigue after moderate exercise, family history of hypertension.",
      "physical_exam": "BMI 26.5 (slightly overweight), normal physical exam otherwise.",
      "vital_signs": {
        "blood_pressure": "138/88 mmHg",
        "heart_rate": 78,
        "bmi": 26.5
      },
      "blood_tests": {
        "ogtt_insulin": "Normal glucose tolerance, mildly elevated fasting insulin",
        "lipid_profile": {
          "cholesterol_total": 215,
          "ldl": 135,
          "hdl": 45,
          "triglycerides": 180,
          "apob_apoa": "Elevated ApoB/ApoA ratio"
        },
        "fbc": "Within normal range",
        "liver_kidney": "Normal LFT/KFT",
        "micronutrient_panel": "Low Vitamin D, borderline low Omega-3 index",
        "esr_crp": "CRP mildly elevated (3.5 mg/L)",
        "biological": "TruAge: biological age 1.8 years > chronological age",
        "thyroid": {
          "TSH": 2.1,
          "T3": 4.1,
          "T4": 1.2,
          "cortisol": "Normal"
        },
        "sex_hormones": {
          "testosterone": "Normal age-adjusted",
          "estradiol": "Low-normal"
        },
        "heavy_metals": "Mercury mildly elevated",
        "apoe4": "Negative",
        "epigenetic": "Mild methylation drift"
      },
      "urinalysis": "Normal"
    },
    "cancer_screening": {
      "colorectal": "FIT negative",
      "colonoscopy": "Not indicated at this time",
      "breast_cervical": "Not applicable"
    },
    "advanced_cardiovascular": {
      "ecg": "Normal sinus rhythm",
      "coronary_calcium": "Score 25 (mild plaque burden)",
      "cimt": "Mild intima thickening, early atherosclerosis"
    },
    "overall_fitness": {
      "vo2max": "42 ml/kg/min (average for age)",
      "grip_strength": "Lower than expected (hand dynamometer: 25kg)",
      "fms": "Deficit in hip stability",
      "spirometry": "Normal"
    },
    "genetic_testing": {
      "hereditary_risk": "Moderate risk for type 2 diabetes (family history)",
      "pharmacogenomics": "No significant drug-gene interactions"
    },
    "body_composition": {
      "dexa": "24% body fat, normal bone density"
    },
    "nutritional_assessment": {
      "micronutrients": "Low vitamin D, borderline zinc",
      "food_allergies": "Mild lactose intolerance",
      "gut_microbiome": "Reduced diversity, low bifidobacteria"
    },
    "brain_health": {
      "cognitive_function": "Normal memory, mild attention deficits",
      "mental_health": "Mild anxiety reported",
      "mri": "No abnormalities"
    },
    "skin_analysis": {
      "visia": "Mild sun damage, early pigmentation"
    },
    "extended_care": {
      "consultations": ["Cardiologist", "Nutritionist"],
      "recommendations": "Reduce saturated fats, increase Omega-3, structured resistance training"
    },
    "summary": "Mild hypertension, early signs of metabolic syndrome, low vitamin D, early vascular changes. Lifestyle intervention recommended."
  },
  {
    "test_id": "test_2025_02",
    "date": "2025-02-15",
    "member": "Rohan Patel",
    "general_health": {
      "clinical_history": "Reports improved stamina after diet change, but occasional dizziness.",
      "physical_exam": "BMI 25.8, waist circumference improved by 2cm.",
      "vital_signs": {
        "blood_pressure": "128/82 mmHg",
        "heart_rate": 72,
        "bmi": 25.8
      },
      "blood_tests": {
        "ogtt_insulin": "Normal",
        "lipid_profile": {
          "cholesterol_total": 198,
          "ldl": 118,
          "hdl": 50,
          "triglycerides": 160,
          "apob_apoa": "Improved since last test"
        },
        "fbc": "Normal",
        "liver_kidney": "Normal LFT/KFT",
        "micronutrient_panel": "Vitamin D improved with supplementation, Omega-3 borderline",
        "esr_crp": "CRP normal (1.2 mg/L)",
        "biological": "TruAge: biological age equal to chronological age",
        "thyroid": {
          "TSH": 1.9,
          "T3": 4.3,
          "T4": 1.4,
          "cortisol": "Normal"
        },
        "sex_hormones": {
          "testosterone": "Normal",
          "estradiol": "Normal"
        },
        "heavy_metals": "No significant elevation",
        "apoe4": "Negative",
        "epigenetic": "Stable"
      },
      "urinalysis": "Normal"
    },
    "cancer_screening": {
      "colorectal": "FIT negative",
      "colonoscopy": "Not indicated",
      "breast_cervical": "Not applicable"
    },
    "advanced_cardiovascular": {
      "ecg": "Normal",
      "coronary_calcium": "Score 20 (stable, no progression)",
      "cimt": "No significant progression"
    },
    "overall_fitness": {
      "vo2max": "45 ml/kg/min (above average)",
      "grip_strength": "Improved (28kg)",
      "fms": "Better hip stability",
      "spirometry": "Normal"
    },
    "genetic_testing": {
      "hereditary_risk": "No change",
      "pharmacogenomics": "No new findings"
    },
    "body_composition": {
      "dexa": "22% body fat, normal bone density"
    },
    "nutritional_assessment": {
      "micronutrients": "Improved Vitamin D and zinc levels",
      "food_allergies": "Mild lactose intolerance",
      "gut_microbiome": "Improved diversity, higher bifidobacteria"
    },
    "brain_health": {
      "cognitive_function": "Normal",
      "mental_health": "Reduced anxiety, stable mood",
      "mri": "Normal"
    },
    "skin_analysis": {
      "visia": "Improved hydration, less pigmentation"
    },
    "extended_care": {
      "consultations": ["Physiotherapist", "Endocrinologist"],
      "recommendations": "Maintain current plan, consider HIIT for endurance boost"
    },
    "summary": "Significant improvement in cardiovascular risk markers, inflammation resolved, fitness improved. Condition stabilizing with current lifestyle plan."
    }
]

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
            "Rohan Patel",
            "HighBP",
            test_reports,
            start_year=2024,
            start_month=8,
            months=8
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