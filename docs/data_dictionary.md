# Data Dictionary

This document describes the synthetic data model for the Enterprise Banking AI Transformation Platform.

## customers

Customer master data used across onboarding, support, transactions, and fraud workflows.

| Column | Description |
| --- | --- |
| customer_id | Unique customer identifier. |
| first_name | Synthetic customer first name. |
| last_name | Synthetic customer last name. |
| email | Demo email address. |
| phone | Synthetic phone number. |
| city | Customer city. |
| state | Customer state abbreviation. |
| customer_segment | Retail, Mass Affluent, Small Business, or Private Banking. |
| risk_rating | Low, Medium, or High customer risk rating. |
| account_type | Primary product or account type. |
| acquisition_channel | Channel where the customer was acquired. |
| created_at | Customer creation date. |

## customer_onboarding

Tracks digital onboarding applications and KYC progress.

| Column | Description |
| --- | --- |
| onboarding_id | Unique onboarding record identifier. |
| customer_id | Customer linked to the onboarding record. |
| application_date | Date application started. |
| completion_date | Date application completed or rejected. |
| status | Completed, In Progress, or Rejected. |
| kyc_status | KYC review outcome or current state. |
| documents_submitted | Number of documents received. |
| documents_required | Number of documents required. |
| digital_completion | Whether the journey was completed digitally. |
| manual_review_required | Whether employee review was needed. |
| onboarding_stage | Current or final funnel stage. |

## departments

Internal bank department reference table.

| Column | Description |
| --- | --- |
| department_id | Unique department identifier. |
| department_name | Department name. |
| business_unit | Higher-level business unit. |

## employees

Synthetic bank employees assigned to support, fraud, onboarding, and AI workflows.

| Column | Description |
| --- | --- |
| employee_id | Unique employee identifier. |
| first_name | Employee first name. |
| last_name | Employee last name. |
| role_title | Employee role. |
| department_id | Linked department. |
| location | Office or operations location. |
| is_ai_champion | Whether the employee is an AI adoption champion. |

## sla_rules

Target response and resolution times by ticket category and priority.

| Column | Description |
| --- | --- |
| sla_rule_id | Unique SLA rule identifier. |
| ticket_priority | Low, Medium, High, or Critical. |
| ticket_category | Support ticket category. |
| response_time_hours | Target first response time. |
| resolution_time_hours | Target resolution time. |

## support_tickets

Customer service ticket data with AI triage and SLA tracking.

| Column | Description |
| --- | --- |
| ticket_id | Unique ticket identifier. |
| customer_id | Customer who opened the ticket. |
| assigned_employee_id | Employee assigned to the ticket. |
| created_at | Ticket creation timestamp. |
| first_response_at | First response timestamp. |
| resolved_at | Resolution timestamp. |
| ticket_category | Issue category. |
| priority | Ticket urgency. |
| channel | Customer contact channel. |
| status | Ticket status. |
| customer_sentiment | Positive, Neutral, or Negative. |
| ai_triaged | Whether AI routed or classified the ticket. |
| ai_suggested_resolution | Whether AI drafted or suggested a resolution. |
| sla_breached | Whether the SLA target was missed. |
| resolution_hours | Time to resolution for resolved tickets. |

## transactions

Synthetic retail banking transactions used for fraud monitoring.

| Column | Description |
| --- | --- |
| transaction_id | Unique transaction identifier. |
| customer_id | Customer linked to the transaction. |
| transaction_date | Transaction timestamp. |
| transaction_type | Payment or account activity type. |
| channel | Channel where transaction occurred. |
| merchant_category | Merchant or transaction category. |
| amount | Transaction amount. |
| currency | Currency code. |
| transaction_status | Posted, Pending, Declined, or Reversed. |
| fraud_score | Synthetic AI risk score from 1 to 99.9. |
| is_flagged | Whether the transaction was flagged for review. |

## fraud_cases

Fraud operations cases linked to suspicious transactions.

| Column | Description |
| --- | --- |
| fraud_case_id | Unique fraud case identifier. |
| transaction_id | Transaction under review. |
| opened_at | Case open timestamp. |
| closed_at | Case closure timestamp. |
| case_status | Closed, Investigating, or Escalated. |
| fraud_type | Fraud typology. |
| severity | Low, Medium, High, or Critical. |
| investigator_employee_id | Assigned investigator. |
| ai_risk_summary | Example AI-generated case summary. |
| confirmed_fraud | Whether fraud was confirmed. |
| loss_amount | Estimated loss amount. |
| recovery_amount | Recovered amount. |

## ai_interactions

Examples of employee use of AI-assisted workflows.

| Column | Description |
| --- | --- |
| ai_interaction_id | Unique interaction identifier. |
| related_ticket_id | Optional related support ticket. |
| related_fraud_case_id | Optional related fraud case. |
| employee_id | Employee who used AI. |
| interaction_at | Interaction timestamp. |
| workflow_area | Business workflow supported by AI. |
| prompt_type | Type of prompt or task. |
| model_name | Model used for the interaction. |
| user_prompt | Example user prompt. |
| ai_response_summary | Summary of the AI response. |
| human_accepted | Whether the employee accepted the output. |
| estimated_minutes_saved | Estimated productivity benefit. |
