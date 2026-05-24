"""
Generate realistic synthetic data for the Enterprise Banking AI Transformation Platform.

This script writes CSV files into the data/ folder. Those CSV files can be used by:
- Streamlit for a quick local demo
- PostgreSQL loader script
- Power BI imports
"""

from datetime import datetime, timedelta
from pathlib import Path
import random

import numpy as np
import pandas as pd
from faker import Faker


fake = Faker("en_US")
Faker.seed(42)
random.seed(42)
np.random.seed(42)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

CUSTOMER_COUNT = 1000
TICKET_COUNT = 2500
TRANSACTION_COUNT = 5000
FRAUD_CASE_COUNT = 300
AI_INTERACTION_COUNT = 900


def choose_weighted(options, weights):
    """Return one value from a weighted list."""
    return random.choices(options, weights=weights, k=1)[0]


def random_date(start_days_ago=365, end_days_ago=0):
    """Return a random datetime between two day offsets from today."""
    today = datetime.now()
    start = today - timedelta(days=start_days_ago)
    end = today - timedelta(days=end_days_ago)
    seconds_between = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, seconds_between))


def generate_departments():
    departments = [
        (1, "Retail Banking", "Consumer Bank"),
        (2, "Customer Support", "Operations"),
        (3, "Fraud Operations", "Risk"),
        (4, "Digital Onboarding", "Transformation"),
        (5, "Data and AI", "Technology"),
        (6, "Compliance", "Risk"),
        (7, "Executive Office", "Strategy"),
    ]
    return pd.DataFrame(departments, columns=["department_id", "department_name", "business_unit"])


def generate_employees(departments):
    roles_by_department = {
        "Retail Banking": ["Relationship Manager", "Branch Advisor", "Digital Banker"],
        "Customer Support": ["Support Specialist", "Senior Support Analyst", "Contact Center Lead"],
        "Fraud Operations": ["Fraud Investigator", "Fraud Analyst", "Fraud Operations Lead"],
        "Digital Onboarding": ["Onboarding Specialist", "KYC Analyst", "Process Manager"],
        "Data and AI": ["AI Product Analyst", "Data Engineer", "Analytics Manager"],
        "Compliance": ["Compliance Analyst", "Risk Officer", "KYC Quality Lead"],
        "Executive Office": ["Transformation Lead", "Portfolio Manager", "Executive Analyst"],
    }

    employees = []
    employee_id = 1

    for _, department in departments.iterrows():
        for _ in range(10):
            employees.append(
                {
                    "employee_id": employee_id,
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "role_title": random.choice(roles_by_department[department["department_name"]]),
                    "department_id": int(department["department_id"]),
                    "location": random.choice(["New York", "Charlotte", "Dallas", "Phoenix", "Chicago"]),
                    "is_ai_champion": random.random() < 0.25,
                }
            )
            employee_id += 1

    return pd.DataFrame(employees)


def generate_sla_rules():
    rules = []
    rule_id = 1
    categories = ["Account Access", "Payments", "Cards", "Loans", "Fraud Alert", "KYC", "Digital Banking"]
    priority_hours = {
        "Low": (24, 96),
        "Medium": (8, 48),
        "High": (4, 24),
        "Critical": (1, 8),
    }

    for category in categories:
        for priority, hours in priority_hours.items():
            rules.append(
                {
                    "sla_rule_id": rule_id,
                    "ticket_priority": priority,
                    "ticket_category": category,
                    "response_time_hours": hours[0],
                    "resolution_time_hours": hours[1],
                }
            )
            rule_id += 1

    return pd.DataFrame(rules)


