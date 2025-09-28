import os
import time
import subprocess
import psycopg2

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DB = os.getenv("POSTGRES_DB", "paris_data")
POSTGRES_USER = os.getenv("POSTGRES_USER", "eya")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "eyaeya")

# -------------------- Wait for PostgreSQL --------------------
while True:
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )
        conn.close()
        print("✅ PostgreSQL is ready")
        break
    except Exception:
        print("⏳ Waiting for PostgreSQL...")
        time.sleep(1)

# -------------------- Run ETL --------------------
print("🔹 Running ETL...")
subprocess.run(["bash", "/app/db-init/load.sh"], check=True)

# -------------------- Start Gunicorn --------------------
print("🚀 Starting Gunicorn...")
subprocess.run([
    "gunicorn",
    "dashboard.app:server",
    "--bind", "0.0.0.0:8050",
    "--workers", "2",
    "--threads", "2",
    "--timeout", "120"
])
