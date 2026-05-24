-- Enterprise Banking AI Transformation Platform
-- PostgreSQL schema for local development with Postgres.app

DROP TABLE IF EXISTS ai_interactions CASCADE;
DROP TABLE IF EXISTS fraud_cases CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS support_tickets CASCADE;
DROP TABLE IF EXISTS sla_rules CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS customer_onboarding CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    email VARCHAR(160) UNIQUE NOT NULL,
    phone VARCHAR(40),
    city VARCHAR(80),
    state VARCHAR(40),
    customer_segment VARCHAR(40) NOT NULL,
    risk_rating VARCHAR(20) NOT NULL,
    account_type VARCHAR(40) NOT NULL,
    acquisition_channel VARCHAR(60) NOT NULL,
    created_at DATE NOT NULL
);

CREATE TABLE customer_onboarding (
    onboarding_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    application_date DATE NOT NULL,
    completion_date DATE,
    status VARCHAR(40) NOT NULL,
    kyc_status VARCHAR(40) NOT NULL,
    documents_submitted INTEGER NOT NULL,
    documents_required INTEGER NOT NULL,
    digital_completion BOOLEAN NOT NULL,
    manual_review_required BOOLEAN NOT NULL,
    onboarding_stage VARCHAR(80) NOT NULL
);

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY,
    department_name VARCHAR(80) UNIQUE NOT NULL,
    business_unit VARCHAR(80) NOT NULL
);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    role_title VARCHAR(100) NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(department_id),
    location VARCHAR(80) NOT NULL,
    is_ai_champion BOOLEAN NOT NULL
);

CREATE TABLE sla_rules (
    sla_rule_id INTEGER PRIMARY KEY,
    ticket_priority VARCHAR(20) NOT NULL,
    ticket_category VARCHAR(60) NOT NULL,
    response_time_hours INTEGER NOT NULL,
    resolution_time_hours INTEGER NOT NULL
);

CREATE TABLE support_tickets (
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    assigned_employee_id INTEGER REFERENCES employees(employee_id),
    created_at TIMESTAMP NOT NULL,
    first_response_at TIMESTAMP,
    resolved_at TIMESTAMP,
    ticket_category VARCHAR(60) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    channel VARCHAR(40) NOT NULL,
    status VARCHAR(40) NOT NULL,
    customer_sentiment VARCHAR(20) NOT NULL,
    ai_triaged BOOLEAN NOT NULL,
    ai_suggested_resolution BOOLEAN NOT NULL,
    sla_breached BOOLEAN NOT NULL,
    resolution_hours NUMERIC(10, 2)
);

CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(40) NOT NULL,
    channel VARCHAR(40) NOT NULL,
    merchant_category VARCHAR(80) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    transaction_status VARCHAR(30) NOT NULL,
    fraud_score NUMERIC(5, 2) NOT NULL,
    is_flagged BOOLEAN NOT NULL
);

CREATE TABLE fraud_cases (
    fraud_case_id INTEGER PRIMARY KEY,
    transaction_id INTEGER NOT NULL REFERENCES transactions(transaction_id),
    opened_at TIMESTAMP NOT NULL,
    closed_at TIMESTAMP,
    case_status VARCHAR(40) NOT NULL,
    fraud_type VARCHAR(80) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    investigator_employee_id INTEGER REFERENCES employees(employee_id),
    ai_risk_summary TEXT,
    confirmed_fraud BOOLEAN NOT NULL,
    loss_amount NUMERIC(12, 2) NOT NULL,
    recovery_amount NUMERIC(12, 2) NOT NULL
);

CREATE TABLE ai_interactions (
    ai_interaction_id INTEGER PRIMARY KEY,
    related_ticket_id INTEGER REFERENCES support_tickets(ticket_id),
    related_fraud_case_id INTEGER REFERENCES fraud_cases(fraud_case_id),
    employee_id INTEGER REFERENCES employees(employee_id),
    interaction_at TIMESTAMP NOT NULL,
    workflow_area VARCHAR(60) NOT NULL,
    prompt_type VARCHAR(80) NOT NULL,
    model_name VARCHAR(80) NOT NULL,
    user_prompt TEXT NOT NULL,
    ai_response_summary TEXT NOT NULL,
    human_accepted BOOLEAN NOT NULL,
    estimated_minutes_saved NUMERIC(8, 2) NOT NULL
);

CREATE INDEX idx_customers_segment ON customers(customer_segment);
CREATE INDEX idx_onboarding_customer ON customer_onboarding(customer_id);
CREATE INDEX idx_tickets_created_at ON support_tickets(created_at);
CREATE INDEX idx_tickets_sla ON support_tickets(sla_breached);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_flagged ON transactions(is_flagged);
CREATE INDEX idx_fraud_cases_status ON fraud_cases(case_status);
CREATE INDEX idx_ai_workflow_area ON ai_interactions(workflow_area);
