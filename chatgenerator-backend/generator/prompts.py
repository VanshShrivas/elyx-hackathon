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
between the Elyx Concierge Team and the member ({member_name}, Singapore).

{condition_text}

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
    input_variables=["month_index", "theme", "week", "context", "member_name", "condition_text"],
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

context = "Onboarding week, first exercise plan shared."

def generate_week(month_index: int, month: str, theme: str, week: int, context: str, member_name: str, condition: str):
  """Generates a week of chat based on context"""
  condition_text = f"{member_name} has the following condition(s): {condition}" if condition != "none" else ""
  formatted_prompt = prompt.format(
      month_index=month_index,
      month=month,
      theme=theme,
      week=week,
      member_name=member_name,
      condition_text=condition_text,
      context=context
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
                   initial_context: str, previous_month_data: Optional[List[ChatWeek]] = None) -> List[ChatWeek]:
    """Generates 4 weeks of chats for a month. If not the first month, includes summary of last month in context."""

    # ---- Prepare context ----
    if previous_month_data is None:   # first month
        context = initial_context
    else:
        context = summarize_month(previous_month_data) + "\nStarting new month..."

    # ---- Generate 4 weeks ----
    month_weeks = []
    for week in range(1, 5):
        week_data = generate_week(month_index, month, theme, week, context, member_name, condition)
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

