import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function TestVisualizer({ testData }) {
  if (!testData) return <p className="text-center">No test data provided</p>;

  const { general_health, overall_fitness, body_composition, lipid_profile } = testData;

  // Vital Signs Chart
  const vitalSignsData = {
    labels: ["Heart Rate", "BMI"],
    datasets: [
      {
        label: "Vital Signs",
        data: [general_health.vital_signs.heart_rate, general_health.vital_signs.bmi],
        backgroundColor: "rgba(59, 130, 246, 0.7)",
      },
    ],
  };

  // Lipid Profile Chart
  const lipidData = {
    labels: ["Total Cholesterol", "LDL", "HDL", "Triglycerides"],
    datasets: [
      {
        label: "Lipid Profile",
        data: [
          general_health.blood_tests.lipid_profile.cholesterol_total,
          general_health.blood_tests.lipid_profile.ldl,
          general_health.blood_tests.lipid_profile.hdl,
          general_health.blood_tests.lipid_profile.triglycerides,
        ],
        backgroundColor: "rgba(16, 185, 129, 0.7)",
      },
    ],
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="border rounded-lg p-4 bg-white shadow">
        <h2 className="text-xl font-bold text-blue-600">
          {testData.member} - {testData.test_id} ({testData.date})
        </h2>
        <p className="mt-2 text-gray-700 font-semibold">Summary:</p>
        <p className="text-gray-700">{testData.summary}</p>
      </div>

      {/* Vital Signs */}
      <div className="border rounded-lg p-4 bg-white shadow">
        <h3 className="font-semibold text-blue-600 mb-2">Vital Signs</h3>
        <Bar data={vitalSignsData} options={{ responsive: true }} />
      </div>

      {/* Lipid Profile */}
      <div className="border rounded-lg p-4 bg-white shadow">
        <h3 className="font-semibold text-green-600 mb-2">Lipid Profile</h3>
        <Bar data={lipidData} options={{ responsive: true }} />
      </div>

      {/* Other Textual Sections */}
      <div className="grid grid-cols-2 gap-4">
        <div className="border rounded-lg p-4 bg-yellow-50">
          <h4 className="font-semibold text-yellow-700">Overall Fitness</h4>
          <p>VO2max: {overall_fitness.vo2max}</p>
          <p>Grip Strength: {overall_fitness.grip_strength}</p>
          <p>FMS: {overall_fitness.fms}</p>
        </div>

        <div className="border rounded-lg p-4 bg-pink-50">
          <h4 className="font-semibold text-pink-700">Body Composition</h4>
          <p>DEXA: {body_composition.dexa}</p>
        </div>
      </div>

      <div className="border rounded-lg p-4 bg-gray-50">
        <h4 className="font-semibold text-gray-700">Extended Care</h4>
        <p>Consultations: {testData.extended_care.consultations.join(", ")}</p>
        <p>Recommendations: {testData.extended_care.recommendations}</p>
      </div>
    </div>
  );
}
