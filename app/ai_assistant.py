"""
Small OpenAI helper for the Streamlit dashboard.

The dashboard works without an OpenAI API key. When OPENAI_API_KEY is present,
this module can generate an executive-style KPI narrative.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI


def build_kpi_prompt(kpi_summary):
    """Create a short prompt using only aggregated KPI values."""
    return f"""
You are an AI transformation consultant helping a retail bank.

Write a concise executive briefing based on these KPIs:
{kpi_summary}

Include:
- 3 operational insights
- 2 recommended next actions
- 1 risk to monitor

Keep it clear, professional, and suitable for a portfolio demo.
"""


def generate_executive_summary(kpi_summary):
    """Return an AI-generated summary, or a friendly setup message."""
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        return (
            "OPENAI_API_KEY is not configured. Add it to a local .env file to enable "
            "AI-generated executive KPI summaries."
        )

    client = OpenAI()
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        input=build_kpi_prompt(kpi_summary),
        max_output_tokens=500,
    )

    return response.output_text
