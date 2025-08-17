# ChatGenerator 🧩

Built For Elyx Life Hackathon by **Swarit Srivastava** and **Vansh Srivas**

---

## 📌 Overview
ChatGenerator is a full-stack project that simulates and visualizes **synthetic WhatsApp-style health coaching journeys**.  
It generates journeys (back-end powered by Flask + LangChain + Mistral AI) and visualizes them (front-end powered by React + Vite + Tailwind).

- **Backend (`chatgenerator-backend`)**: Flask API that generates journeys, handles test reports, and provides structured summaries.  
- **Frontend (`chatgenerator-frontend`)**: React + Vite app deployed on Netlify to visualize chat bubbles and journey data.

---

## ⚡ Tech Stack
- **Backend**: Python, Flask, LangChain, MistralAI, dotenv, Flask-CORS  
- **Frontend**: React (Vite), TailwindCSS, ShadCN UI, Recharts  
- **Deployment**:  
  - Backend → Render / Railway / Heroku  
  - Frontend → Netlify  

---

## 🚀 Getting Started

### 1. Clone Repo
```bash
git clone https://github.com/<your-username>/chatgenerator.git
cd chatgenerator
```
### 2. Backend Setup (chatgenerator-backend)
```bash
  cd chatgenerator-backend
  python -m venv venv
  source venv/bin/activate   # (Linux/Mac)
  venv\Scripts\activate      # (Windows)
  
  pip install -r requirements.txt
```
###Create a .env file inside chatgenerator-backend/:
```bash
  MISTRAL_API_KEY=your_api_key_here
```
### Run backend locally:
```bash
  python app.py
```
This starts the API on http://localhost:5000.

### 3. Frontend Setup (chatgenerator-frontend)
```bash
  cd ../chatgenerator-frontend
  npm install
  npm run dev
```
Frontend runs at http://localhost:5173.
For production build:
```bash
npm run build
```
### 🌍 Deployment

## Backend

1.Deploy on Render, Railway, or Heroku.
2.Add your MISTRAL_API_KEY in environment variables.
3.Make sure Procfile contains:
``` bash
web: gunicorn app:app
```
## Frontend

Deploy on Netlify.
Add a netlify.toml in root of chatgenerator-frontend/:
```bash
[build]
  command = "npm run build"
  publish = "dist"
```
Publish directory: dist

## 📡 API Documentation

### 🔹 1. Generate Journey
**Endpoint**:  

# POST /generate

**Description**:  
Generates the full health journey JSON (not downloadable, direct response).

**Request Body**:
```json
{
  "name": "Rohan Patel",
  "condition": "High BP",
  "start_year": 2024,
  "start_month": 8,
  "months": 8
}
```
# Response 
```json
{
  "month_index": 1,
  "month": "August",
  "theme": "The Urgent Plea & The Skeptical Hand-off",
  "week": 1,
  "messages": [ ... ]
}
```
# POST /generate/download

**Description**: 
Generates the journey and returns it as a downloadable .json file.
```json
{
  "name": "Rohan Patel",
  "condition": "High BP",
  "start_year": 2024,
  "start_month": 8,
  "months": 8
}
```
# Response:
application/json file download → Rohan_Patel_journey.json

# POST /visualize

**Description**: 
Takes journey JSON and summarizes it into 6 episodes with structured fields.
```json
{ "chat_data": { ...full_journey_json... } }
```
# Response 
```json
[
  {
    "episode": 1,
    "title": "Initial Setup and Goal Clarification",
    "date_range": "June 1-10",
    "primary_goal_trigger": "User requests assistance with project setup and goal definition",
    "triggered_by": "User",
    "friction_points": ["Unclear project scope", "Lack of initial documentation"],
    "final_outcome": "Project goals and initial setup documented",
    "persona_analysis": {
      "before_state": "Unclear about project objectives and requirements",
      "after_state": "Clear understanding of project goals and initial steps"
    },
    "metrics": {
      "response_time": "2 hours 15 minutes",
      "time_to_resolution": "5 days"
    }
  }
]
```
📊 Features

- Generates 8-month WhatsApp-style health journey for a member.
- Inserts quarterly diagnostic test results into timeline.
- Summarizes chat into 6 structured episodes.

Interactive visualization with chat bubbles + charts.

👥 Authors
Swarit Srivastava
Vansh Srivas
