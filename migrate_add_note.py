import sqlite3
from pathlib import Path

DB_NAME = "bounty24.db"

# adds the customer note to the accounts:
#   note      free text shown when the customer is opened
#   noteLevel 'info' for a banner above the products, 'warning' for a modal

COLUMNS = [
    ("note", "VARCHAR(200)"),
    ("noteLevel", "VARCHAR(10)"),
]

db_path = Path(DB_NAME)
if not db_path.exists():
    print("%s not found — nothing to migrate." % DB_NAME)
else:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("PRAGMA table_info(accounts);")
    existing = [row[1] for row in cur.fetchall()]

    for column, definition in COLUMNS:
        if column in existing:
            print("Column '%s' already exists — skipping." % column)
            continue
        cur.execute("ALTER TABLE accounts ADD COLUMN %s %s;" % (column, definition))
        print("Added column '%s' to accounts." % column)

    con.commit()
    con.close()