def generate_customers():
    customers = []
    used_emails = set()

    for customer_id in range(1, CUSTOMER_COUNT + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name}.{last_name}.{customer_id}@examplebankdemo.com".lower()

        while email in used_emails:
            email = fake.unique.email()
        used_emails.add(email)

        customers.append(
            {
                "customer_id": customer_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": fake.phone_number(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "customer_segment": choose_weighted(
                    ["Retail", "Mass Affluent", "Small Business", "Private Banking"],
                    [0.58, 0.24, 0.14, 0.04],
                ),
                "risk_rating": choose_weighted(["Low", "Medium", "High"], [0.65, 0.28, 0.07]),
                "account_type": choose_weighted(
                    ["Checking", "Savings", "Credit Card", "Mortgage", "Business Checking"],
                    [0.42, 0.22, 0.18, 0.10, 0.08],
                ),
                "acquisition_channel": choose_weighted(
                    ["Mobile App", "Website", "Branch", "Referral", "Partner Marketplace"],
                    [0.38, 0.26, 0.18, 0.12, 0.06],
                ),
                "created_at": random_date(720, 10).date(),
            }
        )

    return pd.DataFrame(customers)


def generate_onboarding(customers):
    records = []
    stages = ["Application Started", "Documents Uploaded", "KYC Review", "Account Approved", "Activated"]

    for onboarding_id, customer in enumerate(customers.itertuples(index=False), start=1):
        application_date = customer.created_at
        status = choose_weighted(["Completed", "In Progress", "Rejected"], [0.78, 0.16, 0.06])
        documents_required = random.choice([2, 3, 4, 5])

        if status == "Completed":
            completion_date = application_date + timedelta(days=random.randint(1, 14))
            stage = "Activated"
            documents_submitted = documents_required
            kyc_status = choose_weighted(["Approved", "Manual Review"], [0.88, 0.12])
        elif status == "Rejected":
            completion_date = application_date + timedelta(days=random.randint(2, 20))
            stage = choose_weighted(["KYC Review", "Documents Uploaded"], [0.65, 0.35])
            documents_submitted = random.randint(1, documents_required)
            kyc_status = choose_weighted(["Rejected", "Manual Review"], [0.75, 0.25])
        else:
            completion_date = None
            stage = random.choice(stages[:-1])
            documents_submitted = random.randint(0, documents_required)
            kyc_status = choose_weighted(["Pending", "Manual Review"], [0.70, 0.30])

        records.append(
            {
                "onboarding_id": onboarding_id,
                "customer_id": customer.customer_id,
                "application_date": application_date,
                "completion_date": completion_date,
                "status": status,
                "kyc_status": kyc_status,
                "documents_submitted": documents_submitted,
                "documents_required": documents_required,
                "digital_completion": random.random() < 0.72,
                "manual_review_required": kyc_status in ["Manual Review", "Rejected"],
                "onboarding_stage": stage,
            }
        )

    return pd.DataFrame(records)


def generate_support_tickets(customers, employees):
    support_employee_ids = employees[employees["department_id"].isin([2, 4, 6])]["employee_id"].tolist()
    categories = ["Account Access", "Payments", "Cards", "Loans", "Fraud Alert", "KYC", "Digital Banking"]
    tickets = []

    for ticket_id in range(1, TICKET_COUNT + 1):
        created_at = random_date(270, 0)
        priority = choose_weighted(["Low", "Medium", "High", "Critical"], [0.36, 0.42, 0.17, 0.05])
        status = choose_weighted(["Resolved", "Open", "Pending Customer", "Escalated"], [0.72, 0.12, 0.10, 0.06])
        response_hours = {"Low": 20, "Medium": 7, "High": 3, "Critical": 1}[priority]
        target_resolution = {"Low": 96, "Medium": 48, "High": 24, "Critical": 8}[priority]
        actual_resolution = max(1, np.random.normal(target_resolution * 0.75, target_resolution * 0.45))
        sla_breached = actual_resolution > target_resolution or random.random() < 0.08

        if status == "Resolved":
            resolved_at = created_at + timedelta(hours=float(actual_resolution))
            resolution_hours = round(actual_resolution, 2)
        else:
            resolved_at = None
            resolution_hours = None

        tickets.append(
            {
                "ticket_id": ticket_id,
                "customer_id": int(customers.sample(1).iloc[0]["customer_id"]),
                "assigned_employee_id": random.choice(support_employee_ids),
                "created_at": created_at,
                "first_response_at": created_at + timedelta(hours=random.uniform(0.2, response_hours)),
                "resolved_at": resolved_at,
                "ticket_category": choose_weighted(categories, [0.20, 0.19, 0.17, 0.10, 0.12, 0.09, 0.13]),
                "priority": priority,
                "channel": choose_weighted(["Mobile App", "Web Chat", "Phone", "Email", "Branch"], [0.30, 0.24, 0.22, 0.18, 0.06]),
                "status": status,
                "customer_sentiment": choose_weighted(["Positive", "Neutral", "Negative"], [0.22, 0.52, 0.26]),
                "ai_triaged": random.random() < 0.68,
                "ai_suggested_resolution": random.random() < 0.54,
                "sla_breached": sla_breached,
                "resolution_hours": resolution_hours,
            }
        )

    return pd.DataFrame(tickets)


