import { useState } from "react";

export default function GenerateForm() {
  const [name, setName] = useState("Rohan Patel");
  const [condition, setCondition] = useState("");
  const [months, setMonths] = useState(8);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);

    try {
      const response = await fetch("https://elyx-hackathon-backend.onrender.com/generate/download", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, condition, months }),
      });

      if (!response.ok) throw new Error("Failed to generate file");

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      // Download
      const a = document.createElement("a");
      a.href = url;
      a.download = `${name.replace(" ", "_")}_journey.json`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow rounded-xl p-6 max-w-lg mx-auto">
      <h2 className="text-xl font-semibold mb-4">Generate New Journey</h2>

      <div className="space-y-4">


        <button
          onClick={handleGenerate}
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-600"
          disabled={loading}
        >
          {loading ? "⏳ Generating... Please wait" : "Generate & Download"}
        </button>
      </div>

      {loading && (
        <div className="mt-6 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500 border-opacity-50 mx-auto"></div>
          <p className="mt-2 text-gray-600">
            This may take up to 5–10 minutes...
          </p>
        </div>
      )}
      <div class="max-w-md mx-auto mt-8 p-6 bg-white rounded-2xl shadow-lg">
        <h2 class="text-xl font-bold mb-4 text-gray-800">Downloadable Datasets</h2>

        <ul class="space-y-3">
          <li>
            <a href="/datasets_examples/example1.json" download
              class="block px-4 py-2 rounded-lg bg-blue-500 text-white font-medium hover:bg-blue-600 transition">
              Download Example 1
            </a>
          </li>
          <li>
            <a href="/datasets_examples/example2.json" download
              class="block px-4 py-2 rounded-lg bg-green-500 text-white font-medium hover:bg-green-600 transition">
              Download Example 2
            </a>
          </li>
        </ul>
      </div>

    </div>
  );
}
