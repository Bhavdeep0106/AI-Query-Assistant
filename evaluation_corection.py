import sqlite3

from text_to_sql import (
    generate_sql,
    validate_sql,
    execute_sql,
    fix_sql
)


DB_NAME = "database.db"


TEST_CASES = [
    {
        "question": "How many customers are there?",
        "expected": 8
    },
    {
        "question": "How many products are there?",
        "expected": 10
    },
    {
        "question": "Which country has the most customers?",
        "expected": "India"
    },
    {
        "question": "How many completed orders are there?",
        "expected": 68
    },
    {
        "question": "Which products sold the most?",
        "expected": ("Running Shoes", 72)
    }
]


def evaluate():

    passed = 0
    failed = 0
    corrected = 0

    print("\nRunning self-correction evaluation...\n")

    for i, test in enumerate(TEST_CASES, 1):

        question = test["question"]

        print(f"{i}. {question}")

        try:

            sql = generate_sql(question)

            is_valid, message = validate_sql(sql)

            if not is_valid:

                print("Initial SQL invalid.")
                print("Attempting correction...")

                sql = fix_sql(
                    question,
                    sql,
                    message
                )

                corrected += 1

            try:

                generated_result = execute_sql(sql)[1]

            except Exception as e:

                print("Initial execution failed.")
                print("Attempting correction...")

                sql = fix_sql(
                    question,
                    sql,
                    str(e)
                )

                corrected += 1

                generated_result = execute_sql(sql)[1]

            if not generated_result:
                print("❌ FAIL - No result")
                failed += 1
                continue

            row = generated_result[0]

            if question == "How many customers are there?":

                passed_test = int(row[0]) == 8

            elif question == "How many products are there?":

                passed_test = int(row[0]) == 10

            elif question == "Which country has the most customers?":

                passed_test = row[0] == "India"

            elif question == "How many completed orders are there?":

                passed_test = int(row[0]) == 68

            elif question == "Which products sold the most?":

                passed_test = (
                    row[1] == "Running Shoes"
                    and int(row[2]) == 72
                )

            else:

                passed_test = False

            if passed_test:

                print("✅ PASS")
                passed += 1

            else:

                print("❌ FAIL")

                print("\nFinal SQL:")
                print(sql)

                print("\nExpected:")
                print(test["expected"])

                print("\nGenerated:")
                print(generated_result)

                failed += 1

        except Exception as e:

            print("❌ ERROR")
            print(e)

            failed += 1

        print()

    total = passed + failed

    accuracy = (
        passed / total * 100
        if total
        else 0
    )

    print("=" * 45)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {failed}/{total}")
    print(f"Corrected: {corrected}")
    print(f"End-to-End Accuracy: {accuracy:.1f}%")
    print("=" * 45)


if __name__ == "__main__":
    evaluate()