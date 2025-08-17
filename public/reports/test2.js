const testData2 = {
  test_id: "test_2025_02",
  date: "2025-02-15",
  member: "Rohan Patel",
  general_health: {
    clinical_history: "Reports improved stamina after diet change, but occasional dizziness.",
    physical_exam: "BMI 25.8, waist circumference improved by 2cm.",
    vital_signs: {
      blood_pressure: "128/82 mmHg",
      heart_rate: 72,
      bmi: 25.8
    },
    blood_tests: {
      ogtt_insulin: "Normal",
      lipid_profile: {
        cholesterol_total: 198,
        ldl: 118,
        hdl: 50,
        triglycerides: 160,
        apob_apoa: "Improved since last test"
      },
      fbc: "Normal",
      liver_kidney: "Normal LFT/KFT",
      micronutrient_panel: "Vitamin D improved with supplementation, Omega-3 borderline",
      esr_crp: "CRP normal (1.2 mg/L)",
      biological: "TruAge: biological age equal to chronological age",
      thyroid: {
        TSH: 1.9,
        T3: 4.3,
        T4: 1.4,
        cortisol: "Normal"
      },
      sex_hormones: {
        testosterone: "Normal",
        estradiol: "Normal"
      },
      heavy_metals: "No significant elevation",
      apoe4: "Negative",
      epigenetic: "Stable"
    },
    urinalysis: "Normal"
  },
  cancer_screening: {
    colorectal: "FIT negative",
    colonoscopy: "Not indicated",
    breast_cervical: "Not applicable"
  },
  advanced_cardiovascular: {
    ecg: "Normal",
    coronary_calcium: "Score 20 (stable, no progression)",
    cimt: "No significant progression"
  },
  overall_fitness: {
    vo2max: "45 ml/kg/min (above average)",
    grip_strength: "Improved (28kg)",
    fms: "Better hip stability",
    spirometry: "Normal"
  },
  genetic_testing: {
    hereditary_risk: "No change",
    pharmacogenomics: "No new findings"
  },
  body_composition: {
    dexa: "22% body fat, normal bone density"
  },
  nutritional_assessment: {
    micronutrients: "Improved Vitamin D and zinc levels",
    food_allergies: "No new findings",
    gut_microbiome: "Improved diversity, higher bifidobacteria"
  },
  brain_health: {
    cognitive_function: "Normal",
    mental_health: "Reduced anxiety, stable mood",
    mri: "Normal"
  },
  skin_analysis: {
    visia: "Improved hydration, less pigmentation"
  },
  extended_care: {
    consultations: ["Physiotherapist", "Endocrinologist"],
    recommendations: "Maintain current plan, consider HIIT for endurance boost"
  },
  summary: "Significant improvement in cardiovascular risk markers, inflammation resolved, fitness improved. Condition stabilizing with current lifestyle plan."
};
export default testData2;
