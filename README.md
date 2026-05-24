# Enterprise Banking AI Transformation Platform

Consulting-style fintech transformation MVP that simulates how a retail bank can modernize digital onboarding, customer support operations, fraud investigation, SLA monitoring, AI-assisted employee workflows, and executive KPI reporting.

This project is designed as a recruiter-friendly portfolio case study: it combines banking domain modeling, SQL analytics, Python data engineering, an interactive Streamlit dashboard, optional OpenAI-powered executive summaries, and Power BI-ready CSV exports.

## Project Overview

Retail banks often run critical customer operations across fragmented systems: onboarding teams track KYC progress, support teams manage ticket queues, fraud investigators review suspicious activity, and executives need a consolidated view of operational risk and service performance.

The Enterprise Banking AI Transformation Platform models a modern operating layer for these workflows. It uses synthetic banking data to demonstrate how a transformation team could create a centralized analytics foundation, monitor core KPIs, and introduce AI copilots into high-volume operational processes.

The MVP includes:

- PostgreSQL schema for banking operations data.
- Synthetic banking data generation with Python and pandas.
- Around 1,000 customers, 2,500 support tickets, 5,000 transactions, 300 fraud cases, and AI interaction examples.
- Streamlit dashboard with KPI cards and Plotly charts.
- Optional OpenAI-powered executive KPI summary.
- Power BI-ready CSV exports in the `data/` folder.

## Business Problem

A retail bank wants to improve customer experience, operational visibility, and risk management while introducing AI responsibly into employee workflows.

Key challenges simulated in this project:

- Digital onboarding lacks clear funnel visibility across application, KYC, manual review, and completion stages.
- Support teams need better monitoring of ticket volume, channel mix, priority, resolution time, and SLA breaches.
- Fraud operations require faster case prioritization, loss tracking, and recovery reporting.
- Leadership needs a concise executive KPI view across customer operations, service performance, fraud risk, and AI adoption.
- AI-assisted workflows need measurable value, including acceptance rates and estimated time saved.

## Solution Architecture

The project follows a practical analytics and AI workflow architecture:

```text
Synthetic Banking Data
        |
        v
Python + pandas data generation
        |
        +--------------------+
        |                    |
        v                    v
Power BI-ready CSVs     PostgreSQL schema
in data/                and SQL KPI queries
        |                    |
        +----------+---------+
                   |
                   v
          Streamlit + Plotly dashboard
                   |
                   v
      Optional OpenAI executive KPI narrative
```

Core design choices:

- `data/` stores generated CSV exports that can be used directly in Streamlit or imported into Power BI.
- `sql/01_create_schema.sql` defines the relational banking operations model.
- `sql/02_kpi_queries.sql` provides validation queries for onboarding, support, SLA, fraud, and AI workflow metrics.
- `scripts/generate_synthetic_data.py` creates repeatable synthetic portfolio data.
- `scripts/load_data_to_postgres.py` loads generated CSVs into PostgreSQL for SQL analysis.
- `app/streamlit_app.py` provides the interactive dashboard experience.
- `app/ai_assistant.py` adds optional OpenAI-generated executive summaries.

## Features

- Executive KPI snapshot covering customers, onboarding completion, support tickets, SLA breach rate, confirmed fraud, and AI time savings.
- Digital onboarding funnel analysis by status and onboarding stage.
- Customer support analytics by ticket category and service channel.
- SLA monitoring by priority, breach rate, and weekly ticket trend.
- Fraud operations reporting by fraud type, severity, loss amount, and recovery amount.
- AI automation analytics by workflow area, estimated minutes saved, and human acceptance rate.
- Optional AI-generated executive briefing with operational insights, recommended actions, and risks to monitor.
- PostgreSQL schema and SQL queries for backend analytics validation.
- CSV exports structured for Power BI ingestion.

## Tech Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Database | PostgreSQL | Relational data model for banking operations, fraud cases, support tickets, and AI interactions. |
| Querying | SQL | KPI validation, operational analytics, and reporting logic. |
| Data generation | Python, pandas, NumPy, Faker | Synthetic banking data creation for repeatable portfolio demos. |
| App framework | Streamlit | Interactive dashboard and executive reporting interface. |
| Visualization | Plotly | Bar charts, funnel charts, pie charts, and time-series views. |
| AI workflow | OpenAI API | Optional executive KPI narrative generation. |
| Configuration | python-dotenv | Local environment variable management. |
| BI export | CSV | Power BI-ready files for dashboard modeling and reporting. |

## KPIs Tracked

| KPI Area | Example Metrics |
| --- | --- |
| Customer base | Total customers, customer segment mix, risk rating distribution. |
| Onboarding | Completed applications, onboarding stage volume, KYC status, average completion time. |
| Support operations | Ticket volume, category mix, channel mix, average resolution hours. |
| SLA performance | SLA breach rate, breaches by priority, weekly ticket and breach trends. |
| Fraud operations | Confirmed fraud cases, fraud type distribution, loss amount, recovery amount, recovery rate. |
| AI adoption | AI interactions by workflow, human acceptance rate, estimated minutes saved. |
| Executive reporting | Consolidated KPI snapshot and AI-generated leadership summary. |

