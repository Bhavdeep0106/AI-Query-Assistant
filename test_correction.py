from text_to_sql import fix_sql, validate_sql, execute_sql


question = "How many customers are there?"

broken_sql = """
SELECT COUNT(*) FROM customer;
"""

error = "no such table: customer"


print("Original SQL:")
print(broken_sql)

fixed_sql = fix_sql(
    question,
    broken_sql,
    error
)

print("\nFixed SQL:")
print(fixed_sql)

is_valid, message = validate_sql(fixed_sql)

print("\nValidation:")
print(is_valid, message)

if is_valid:

    columns, results = execute_sql(fixed_sql)

    print("\nResult:")
    print(results)

    if results and results[0][0] == 8:
        print("\n✅ SELF-CORRECTION PASSED")
    else:
        print("\n❌ SELF-CORRECTION FAILED")