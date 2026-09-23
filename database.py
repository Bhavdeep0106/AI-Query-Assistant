import sqlite3

from text_to_sql import generate_sql, validate_sql, execute_sql


DB_NAME = "database.db"


TEST_CASES = [
    {
        "question": "How many customers are there?",
        "expected_sql": "SELECT COUNT(*) FROM customers"
    },
    {
        "question": "How many products are there?",
        "expected_sql": "SELECT COUNT(*) FROM products"
    },
    {
        "question": "What is the average product price?",
        "expected_sql": "SELECT AVG(price) FROM products"
    },
    {
        "question": "What are the 5 most expensive products?",
        "expected_sql": """
            SELECT name, price
            FROM products
            ORDER BY price DESC
            LIMIT 5
        """
    },
    {
        "question": "Which country has the most customers?",
        "expected_sql": """
            SELECT country, COUNT(*) AS customer_count
            FROM customers
            GROUP BY country
            ORDER BY customer_count DESC
            LIMIT 1
        """
    },
    {
        "question": "How many completed orders are there?",
        "expected_sql": """
            SELECT COUNT(*)
            FROM orders
            WHERE status = 'completed'
        """
    },
    {
        "question": "What is the total quantity of products sold?",
        "expected_sql": """
            SELECT SUM(quantity)
            FROM order_items
        """
    },
    {
        "question": "Which products sold the most?",
        "expected_sql": """
            SELECT p.name, SUM(oi.quantity) AS total_quantity
            FROM products p
            JOIN order_items oi
                ON p.id = oi.product_id
            GROUP BY p.id, p.name
            ORDER BY total_quantity DESC
            LIMIT 1
        """
    },
    {
        "question": "How many orders does each customer have?",
        "expected_sql": """
            SELECT c.name, COUNT(o.id) AS order_count
            FROM customers c
            LEFT JOIN orders o
                ON c.id = o.customer_id
            GROUP BY c.id, c.name
            ORDER BY order_count DESC
        """
    },
    {
        "question": "Which products have never been ordered?",
        "expected_sql": """
            SELECT p.name
            FROM products p
            LEFT JOIN order_items oi
                ON p.id = oi.product_id
            WHERE oi.product_id IS NULL
        """
    }
]


def run_query(sql):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(sql)

    rows = cursor.fetchall()

    conn.close()

    return rows


def normalize_result(rows):
    return sorted(
        [tuple(row) for row in rows],
        key=lambda row: str(row)
    )


def evaluate():

    passed = 0
    failed = 0

    print("\nRunning result accuracy evaluation...\n")

    for i, test in enumerate(TEST_CASES, 1):

        question = test["question"]

        print(f"{i}. {question}")

        try:

            # Generate SQL using the AI
            generated_sql = generate_sql(question)

            # Validate generated SQL
            is_valid, message = validate_sql(generated_sql)

            if not is_valid:
                print("❌ FAIL - Invalid SQL")
                print(message)
                failed += 1
                continue

            # Execute generated SQL
            generated_result = execute_sql(generated_sql)[1]

            # Execute expected SQL
            expected_result = run_query(test["expected_sql"])

            # Compare results
            if normalize_result(generated_result) == normalize_result(expected_result):

                print("✅ PASS")
                passed += 1

            else:

                print("❌ FAIL")
                print("Generated SQL:")
                print(generated_sql)

                print("\nExpected result:")
                print(expected_result)

                print("\nGenerated result:")
                print(generated_result)

                failed += 1

        except Exception as e:

            print("❌ ERROR")
            print(e)

            failed += 1

        print()

    total = passed + failed
    accuracy = (passed / total) * 100 if total else 0

    print("=" * 45)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {failed}/{total}")
    print(f"Result Accuracy: {accuracy:.1f}%")
    print("=" * 45)


if __name__ == "__main__":
    evaluate()