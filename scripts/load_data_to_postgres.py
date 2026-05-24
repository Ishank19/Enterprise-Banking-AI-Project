"""
Load generated CSV files into PostgreSQL.

Expected workflow:
1. Create a local database in Postgres.app.
2. Run sql/01_create_schema.sql in that database.
3. Generate CSV files with scripts/generate_synthetic_data.py.
4. Run this script to load the CSV files.
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

TABLE_LOAD_ORDER = [
    "customers",
    "customer_onboarding",
    "departments",
    "employees",
    "sla_rules",
    "support_tickets",
    "transactions",
    "fraud_cases",
    "ai_interactions",
]


def get_database_url():
    """Build a database URL from environment variables."""
    load_dotenv(PROJECT_ROOT / ".env")

    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "enterprise_banking_ai")
    db_user = os.getenv("DB_USER", os.getenv("USER", "postgres"))
    db_password = os.getenv("DB_PASSWORD", "")

    if db_password:
        return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    return f"postgresql+psycopg2://{db_user}@{db_host}:{db_port}/{db_name}"


def load_table(engine, table_name):
    """Read one CSV file and replace matching rows in PostgreSQL."""
    csv_path = DATA_DIR / f"{table_name}.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"Missing file: {csv_path}")

    dataframe = pd.read_csv(csv_path)
    dataframe.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Loaded {len(dataframe):,} rows into {table_name}")


def clear_tables(engine):
    """Remove existing data while respecting foreign key relationships."""
    reverse_order = list(reversed(TABLE_LOAD_ORDER))
    with engine.begin() as connection:
        for table_name in reverse_order:
            connection.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;"))


def main():
    engine = create_engine(get_database_url())

    clear_tables(engine)

    for table_name in TABLE_LOAD_ORDER:
        load_table(engine, table_name)

    print("PostgreSQL load complete.")


if __name__ == "__main__":
    main()
