from flask import Flask, request, jsonify, abort
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Load secrets and DB config
SECRET_TOKEN = os.getenv("WEBHOOK_SECRET")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", 5432)


@app.route('/log-ticket', methods=['POST'])
def log_ticket():
    # Authenticate using header token
    auth_token = request.headers.get("X-Auth-Token")
    if auth_token != SECRET_TOKEN:
        abort(401, description="Unauthorized: Invalid token.")

    data = request.get_json()

    ticket_id = data.get("ticket_id")
    title = data.get("title")
    resolution_notes = data.get("resolution_notes")
    received_at = datetime.now()

    # Validate required fields
    if not all([ticket_id, title]):
        abort(400, description="Missing required fields.")

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Insert ticket into database
        cur.execute("""
            INSERT INTO ticket_resolutions (ticket_id, title, resolution_notes, received_at)
            VALUES (%s, %s, %s, %s)
        """, (ticket_id, title, resolution_notes, received_at))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("DB Error:", e)
        return jsonify({"error": "Database insert failed"}), 500


if __name__ == '__main__':
    app.run(debug=True)

