from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/log-ticket', methods=['POST'])
def log_ticket():
    data = request.get_json()
    ticket_id = data.get('ticket_id')
    title = data.get('title')
    resolution_notes = data.get('resolution_notes')

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ticket_resolutions (ticket_id, title, resolution_notes) VALUES (%s, %s, %s)",
            (ticket_id, title, resolution_notes)
        )
        conn.commit()
        return jsonify({"message": "✅ Ticket logged"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
