from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

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


@app.route("/")
def home():
    return "Flask + PostgreSQL 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