## AI Workflow

The AI layer is intentionally scoped as an assistant workflow rather than an autonomous decision-maker. The dashboard can send aggregated KPI values to the OpenAI API and return a concise executive briefing.

The AI summary is designed to produce:

- 3 operational insights.
- 2 recommended next actions.
- 1 risk to monitor.

Modeled AI use cases include:

- Support ticket triage and suggested resolution workflows.
- Fraud case risk summarization.
- Executive KPI narrative generation.
- Time-savings tracking through estimated minutes saved.
- Human-in-the-loop validation through acceptance-rate metrics.

The core dashboard works without an API key. OpenAI configuration is optional and only required for the executive summary button.

## Dashboard Preview

Screenshots are intentionally left as placeholders until final dashboard images are captured.

| View | Placeholder |
| --- | --- |
| Executive KPI Snapshot | Add screenshot: `docs/screenshots/executive-kpi-snapshot.png` |
| Digital Onboarding Funnel | Add screenshot: `docs/screenshots/onboarding-funnel.png` |
| Support and SLA Monitoring | Add screenshot: `docs/screenshots/support-sla-monitoring.png` |
| Fraud Operations | Add screenshot: `docs/screenshots/fraud-operations.png` |
| AI Automation Analytics | Add screenshot: `docs/screenshots/ai-automation-analytics.png` |

## Folder Structure

```text
sql/
scripts/
data/
app/
docs/
dashboards/
presentation/
```

## How to Run Locally

### 1. Install Requirements

Install Python 3.10 or newer and Postgres.app.

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` for your local Postgres.app setup. A typical Postgres.app configuration uses your macOS username and no password.

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=enterprise_banking_ai
DB_USER=your_mac_username
DB_PASSWORD=
```

Do not commit `.env`.

### 3. Create the Database

Open Postgres.app and create a database named:

```text
enterprise_banking_ai
```

Then run the schema script in your preferred SQL client:

```text
sql/01_create_schema.sql
```

### 4. Generate Synthetic Data

```bash
python scripts/generate_synthetic_data.py
```

This creates CSV files in the `data/` folder. These files can be imported into Power BI.

### 5. Load Data into PostgreSQL

```bash
python scripts/load_data_to_postgres.py
```

### 6. Run the Streamlit Dashboard

```bash
streamlit run app/streamlit_app.py
```

The dashboard reads from CSV files by default, so it can run even before PostgreSQL loading.

## Optional OpenAI Setup

To enable the AI executive summary button, add these values to `.env`:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

The app does not require an API key for the core dashboard.

## Power BI Usage

After generating data, import CSV files from the `data/` folder into Power BI:

- `customers.csv`
- `customer_onboarding.csv`
- `departments.csv`
- `employees.csv`
- `sla_rules.csv`
- `support_tickets.csv`
- `transactions.csv`
- `fraud_cases.csv`
- `ai_interactions.csv`

Use the relationships described in `sql/01_create_schema.sql` to build the model.

## Key Files

| File | Purpose |
| --- | --- |
| `sql/01_create_schema.sql` | Creates PostgreSQL tables, keys, and indexes. |
| `sql/02_kpi_queries.sql` | Example KPI queries for analytics validation. |
| `scripts/generate_synthetic_data.py` | Generates realistic synthetic banking CSV data. |
| `scripts/load_data_to_postgres.py` | Loads generated CSV files into PostgreSQL. |
| `app/streamlit_app.py` | Interactive Streamlit dashboard. |
| `app/ai_assistant.py` | Optional OpenAI executive summary helper. |
| `docs/data_dictionary.md` | Business definitions for tables and fields. |
| `docs/project_summary.md` | Consulting-style project overview. |
| `requirements.txt` | Python package dependencies. |
| `.env.example` | Safe example environment configuration. |
| `.gitignore` | Excludes local, generated, and secret files. |

## Business Impact

This project demonstrates how a bank could move from fragmented operational reporting to a more integrated digital transformation model.

Potential impact areas:

- Faster executive visibility into onboarding, service performance, fraud risk, and AI adoption.
- Better prioritization of support operations through SLA breach and category-level analysis.
- Improved fraud investigation reporting through severity, loss, recovery, and case-status metrics.
- More transparent AI adoption measurement through human acceptance and estimated productivity gains.
- Faster BI enablement through clean CSV exports and a relational data model ready for analytics.

## Resume-Ready Project Summary

Built an Enterprise Banking AI Transformation Platform simulating a retail bank modernization program across digital onboarding, customer support, fraud operations, SLA monitoring, AI-assisted workflows, and executive KPI reporting. Designed a PostgreSQL data model, generated synthetic banking datasets with Python and pandas, developed SQL KPI queries, built an interactive Streamlit and Plotly dashboard, added optional OpenAI-powered executive summaries, and produced Power BI-ready CSV exports for business intelligence reporting.
