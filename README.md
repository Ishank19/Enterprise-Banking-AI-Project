# Enterprise Banking AI Transformation Platform

Consulting-style fintech transformation MVP for a retail bank modernizing customer onboarding, support tickets, fraud operations, SLA monitoring, AI-assisted workflows, and executive KPI reporting.

## What This Project Includes

- PostgreSQL schema for banking operations data.
- Synthetic banking data generation with Python and pandas.
- Around 1,000 customers, 2,500 support tickets, 5,000 transactions, 300 fraud cases, and AI interaction examples.
- Streamlit dashboard with KPI cards and Plotly charts.
- Optional OpenAI-powered executive KPI summary.
- Power BI-ready CSV exports in the `data/` folder.

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

## Local Setup on macOS with Postgres.app

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

## Files

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
