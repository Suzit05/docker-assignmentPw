from flask import Flask
import mysql.connector
import os
import time

app = Flask(__name__)

# Database configuration from environment variables
db_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

def get_db_connection():
    # Retry logic to wait for DB container
    for _ in range(10):
        try:
            return mysql.connector.connect(**db_config)
        except:
            time.sleep(2)
    return None

@app.route("/")
def home():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed"

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS visits (count INT)")
    cursor.execute("SELECT count FROM visits")

    row = cursor.fetchone()
    if row is None:
        count = 1
        cursor.execute("INSERT INTO visits VALUES (1)")
    else:
        count = row[0] + 1
        cursor.execute("UPDATE visits SET count = %s", (count,))

    conn.commit()
    cursor.close()
    conn.close()

    return f"<h1>Hello from Docker Compose!</h1><p>Visits: {count}</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
