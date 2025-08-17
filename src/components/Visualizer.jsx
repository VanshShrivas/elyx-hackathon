import { useState } from "react";
import Journey from "../tabs/journey";
import TestVisualizer from "../tabs/tests";
import testData1 from "../../public/reports/test1";
import testData2 from "../../public/reports/test2";

export default function Visualizer({ data}) {
  const [activeTab, setActiveTab] = useState("journey");

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Tabs */}
      <div className="flex gap-4 mb-6 border-b pb-2 justify-center">
        <button
          onClick={() => setActiveTab("journey")}
          className={`px-6 py-2 rounded-t-lg ${
            activeTab === "journey" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
        >
          Journey
        </button>
        <button
          onClick={() => setActiveTab("test")}
          className={`px-6 py-2 rounded-t-lg ${
            activeTab === "test" ? "bg-green-600 text-white" : "bg-gray-200"
          }`}
        >
          Tests
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === "journey" && <Journey data={data} />}
      {activeTab === "test" && [testData1, testData2].map((td, idx) => (
  <TestVisualizer key={idx} testData={td} />
))}
    </div>
  );
}
