from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List
import json
import re

calendar_months = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

theme_list = [
    "The Urgent Plea & The Skeptical Hand-off",
    "Resistance & Reframing",
    "The Relapse",
    "Breakthrough & Pushback",
    "The Travel Test",
    "The Diagnostic Reset",
    "The Plateau",
    "The Wrap-up & New Beginning"
]
# ------START MONTH CALCULATION -----------
start_month_index = 8  # Example: August onboarding
month_list = [calendar_months[(start_month_index-1 + i) % 12] for i in range(8)]


import datetime

# Example: start in August 2023
start_date = datetime.datetime(2023, start_month_index, 1)

def get_week_start_date(start_date, month_offset, week_num):
    # Shift by full months first
    year = start_date.year + ((start_date.month - 1 + month_offset) // 12)
    month = (start_date.month - 1 + month_offset) % 12 + 1
    month_start = datetime.datetime(year, month, 1)

    # Week start = first day of that week (7-day intervals)
    return month_start + datetime.timedelta(weeks=(week_num - 1))


# ---- Define schema ----
class Decision(BaseModel):
    action: str
    reason: str
    trigger: str

class Message(BaseModel):
    id: str = Field(..., description="unique message ID")
    author: str = Field(..., description="sender (Rohan, Ruby, Dr. Warren, Carla, Advik, Rachel, Neel)")
    role: str = Field(..., description="member|concierge|doctor|nutritionist|physiotherapist|scientist|lead")
    text: str = Field(..., description="actual WhatsApp-style message text")
    decision: Optional[Decision] = Field(None, description="action taken (optional)")
    timestamp: str = Field(..., description="ISO format datetime string: YYYY-MM-DD HH:MM")

class ChatWeek(BaseModel):
    month_index: int
    month: str
    theme: str
    week: int
    messages: List[Message]

parser = PydanticOutputParser(pydantic_object=ChatWeek)

# ---- Define prompt ----
template =  """
You are Elyx Chat Generator.
Your job is to create synthetic **WhatsApp-style JSON chat histories**
between the Elyx Concierge Team and the member with the following profile :
Member’s profile
1. Member Snapshot
Preferred name: Rohan Patel
Date of birth, age, gender identity: 12 March 1979, 46, Male
Primary residence & frequent travel hubs: Singapore, frequently travels to UK,
US, South Korea, Jakarta
Occupation / business commitments: Regional Head of Sales for a FinTech
company with frequent international travel and high-stress demands.
Personal assistant: Sarah Tan
2. Core Outcomes & Time-Lines
Top three health or performance goals (with target dates):
Reduce risk of heart disease (due to family history) by maintaining healthy
cholesterol and blood pressure levels by December 2026.
Enhance cognitive function and focus for sustained mental performance in
demanding work environment by June 2026.
Implement annual full-body health screenings for early detection of debilitating
diseases, starting November 2025.
"Why now?" – intrinsic motivations & external drivers: Family history of heart
disease; wants to proactively manage health for long-term career performance and to
be present for his young children.
Success metrics the member cares about (e.g. VO₂max, biological age, stress
resilience): Blood panel markers (cholesterol, blood pressure, inflammatory
markers), cognitive assessment scores, sleep quality (Garmin data), stress resilience
(subjective self-assessment, Garmin HRV).
3. Behavioural & Psychosocial Insights
Personality / values assessment: Analytical, driven, values efficiency and
evidence-based approaches.
Stage of change & motivational interviewing notes: Highly motivated and ready
to act, but time-constrained. Needs clear, concise action plans and data-driven
insights.
Social support network – family, colleagues, clubs: Wife is supportive; has 2
young kids; employs a cook at home which helps with nutrition management.
Mental-health history, current therapist or psychiatrist: No formal mental health
history; manages work-related stress through exercise.
4. Tech Stack & Data Feeds
Wearables in use: Garmin watch (used for runs), considering Oura ring.
Health apps / platforms (Trainerize, MyFitnessPal, Whoop).
Data-sharing permissions & API access details: Willing to enable full data sharing
from Garmin and any new wearables for comprehensive integration and analysis.
Desired dashboards or report cadence: Monthly consolidated health report focusing
on key trends and actionable insights; quarterly deep-dive into specific health areas.
5. Service & Communication Preferences
Preferred channels important updates, and communication via PA (Sarah) for
scheduling.
Response-time expectations & escalation protocol: Expects responses within
24-48 hours for non-urgent inquiries. For urgent health concerns, contact his PA
immediately, who will then inform his wife.
Detail depth (executive summary vs granular data): Prefers executive summaries
with clear recommendations, but appreciates access to granular data upon request to
understand the underlying evidence.
Language, cultural or religious considerations: English, Indian cultural
background, no specific religious considerations impacting health services.
6. Scheduling & Logistics
Typical weekly availability blocks: Exercises every morning (20 min routine),
occasional runs. Often travels at least once every two weeks.
Upcoming travel calendar & time-zone shifts: Travel calendar provided by PA
(Sarah) on a monthly basis. Requires flexible scheduling and consideration for
time-zone adjustments during frequent travel (UK, US, South Korea, Jakarta).
On-site vs virtual appointment mix: Prefers virtual appointments due to travel, but
open to on-site for initial comprehensive assessments or specific procedures.
Transport: Will arrange his own transport.

Respond according to test reports after the test has been conducted as per the dates mentioned in reports.

### OUTPUT FORMAT
- Always output only a valid JSON object.
- Structure must be:
{{
  "month_index": {month_index},
  "month": "{month}",
  "theme": "{theme}",
  "week": {week},
  "messages": [
      {{
        "id": "m_week{week}_{{N}}",
        "author": "Name",
        "role": "member|concierge|doctor|nutritionist|physiotherapist|scientist|lead",
        "text": "short conversational WhatsApp-style text",
        "decision": {{
           "action": "...", "reason": "...", "trigger": "..."
        }} OR null,
        "timestamp": "YYYY-MM-DD HH:MM"
      }}
  ]
}}

### RULES
1. WhatsApp Style:
   - Short, natural, conversational.
   - Break explanations into multiple short messages.
   - Use emojis sparingly (😊, 👍, 📊, 🙌).
   - Max 5 member-initiated messages per week.

2. Elyx Team Voices:
   - Ruby (concierge): empathetic, proactive, organized.
   - Dr. Warren (doctor): authoritative, precise, clear.
   - Carla (nutritionist): practical, explains "why".
   - Rachel (physio): direct, encouraging.
   - Advik (scientist): analytical, data-driven.
   - Neel (lead): reassuring, big-picture.

3. Timeline Constraints:
   - One full diagnostic test every 3 months (Jan, Apr, Jul, Oct).
   - Exercise updated every 2 weeks.
   - One business travel week every month.
   - Member commits ~5 hrs/week on plan.
   - Member follows plan only ~50% → sometimes adjustments needed.
   - One chronic condition (e.g., high BP or high sugar) must persist.

4. Continuity:
   - Keep story flowing across weeks & months.
   - Use the given MONTH + THEME as narrative anchor.
   - Assume Singapore timezone/lifestyle context.

5. Time Rules:
   - Output each message with a `"timestamp"` in format `YYYY-MM-DD HH:MM`.
   - Use Singapore timezone.
   - Chats typically happen between 07:00–22:00.
   - Predict realistic gaps:
     • A few minutes between back-and-forth messages.
     • Several hours gap if conversation pauses.
     • Sometimes skip a full day (especially member delays).
   - Start each week on the first Monday of that week.

### CURRENT CONTEXT
Month: {month_index}
Month: {month}
Theme: {theme}
Week: {week}
Context: {context}

Now generate the WhatsApp chat in JSON with 15–30 messages following the rules.
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["month_index", "theme", "week", "context"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# ---- Connect to Mistral API ----
llm = ChatMistralAI(
    api_key="cMh3Pd9mNrDh42d6QzjRm96r1Z1zkyY3",
    model="mistral-small-latest",   # or mistral-medium, mistral-large
    temperature=0.7
)

# ---- Generate one week ----
month_index = 1
month = month_list[month_index - 1]
theme = theme_list[month_index - 1]
week = 1
member_name = "Rohan Patel"
condition = "High BP"

condition_text = f"{member_name} has the following condition(s): {condition}" if condition != "none" else ""

# Define the test reports
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


def generate_week(month_index: int, month: str, theme: str, week: int, context: str, member_name: str, condition: str, test_reports: List[dict]):
  """Generates a week of chat based on context, including test reports."""
  condition_text = f"{member_name} has the following condition(s): {condition}" if condition != "none" else ""

  # Include test reports in the context
  full_context = f"{context}\n\nTest Reports:\n{json.dumps(test_reports, indent=2)}"

  formatted_prompt = prompt.format(
      month_index=month_index,
      month=month,
      theme=theme,
      week=week,
      context=full_context
  )
  response = llm.invoke(formatted_prompt)
  return parser.parse(response.content)

def summarize_month(chat_weeks: List[ChatWeek]) -> str:
    """Summarizes all chats in a month into short context text"""
    summary = f"Last month ({chat_weeks[0].month}) summary:\n"
    for week in chat_weeks:
        highlights = []
        for msg in week.messages:
            # pick out major interventions or decisions
            if msg.role in ["doctor", "nutritionist", "physiotherapist", "lead"] or msg.decision:
                highlights.append(f"- {msg.author}: {msg.text}")
        if highlights:
            summary += f"\nWeek {week.week} highlights:\n" + "\n".join(highlights)
    return summary

def generate_month(month_index: int, month: str, theme: str, member_name: str, condition: str,
                   initial_context: str, test_reports: List[dict], previous_month_data: Optional[List[ChatWeek]] = None) -> List[ChatWeek]:
    """Generates 4 weeks of chats for a month. If not the first month, includes summary of last month in context."""

    # ---- Prepare context ----
    if previous_month_data is None:   # first month
        context = initial_context
    else:
        context = summarize_month(previous_month_data) + "\nStarting new month..."

    # ---- Generate 4 weeks ----
    month_weeks = []
    for week in range(1, 5):
        week_data = generate_week(month_index, month, theme, week, context, member_name, condition, test_reports)
        month_weeks.append(week_data)

        # Update context slightly for continuity in subsequent weeks
        context = f"Continuing {month}, Week {week} completed. Key highlights will flow into next week."

    return month_weeks

def get_month_year(start_year: int, start_month: int, offset: int):
    """
    Given a start year+month and an offset (0-based),
    return the correct (year, month) tuple.
    """
    year = start_year + ((start_month - 1 + offset) // 12)
    month = (start_month - 1 + offset) % 12 + 1
    return year, month


#-----------------------------SUMMARIZER------------------------------------#
from langchain.prompts import PromptTemplate
from langchain_mistralai import ChatMistralAI

class Episode(BaseModel):
    episode: int
    title: str
    date_range: str
    primary_goal_trigger: str
    triggered_by: str
    friction_points: List[str]
    final_outcome: str
    persona_analysis: dict
    metrics: dict

# Reuse the same LLM
summarizer_llm = ChatMistralAI(
    api_key="cMh3Pd9mNrDh42d6QzjRm96r1Z1zkyY3",
    model="mistral-small-latest",
    temperature=0.5
)

summary_template = """
You are Elyx Summarizer.
Summarize the chat JSON into structured 6 **episodes**.

Here is the chat {chat_json}
### REQUIRED JSON FORMAT
[
  {{
    "episode": <int>,
    "title": "<short descriptive title>",
    "date_range": "<Month Day-Day>",
    "primary_goal_trigger": "<text>",
    "triggered_by": "<who initiated>",
    "friction_points": ["<point1>", "<point2>", ...],
    "final_outcome": "<short outcome>",
    "persona_analysis": {{
      "before_state": "<text>",
      "after_state": "<text>"
    }},
    "metrics": {{
      "response_time": "<e.g., 3 hours 2 minutes>",
      "time_to_resolution": "<e.g., 9 days>"
    }}
  }}
]

Return atleast 6 episodes.
Episode must be ordered from the start of the timeline to end of the timeline.
Only return valid JSON, nothing else.

"""

summary_prompt = PromptTemplate(
    template=summary_template,
    input_variables=["chat_json"]
)

def summarize_chat(chat_data: dict) -> str:
    """Summarize chat data into structured episodes"""
    formatted = summary_prompt.format(chat_json=json.dumps(chat_data, indent=2))
    response = summarizer_llm.invoke(formatted)
    raw = response.content.strip()

    raw = raw = re.sub(r"^```json|```$", "", raw, flags=re.MULTILINE).strip()
    return json.loads(raw)
