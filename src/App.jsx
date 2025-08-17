import { useState } from "react";
import ChatView from "./components/ChatView";
import Visualizer from "./components/Visualizer";
import GenerateForm from "./components/GenerateForm";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";

export default function App() {
  const [chatData, setChatData] = useState(null);
  const [activePage, setActivePage] = useState(null); // "generate" | "visualize" | null

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          setChatData(data);
        } catch (err) {
          alert("Invalid JSON file!");
        }
      };
      reader.readAsText(file);
    } else {
      alert("Please upload a valid JSON file.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold mb-4 text-center">
        📊 Elyx Journey Visualizer
      </h1>

      {/* Step 1 → Ask user what they want */}
      {!chatData && !activePage && (
        <div className="flex gap-4 items-center">
          <button
            className="px-6 py-3 bg-blue-500 text-white rounded-xl shadow hover:bg-blue-600"
            onClick={() => setActivePage("generate")}
          >
            Generate
          </button>
          <button
            className="px-6 py-3 bg-green-500 text-white rounded-xl shadow hover:bg-green-600"
            onClick={() => setActivePage("visualize")}
          >
            Visualize
          </button>
        </div>
      )}

      {/* Step 2 → If Generate clicked */}
      {activePage === "generate" && <GenerateForm />}

      {/* Step 2 → If Visualize clicked but file not uploaded */}
      {activePage === "visualize" && !chatData && (
        <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-400 rounded-xl p-10 bg-white shadow">
          <p className="mb-4 text-green-700">
            Drag & Drop your <code>chat_data.json</code> here
          </p>
          <input
            className="cursor-pointer border-2 border-black-400"
            type="file"
            accept=".json"
            onChange={handleFileUpload}
          />
        </div>
      )}

      {/* Step 3 → After file upload, show Router-based pages */}
      {chatData && (
        <Router>
          <div className="p-4">
            {/* Navigation */}
            <nav className="flex space-x-4 mb-6">
              <Link
                to="/"
                className="w-28 flex flex-col items-center justify-center border-2 border-dashed border-blue-400 rounded-xl p-2"
              >
                Chat
              </Link>

              <Link
                to="/visualizer"
                className="w-28 flex flex-col items-center justify-center border-2 border-dashed border-green-400 rounded-xl p-2"
              >
                Visualizer
              </Link>
            </nav>

            {/* Routes */}
            <Routes>
              <Route path="/" element={<ChatView data={chatData} />} />
              <Route path="/visualizer" element={<Visualizer data={chatData} />} />
            </Routes>
          </div>
        </Router>
      )}
    </div>
  );
}
