import psycopg2
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Get environment variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()

    alter_table_query = """
    ALTER TABLE ticket_resolutions
    ADD COLUMN IF NOT EXISTS received_at TIMESTAMP;
    """

    cursor.execute(alter_table_query)
    conn.commit()
    print("✅ Column 'received_at' added successfully.")

except Exception as e:
    print("❌ Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
