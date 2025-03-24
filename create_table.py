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

# Connect and create table
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS ticket_resolutions (
        ticket_id TEXT PRIMARY KEY,
        title TEXT,
        priority TEXT,
        resolved_date TIMESTAMP,
        resolution_notes TEXT
    );
    """

    cursor.execute(create_table_query)
    conn.commit()
    print("✅ Table 'ticket_resolutions' created successfully.")

except Exception as e:
    print("❌ Error:", e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
