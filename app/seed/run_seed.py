import psycopg2
import os
import csv
from datetime import datetime

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

OUTPUT_DIR = "/seed_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    port=5432
)

cur = conn.cursor()

# tabela testowa
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
""")

users = [
    ("Jan", "jan@test.pl"),
    ("Anna", "anna@test.pl"),
    ("Piotr", "piotr@test.pl"),
    ("Kasia", "kasia@test.pl"),
    ("Tomek", "tomek@test.pl"),
]

for u in users:
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", u)

conn.commit()

# zapis CSV
csv_path = f"{OUTPUT_DIR}/users.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "email"])
    writer.writerows(users)

# zapis loga
log_path = f"{OUTPUT_DIR}/seed.log"
with open(log_path, "w") as f:
    f.write(f"Seed completed at {datetime.now()}\n")
    f.write(f"Inserted {len(users)} users\n")

cur.close()
conn.close()

print("Seeding completed successfully")
