import sqlite3
import os

db_path = "C:/Users/bmore/.metaclaw/memory/memory.db"
wal_path = "C:/Users/bmore/.metaclaw/memory/memory.db-wal"

print(f"DB exists: {os.path.exists(db_path)}")
print(f"DB size: {os.path.getsize(db_path) if os.path.exists(db_path) else 'N/A'}")
print(f"WAL size: {os.path.getsize(wal_path) if os.path.exists(wal_path) else 'N/A'}")

try:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print(f"\nTables: {tables}")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        count = cur.fetchone()[0]
        print(f"  {t}: {count} rows")
        if count > 0:
            cur.execute(f"SELECT * FROM {t} LIMIT 5")
            for row in cur.fetchall():
                print(f"    {row}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
