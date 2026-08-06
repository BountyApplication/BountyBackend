import sqlite3
from pathlib import Path

DB_NAME = "bounty24.db"

# adds the donation column to the history.
# the settings table is created by BountyDatabase on startup, it needs no migration.

db_path = Path(DB_NAME)
if not db_path.exists():
    print("%s not found — nothing to migrate." % DB_NAME)
else:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("PRAGMA table_info(history);")
    columns = [row[1] for row in cur.fetchall()]
    if "donation" in columns:
        print("Column 'donation' already exists — skipping.")
    else:
        cur.execute("ALTER TABLE history ADD COLUMN donation FLOAT DEFAULT 0;")
        con.commit()
        print("Migration successful: added column 'donation' to history.")
    con.close()