def generate_transactions(customers):
    transactions = []
    transaction_types = ["Debit Card", "ACH Transfer", "Wire Transfer", "ATM Withdrawal", "Bill Pay", "Deposit"]
    merchant_categories = ["Grocery", "Fuel", "Travel", "Electronics", "Healthcare", "Restaurant", "Utilities", "Online Retail"]

    for transaction_id in range(1, TRANSACTION_COUNT + 1):
        transaction_type = choose_weighted(transaction_types, [0.36, 0.20, 0.06, 0.12, 0.15, 0.11])
        amount = round(max(5, np.random.lognormal(mean=4.2, sigma=1.0)), 2)
        fraud_score = round(min(99.9, max(1.0, np.random.beta(1.2, 8.0) * 100)), 2)

        if transaction_type == "Wire Transfer" and amount > 5000:
            fraud_score = round(min(99.9, fraud_score + random.uniform(10, 25)), 2)

        transactions.append(
            {
                "transaction_id": transaction_id,
                "customer_id": int(customers.sample(1).iloc[0]["customer_id"]),
                "transaction_date": random_date(270, 0),
                "transaction_type": transaction_type,
                "channel": choose_weighted(["Mobile App", "Online Banking", "Branch", "ATM", "Card Network"], [0.34, 0.28, 0.08, 0.12, 0.18]),
                "merchant_category": random.choice(merchant_categories),
                "amount": amount,
                "currency": "USD",
                "transaction_status": choose_weighted(["Posted", "Pending", "Declined", "Reversed"], [0.86, 0.08, 0.04, 0.02]),
                "fraud_score": fraud_score,
                "is_flagged": fraud_score >= 72 or random.random() < 0.03,
            }
        )

    return pd.DataFrame(transactions)


def generate_fraud_cases(transactions, employees):
    fraud_employee_ids = employees[employees["department_id"].isin([3, 6])]["employee_id"].tolist()
    flagged_transactions = transactions[transactions["is_flagged"]].copy()

    if len(flagged_transactions) < FRAUD_CASE_COUNT:
        extra_needed = FRAUD_CASE_COUNT - len(flagged_transactions)
        extra_transactions = transactions.sample(extra_needed)
        flagged_transactions = pd.concat([flagged_transactions, extra_transactions])

    selected_transactions = flagged_transactions.sample(FRAUD_CASE_COUNT, replace=False)
    fraud_cases = []

    for fraud_case_id, transaction in enumerate(selected_transactions.itertuples(index=False), start=1):
        opened_at = transaction.transaction_date + timedelta(hours=random.randint(1, 48))
        case_status = choose_weighted(["Closed", "Investigating", "Escalated"], [0.66, 0.25, 0.09])
        confirmed_fraud = random.random() < 0.58
        loss_amount = round(transaction.amount if confirmed_fraud else transaction.amount * random.uniform(0, 0.20), 2)
        recovery_amount = round(loss_amount * random.uniform(0.05, 0.75), 2)

        fraud_cases.append(
            {
                "fraud_case_id": fraud_case_id,
                "transaction_id": int(transaction.transaction_id),
                "opened_at": opened_at,
                "closed_at": opened_at + timedelta(days=random.randint(1, 21)) if case_status == "Closed" else None,
                "case_status": case_status,
                "fraud_type": choose_weighted(
                    ["Account Takeover", "Card Not Present", "Synthetic Identity", "Authorized Push Payment", "Check Fraud"],
                    [0.24, 0.31, 0.13, 0.20, 0.12],
                ),
                "severity": choose_weighted(["Low", "Medium", "High", "Critical"], [0.22, 0.40, 0.28, 0.10]),
                "investigator_employee_id": random.choice(fraud_employee_ids),
                "ai_risk_summary": "AI summarized transaction behavior, customer history, device signals, and recommended next action.",
                "confirmed_fraud": confirmed_fraud,
                "loss_amount": loss_amount,
                "recovery_amount": recovery_amount,
            }
        )

    return pd.DataFrame(fraud_cases)


