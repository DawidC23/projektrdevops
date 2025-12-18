from flask import Flask, jsonify
from src.db import get_connection

import os
import psycopg2

app = Flask(__name__)
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        port=5432
    )

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/health/db")
def health_db():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            dbname=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            connect_timeout=2
        )
        conn.close()
        return jsonify(status="ok", db="connected")
    except Exception:
        return jsonify(status="error", db="disconnected"), 500

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = [
        {"id": r[0], "name": r[1], "email": r[2]}
        for r in rows
    ]
    return jsonify(users)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "created"}), 201

@app.route("/")
def home():
    return "Flask + PostgreSQL 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
