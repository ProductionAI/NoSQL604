"""
MariaDB + Python Demonstration using PyMySQL
Covers: connecting, creating tables, CRUD operations, transactions, and queries
"""

import pymysql
import pymysql.cursors
from datetime import date

# ── 1. CONNECTION ─────────────────────────────────────────────────────────────
print("=" * 55)
print("  MariaDB + Python Demo")
print("=" * 55)

conn = pymysql.connect(
    host="127.0.0.1",
    user="demo_user",
    password="demo_pass",
    database="demo_db",
    cursorclass=pymysql.cursors.DictCursor,   # rows as dicts
    autocommit=False,
)
print("\n✅  Connected to MariaDB\n")

cursor = conn.cursor()

# ── 2. CREATE TABLE ───────────────────────────────────────────────────────────
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("""
    CREATE TABLE employees (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        name        VARCHAR(100)   NOT NULL,
        department  VARCHAR(50)    NOT NULL,
        salary      DECIMAL(10, 2) NOT NULL,
        hire_date   DATE           NOT NULL
    )
""")
conn.commit()
print("📋  Table 'employees' created\n")

# ── 3. INSERT (single row) ────────────────────────────────────────────────────
cursor.execute("""
    INSERT INTO employees (name, department, salary, hire_date)
    VALUES (%s, %s, %s, %s)
""", ("Alice Johnson", "Engineering", 95000.00, date(2021, 3, 15)))
conn.commit()
print(f"➕  Inserted 1 row  (last id = {cursor.lastrowid})")

# ── 4. INSERT MANY (batch) ────────────────────────────────────────────────────
employees = [
    ("Bob Smith",    "Marketing",   72000.00, date(2020, 7,  1)),
    ("Carol White",  "Engineering", 105000.00, date(2019, 11, 20)),
    ("David Lee",    "HR",          68000.00, date(2022, 1,  10)),
    ("Eva Martinez", "Engineering",  89000.00, date(2023, 5,  5)),
]
cursor.executemany("""
    INSERT INTO employees (name, department, salary, hire_date)
    VALUES (%s, %s, %s, %s)
""", employees)
conn.commit()
print(f"➕  Inserted {cursor.rowcount} more rows via executemany\n")

# ── 5. SELECT ALL ─────────────────────────────────────────────────────────────
cursor.execute("SELECT * FROM employees ORDER BY id")
rows = cursor.fetchall()
print("📊  All employees:")
print(f"  {'ID':<4} {'Name':<20} {'Department':<15} {'Salary':>10}  {'Hire Date'}")
print("  " + "-" * 65)
for r in rows:
    print(f"  {r['id']:<4} {r['name']:<20} {r['department']:<15}"
          f"  ${r['salary']:>9,.2f}  {r['hire_date']}")

# ── 6. SELECT with WHERE + parameterised query ────────────────────────────────
dept = "Engineering"
cursor.execute(
    "SELECT name, salary FROM employees WHERE department = %s ORDER BY salary DESC",
    (dept,)
)
eng = cursor.fetchall()
print(f"\n🔍  Engineers (filtered query):")
for r in eng:
    print(f"  {r['name']:<20}  ${r['salary']:,.2f}")

# ── 7. AGGREGATE QUERY ────────────────────────────────────────────────────────
cursor.execute("""
    SELECT department,
           COUNT(*)       AS headcount,
           AVG(salary)    AS avg_salary,
           MAX(salary)    AS max_salary
    FROM   employees
    GROUP  BY department
    ORDER  BY avg_salary DESC
""")
print("\n📈  Department summary:")
print(f"  {'Department':<15} {'Headcount':>10} {'Avg Salary':>12} {'Max Salary':>12}")
print("  " + "-" * 52)
for r in cursor.fetchall():
    print(f"  {r['department']:<15} {r['headcount']:>10}"
          f"  ${r['avg_salary']:>10,.2f}  ${r['max_salary']:>10,.2f}")

# ── 8. UPDATE ─────────────────────────────────────────────────────────────────
cursor.execute(
    "UPDATE employees SET salary = salary * 1.10 WHERE department = %s",
    ("Engineering",)
)
conn.commit()
print(f"\n✏️   Gave Engineering a 10% raise  ({cursor.rowcount} rows updated)")

# ── 9. TRANSACTIONS (rollback demo) ──────────────────────────────────────────
print("\n🔄  Transaction demo (intentional rollback):")
try:
    cursor.execute(
        "INSERT INTO employees (name, department, salary, hire_date) "
        "VALUES (%s, %s, %s, %s)",
        ("Test User", "Temp", 50000, date(2024, 1, 1))
    )
    cursor.execute("SELECT COUNT(*) AS cnt FROM employees")
    before = cursor.fetchone()["cnt"]
    print(f"  Rows mid-transaction: {before}")

    raise ValueError("Simulated error – rolling back!")   # force rollback

    conn.commit()   # never reached

except ValueError as e:
    conn.rollback()
    cursor.execute("SELECT COUNT(*) AS cnt FROM employees")
    after = cursor.fetchone()["cnt"]
    print(f"  ⚠️  {e}")
    print(f"  Rows after rollback:  {after}  ✅ unchanged")

# ── 10. DELETE ────────────────────────────────────────────────────────────────
cursor.execute("DELETE FROM employees WHERE name = %s", ("David Lee",))
conn.commit()
print(f"\n🗑️   Deleted {cursor.rowcount} row (David Lee)")

# ── 11. FINAL STATE ───────────────────────────────────────────────────────────
cursor.execute("SELECT COUNT(*) AS cnt, SUM(salary) AS total FROM employees")
summary = cursor.fetchone()
print(f"\n📌  Final table: {summary['cnt']} employees, "
      f"total payroll = ${summary['total']:,.2f}")

# ── CLEANUP ───────────────────────────────────────────────────────────────────
cursor.close()
conn.close()
print("\n🔒  Connection closed. Demo complete!\n")