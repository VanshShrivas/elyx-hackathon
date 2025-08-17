const testData1 = {
  test_id: "test_2024_11",
  date: "2024-11-12",
  member: "Rohan Patel",
  general_health: {
    clinical_history: "Reports fatigue after moderate exercise, family history of hypertension.",
    physical_exam: "BMI 26.5 (slightly overweight), normal physical exam otherwise.",
    vital_signs: {
      blood_pressure: "138/88 mmHg",
      heart_rate: 78,
      bmi: 26.5
    },
    blood_tests: {
      ogtt_insulin: "Normal glucose tolerance, mildly elevated fasting insulin",
      lipid_profile: {
        cholesterol_total: 215,
        ldl: 135,
        hdl: 45,
        triglycerides: 180,
        apob_apoa: "Elevated ApoB/ApoA ratio"
      },
      fbc: "Within normal range",
      liver_kidney: "Normal LFT/KFT",
      micronutrient_panel: "Low Vitamin D, borderline low Omega-3 index",
      esr_crp: "CRP mildly elevated (3.5 mg/L)",
      biological: "TruAge: biological age 1.8 years > chronological age",
      thyroid: {
        TSH: 2.1,
        T3: 4.1,
        T4: 1.2,
        cortisol: "Normal"
      },
      sex_hormones: {
        testosterone: "Normal age-adjusted",
        estradiol: "Low-normal"
      },
      heavy_metals: "Mercury mildly elevated",
      apoe4: "Negative",
      epigenetic: "Mild methylation drift"
    },
    urinalysis: "Normal"
  },
  cancer_screening: {
    colorectal: "FIT negative",
    colonoscopy: "Not indicated at this time",
    breast_cervical: "Not applicable"
  },
  advanced_cardiovascular: {
    ecg: "Normal sinus rhythm",
    coronary_calcium: "Score 25 (mild plaque burden)",
    cimt: "Mild intima thickening, early atherosclerosis"
  },
  overall_fitness: {
    vo2max: "42 ml/kg/min (average for age)",
    grip_strength: "Lower than expected (hand dynamometer: 25kg)",
    fms: "Deficit in hip stability",
    spirometry: "Normal"
  },
  genetic_testing: {
    hereditary_risk: "Moderate risk for type 2 diabetes (family history)",
    pharmacogenomics: "No significant drug-gene interactions"
  },
  body_composition: {
    dexa: "24% body fat, normal bone density"
  },
  nutritional_assessment: {
    micronutrients: "Low vitamin D, borderline zinc",
    food_allergies: "Mild lactose intolerance",
    gut_microbiome: "Reduced diversity, low bifidobacteria"
  },
  brain_health: {
    cognitive_function: "Normal memory, mild attention deficits",
    mental_health: "Mild anxiety reported",
    mri: "No abnormalities"
  },
  skin_analysis: {
    visia: "Mild sun damage, early pigmentation"
  },
  extended_care: {
    consultations: ["Cardiologist", "Nutritionist"],
    recommendations: "Reduce saturated fats, increase Omega-3, structured resistance training"
  },
  summary: "Mild hypertension, early signs of metabolic syndrome, low vitamin D, early vascular changes. Lifestyle intervention recommended."
};
export default testData1;