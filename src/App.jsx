import { useState } from "react";
import ChatView from "./components/ChatView";
import Visualizer from "./components/Visualizer";
import GenerateForm from "./components/GenerateForm";
import "./App.css";

export default function App() {
  const [chatData, setChatData] = useState(null);
  const [activePage, setActivePage] = useState(null); // "generate" | "visualize" | null
  const [activeCV, setActiveCV] = useState(true); // boolean
  const [v_data, setVdata] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          setChatData(data);
          handleRequest(data);
        } catch (err) {
          alert("Invalid JSON file!");
        }
      };
      reader.readAsText(file);
    } else {
      alert("Please upload a valid JSON file.");
    }
  };

  async function handleRequest(data) {
    try {
      const response = await fetch("https://elyx-hackathon-backend.onrender.com/visualize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error("Failed to generate file");

      const d = await response.json();
      setVdata(d);
    } catch (err) {
      console.log("Error:", err.message);
    }
  }

  return (
    <div
      className="flex flex-col justify-center items-center min-h-screen p-6 relative bg-cover bg-center"
      style={{ backgroundImage: "url('/images/bg.jpg')" }}
    >
      {/* Global Back Button */}
      {activePage !== null && (
        <button
          className="absolute top-6 left-6 px-4 py-2 border border-black-200 bg-white rounded-md shadow hover:bg-gray-100"
          onClick={() => {
            setActivePage(null);
            setChatData(null);
            setVdata(null);
          }}
        >
          ← Back
        </button>

      )}

      <h1 className="text-2xl font-bold mb-8 text-center text-black drop-shadow">
        📊 Elyx Journey Visualizer
      </h1>

      {/* Step 1 → Ask user what they want */}
      {!chatData && !activePage && (
        <div className="flex justify-center gap-4 items-center">
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
      {activePage === "generate" && (
        <div className="w-full max-w-2xl bg-white/80 rounded-xl shadow p-4">
          <GenerateForm />
        </div>
      )}

      {/* Step 2 → If Visualize clicked but file not uploaded */}
      {activePage === "visualize" && !chatData && (
        <div className="w-full max-w-xl flex flex-col items-center">
          <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-400 rounded-xl p-10 bg-white/80 shadow w-full">
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
        </div>
      )}

      {/* Step 3 → After file upload */}
      {chatData && (
        <div className="mt-6 w-full max-w-4xl bg-white/80 rounded-xl shadow p-4">
          <div className="flex justify-center gap-4 mb-4">
            <button
              className={`px-6 py-2 rounded-lg shadow ${activeCV ? "bg-blue-500 text-white" : "bg-gray-200"}`}
              onClick={() => setActiveCV(true)}
            >
              Chat
            </button>
            <button
              className={`px-6 py-2 rounded-lg shadow ${!activeCV ? "bg-green-500 text-white" : "bg-gray-200"}`}
              onClick={() => setActiveCV(false)}
            >
              Visualize
            </button>
          </div>

          {activeCV ? (
            <ChatView data={chatData} />
          ) : (
            <Visualizer data={v_data} />
          )}
        </div>
      )}
    </div>
  );
}
