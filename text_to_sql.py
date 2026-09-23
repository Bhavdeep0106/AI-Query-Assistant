import os
import sqlite3

from dotenv import load_dotenv
from groq import Groq
import sqlglot


load_dotenv(".env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

DB_NAME = "database.db"


SCHEMA = """
Database: e-commerce

Table: customers
- id INTEGER PRIMARY KEY
- name TEXT
- email TEXT
- country TEXT

Table: products
- id INTEGER PRIMARY KEY
- name TEXT
- category TEXT
- price REAL

Table: orders
- id INTEGER PRIMARY KEY
- customer_id INTEGER
- order_date DATE
- status TEXT

Table: order_items
- id INTEGER PRIMARY KEY
- order_id INTEGER
- product_id INTEGER
- quantity INTEGER

Relationships:
- orders.customer_id → customers.id
- order_items.order_id → orders.id
- order_items.product_id → products.id
"""


def generate_sql(question):

    prompt = f"""
You are a SQL expert.

Convert the user's question into a SQLite SQL query.

Use ONLY the tables and columns provided in the schema.

Return ONLY the SQL query.

Do not use markdown.

Do not explain the query.

SCHEMA:

{SCHEMA}

USER QUESTION:

{question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You generate valid SQLite SELECT queries only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content.strip()

def fix_sql(question, sql, error):

    prompt = f"""
You are a SQL debugging expert.

The following SQLite query produced an error.

USER QUESTION:
{question}

SQL QUERY:
{sql}

DATABASE SCHEMA:
{SCHEMA}

SQL ERROR:
{error}

Fix the SQL query.

Rules:
- Use only the tables and columns in the schema.
- Return ONLY the corrected SQLite SELECT query.
- Do not use markdown.
- Do not explain anything.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You fix SQLite SELECT queries."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content.strip()

def validate_sql(sql):

    try:
        # Check that the SQL can be parsed
        parsed = sqlglot.parse_one(sql, dialect="sqlite")

        # Only allow SELECT queries
        if parsed.key.upper() != "SELECT":
            return False, "Only SELECT queries are allowed."

        # Block dangerous keywords
        forbidden = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "ALTER",
            "TRUNCATE"
        ]

        sql_upper = sql.upper()

        for keyword in forbidden:
            if keyword in sql_upper:
                return False, f"Forbidden SQL operation: {keyword}"

        return True, "SQL is valid."

    except Exception as e:
        return False, f"Invalid SQL: {e}"


def execute_sql(sql):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    column_names = [
        description[0]
        for description in cursor.description
    ]

    conn.close()

    return column_names, results


if __name__ == "__main__":

    question = input("Ask a question: ")

    print("\nGenerating SQL...")

    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    print("\nValidating SQL...")

    is_valid, message = validate_sql(sql)

    print(message)

    if not is_valid:
        print("\nQuery was not executed.")
        exit()

    print("\nExecuting SQL...")

    columns, results = execute_sql(sql)

    print("\nResults:")
    print(columns)

    for row in results:
        print(row)