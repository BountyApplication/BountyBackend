import sqlite3
from pathlib import Path

DB_NAME = "bounty24.db"

db_path = Path(DB_NAME)
if not db_path.exists():
    print(f"{DB_NAME} not found — nothing to migrate.")
else:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("PRAGMA table_info(products);")
    columns = [row[1] for row in cur.fetchall()]
    if "stock" in columns:
        print("Column 'stock' already exists — skipping.")
    else:
        cur.execute("ALTER TABLE products ADD COLUMN stock INTEGER DEFAULT NULL;")
        con.commit()
        print("Migration successful: added column 'stock' to products.")
    con.close()