def generate_ai_interactions(tickets, fraud_cases, employees):
    employee_ids = employees["employee_id"].tolist()
    interactions = []

    workflow_options = [
        ("Support Ticket Triage", "Classify issue and recommend routing"),
        ("Agent Copilot", "Draft customer response"),
        ("Fraud Case Summary", "Summarize fraud evidence"),
        ("KPI Narrative", "Explain operational performance"),
        ("Onboarding Review", "Summarize missing KYC documents"),
    ]

    for ai_interaction_id in range(1, AI_INTERACTION_COUNT + 1):
        workflow_area, prompt_type = random.choice(workflow_options)
        related_ticket_id = None
        related_fraud_case_id = None

        if workflow_area in ["Support Ticket Triage", "Agent Copilot"]:
            related_ticket_id = int(tickets.sample(1).iloc[0]["ticket_id"])
        elif workflow_area == "Fraud Case Summary":
            related_fraud_case_id = int(fraud_cases.sample(1).iloc[0]["fraud_case_id"])

        interactions.append(
            {
                "ai_interaction_id": ai_interaction_id,
                "related_ticket_id": related_ticket_id,
                "related_fraud_case_id": related_fraud_case_id,
                "employee_id": random.choice(employee_ids),
                "interaction_at": random_date(180, 0),
                "workflow_area": workflow_area,
                "prompt_type": prompt_type,
                "model_name": "gpt-4o-mini",
                "user_prompt": f"Create a concise banking operations output for: {prompt_type}.",
                "ai_response_summary": "Generated a concise recommendation for the employee to review before customer or case action.",
                "human_accepted": random.random() < 0.78,
                "estimated_minutes_saved": round(random.uniform(3, 24), 2),
            }
        )

    return pd.DataFrame(interactions)


def save_csv(dataframe, file_name):
    output_path = DATA_DIR / file_name
    dataframe.to_csv(output_path, index=False)
    print(f"Saved {len(dataframe):,} rows to {output_path}")


def main():
    DATA_DIR.mkdir(exist_ok=True)

    departments = generate_departments()
    employees = generate_employees(departments)
    sla_rules = generate_sla_rules()
    customers = generate_customers()
    onboarding = generate_onboarding(customers)
    tickets = generate_support_tickets(customers, employees)
    transactions = generate_transactions(customers)
    fraud_cases = generate_fraud_cases(transactions, employees)
    ai_interactions = generate_ai_interactions(tickets, fraud_cases, employees)

    save_csv(customers, "customers.csv")
    save_csv(onboarding, "customer_onboarding.csv")
    save_csv(departments, "departments.csv")
    save_csv(employees, "employees.csv")
    save_csv(sla_rules, "sla_rules.csv")
    save_csv(tickets, "support_tickets.csv")
    save_csv(transactions, "transactions.csv")
    save_csv(fraud_cases, "fraud_cases.csv")
    save_csv(ai_interactions, "ai_interactions.csv")

    print("Synthetic banking data generation complete.")


if __name__ == "__main__":
    main()
