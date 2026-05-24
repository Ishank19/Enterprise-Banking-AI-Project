"""
Streamlit dashboard for the Enterprise Banking AI Transformation Platform.

The app reads CSV files from data/ by default. This keeps the portfolio demo easy
to run. PostgreSQL loading is supported separately through scripts/load_data_to_postgres.py.
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from ai_assistant import generate_executive_summary


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


st.set_page_config(
    page_title="Enterprise Banking AI Transformation Platform",
    page_icon="EB",
    layout="wide",
)


@st.cache_data
def load_csv(file_name):
    """Load a CSV file from the data folder."""
    path = DATA_DIR / file_name
    return pd.read_csv(path)


def format_number(value):
    """Format numbers for KPI cards."""
    if pd.isna(value):
        return "0"
    return f"{value:,.0f}"


def kpi_card(label, value, help_text=None):
    """Render a simple KPI card using Streamlit metrics."""
    st.metric(label=label, value=value, help=help_text)


def load_data():
    """Load all dashboard datasets."""
    return {
        "customers": load_csv("customers.csv"),
        "onboarding": load_csv("customer_onboarding.csv"),
        "tickets": load_csv("support_tickets.csv"),
        "transactions": load_csv("transactions.csv"),
        "fraud_cases": load_csv("fraud_cases.csv"),
        "ai_interactions": load_csv("ai_interactions.csv"),
    }


def show_missing_data_message(error):
    st.error("CSV data files are missing. Run scripts/generate_synthetic_data.py first.")
    st.caption(str(error))


def main():
    st.title("Enterprise Banking AI Transformation Platform")
    st.caption("Consulting-style MVP for banking operations modernization, AI workflows, and executive KPI reporting.")

    try:
        data = load_data()
    except FileNotFoundError as error:
        show_missing_data_message(error)
        return

    customers = data["customers"]
    onboarding = data["onboarding"]
    tickets = data["tickets"]
    transactions = data["transactions"]
    fraud_cases = data["fraud_cases"]
    ai_interactions = data["ai_interactions"]

    tickets["created_at"] = pd.to_datetime(tickets["created_at"])
    transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])
    ai_interactions["interaction_at"] = pd.to_datetime(ai_interactions["interaction_at"])

    total_customers = len(customers)
    completed_onboarding = (onboarding["status"] == "Completed").sum()
    total_tickets = len(tickets)
    sla_breach_rate = tickets["sla_breached"].mean() * 100
    confirmed_fraud = fraud_cases["confirmed_fraud"].sum()
    minutes_saved = ai_interactions["estimated_minutes_saved"].sum()

    st.subheader("Executive KPI Snapshot")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        kpi_card("Customers", format_number(total_customers))
    with col2:
        kpi_card("Completed Onboarding", format_number(completed_onboarding))
    with col3:
        kpi_card("Support Tickets", format_number(total_tickets))
    with col4:
        kpi_card("SLA Breach Rate", f"{sla_breach_rate:.1f}%")
    with col5:
        kpi_card("Confirmed Fraud", format_number(confirmed_fraud))
    with col6:
        kpi_card("AI Minutes Saved", format_number(minutes_saved))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Onboarding", "Support", "SLA Monitoring", "Fraud Operations", "AI Automation"]
    )

    with tab1:
        left, right = st.columns(2)

        onboarding_status = onboarding["status"].value_counts().reset_index()
        onboarding_status.columns = ["status", "applications"]
        fig_status = px.bar(
            onboarding_status,
            x="status",
            y="applications",
            color="status",
            title="Onboarding Status",
        )
        left.plotly_chart(fig_status, use_container_width=True)

        onboarding_stage = onboarding["onboarding_stage"].value_counts().reset_index()
        onboarding_stage.columns = ["stage", "applications"]
        fig_stage = px.funnel(
            onboarding_stage,
            x="applications",
            y="stage",
            title="Digital Onboarding Funnel",
        )
        right.plotly_chart(fig_stage, use_container_width=True)

    with tab2:
        left, right = st.columns(2)

        category_volume = tickets["ticket_category"].value_counts().reset_index()
        category_volume.columns = ["category", "tickets"]
        fig_category = px.bar(
            category_volume,
            x="tickets",
            y="category",
            orientation="h",
            title="Ticket Volume by Category",
        )
        left.plotly_chart(fig_category, use_container_width=True)

        channel_mix = tickets["channel"].value_counts().reset_index()
        channel_mix.columns = ["channel", "tickets"]
        fig_channel = px.pie(
            channel_mix,
            names="channel",
            values="tickets",
            title="Support Channel Mix",
        )
        right.plotly_chart(fig_channel, use_container_width=True)

    with tab3:
        left, right = st.columns(2)

        sla_by_priority = tickets.groupby("priority", as_index=False)["sla_breached"].mean()
        sla_by_priority["breach_rate_pct"] = sla_by_priority["sla_breached"] * 100
        fig_priority = px.bar(
            sla_by_priority,
            x="priority",
            y="breach_rate_pct",
            title="SLA Breach Rate by Priority",
            labels={"breach_rate_pct": "Breach Rate (%)"},
        )
        left.plotly_chart(fig_priority, use_container_width=True)

        daily_tickets = tickets.set_index("created_at").resample("W").agg(
            tickets=("ticket_id", "count"),
            breaches=("sla_breached", "sum"),
        ).reset_index()
        fig_daily = px.line(
            daily_tickets,
            x="created_at",
            y=["tickets", "breaches"],
            title="Weekly Ticket and SLA Breach Trend",
        )
        right.plotly_chart(fig_daily, use_container_width=True)

    with tab4:
        left, right = st.columns(2)

        fraud_by_type = fraud_cases["fraud_type"].value_counts().reset_index()
        fraud_by_type.columns = ["fraud_type", "cases"]
        fig_fraud_type = px.bar(
            fraud_by_type,
            x="cases",
            y="fraud_type",
            orientation="h",
            title="Fraud Cases by Type",
        )
        left.plotly_chart(fig_fraud_type, use_container_width=True)

        fraud_loss = fraud_cases.groupby("severity", as_index=False)[["loss_amount", "recovery_amount"]].sum()
        fig_loss = px.bar(
            fraud_loss,
            x="severity",
            y=["loss_amount", "recovery_amount"],
            barmode="group",
            title="Loss and Recovery by Severity",
        )
        right.plotly_chart(fig_loss, use_container_width=True)

    with tab5:
        left, right = st.columns(2)

        ai_by_area = ai_interactions.groupby("workflow_area", as_index=False).agg(
            interactions=("ai_interaction_id", "count"),
            minutes_saved=("estimated_minutes_saved", "sum"),
            acceptance_rate=("human_accepted", "mean"),
        )
        ai_by_area["acceptance_rate_pct"] = ai_by_area["acceptance_rate"] * 100

        fig_ai_minutes = px.bar(
            ai_by_area,
            x="minutes_saved",
            y="workflow_area",
            orientation="h",
            title="Estimated AI Time Savings by Workflow",
        )
        left.plotly_chart(fig_ai_minutes, use_container_width=True)

        fig_ai_acceptance = px.bar(
            ai_by_area,
            x="workflow_area",
            y="acceptance_rate_pct",
            title="Human Acceptance Rate by AI Workflow",
            labels={"acceptance_rate_pct": "Acceptance Rate (%)"},
        )
        right.plotly_chart(fig_ai_acceptance, use_container_width=True)

        kpi_summary = {
            "customers": int(total_customers),
            "completed_onboarding": int(completed_onboarding),
            "support_tickets": int(total_tickets),
            "sla_breach_rate_pct": round(float(sla_breach_rate), 1),
            "confirmed_fraud_cases": int(confirmed_fraud),
            "ai_minutes_saved": round(float(minutes_saved), 1),
        }

        if st.button("Generate AI Executive Summary"):
            with st.spinner("Generating summary..."):
                st.write(generate_executive_summary(kpi_summary))

    st.subheader("Power BI-Ready CSV Exports")
    st.write("Generated CSV files in the data folder can be imported directly into Power BI.")
    st.dataframe(customers.head(10), use_container_width=True)


if __name__ == "__main__":
    main()
