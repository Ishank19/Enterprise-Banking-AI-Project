# Architecture

```mermaid
flowchart LR
    A["Synthetic data generation<br/>Python + Faker"] --> B["CSV exports<br/>data/ folder"]
    B --> C[("PostgreSQL database")]

    C --> C1["customers"]
    C --> C2["onboarding"]
    C --> C3["tickets"]
    C --> C4["transactions"]
    C --> C5["fraud cases"]
    C --> C6["employees"]
    C --> C7["SLA rules"]
    C --> C8["AI interactions"]

    C --> D["SQL KPI queries<br/>Operational analytics"]
    D --> E["Streamlit + Plotly dashboard<br/>Interactive monitoring"]
    D --> F["Power BI-ready CSV exports<br/>Executive reporting"]

    C8 --> G["Optional OpenAI API assistant<br/>Executive summaries + AI workflow insights"]
    D --> G
    G --> E
```

## Explanation

**Data layer:** Synthetic banking operations data is generated with Python and Faker, exported as CSV files in the `data/` folder, and loaded into PostgreSQL tables for customers, onboarding, tickets, transactions, fraud cases, employees, SLA rules, and AI interactions.

**Analytics layer:** SQL KPI queries run against PostgreSQL to produce operational metrics for service performance, onboarding, fraud operations, transaction monitoring, SLA compliance, and AI usage.

**AI layer:** The optional OpenAI API assistant uses operational data and AI interaction records to generate executive summaries and workflow insights.

**Visualization layer:** Streamlit and Plotly provide an interactive monitoring dashboard for operational users, while Power BI-ready CSV exports support executive reporting.

**Portfolio/business value:** The project demonstrates an end-to-end enterprise banking analytics platform that connects realistic data generation, relational modeling, KPI analytics, AI-assisted insight generation, and executive-ready reporting.
