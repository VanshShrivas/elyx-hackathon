import json
from typing import List, Optional
from .prompts import generate_month, summarize_month, calendar_months, theme_list, get_month_year



def generate_full_journey(member_name: str, condition: str, test_reports: List[dict], start_year: int = 2023, start_month: int = 8, months: int = 8):
    all_data = {"months": []}
    previous_month_data = None

    for i in range(months):
        year, month_num = get_month_year(start_year, start_month, i)
        month = calendar_months[month_num - 1]
        theme = theme_list[i]

        if i == 0:
            context = "Onboarding week, first exercise plan shared."
        else:
            context = summarize_month(previous_month_data)
        month_index = i + 1
        month_data = generate_month(month_index, month, theme, member_name, condition,
                                    initial_context=context, test_reports=test_reports, previous_month_data=previous_month_data)

        all_data["months"].append({
            "month_index": month_index,
            "month": month,
            "theme": theme,
            "weeks": [week.model_dump() for week in month_data]
        })

        previous_month_data = month_data

    # Save to JSON
    with open("chat_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    return all_data


# Run the full generation
# Define the test reports (moved from the prompt template)

# journey_data = generate_full_journey("Rohan Patel", "High BP", test_reports, start_year = 2024, start_month = 8, months=8)
# print("8-month chat data generated and saved to chat_data.json")

