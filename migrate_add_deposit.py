import json
import sqlite3
import sys
from pathlib import Path

DB_NAME = "bounty24.db"

# usage:
#   python3 migrate_add_deposit.py             adds the columns
#   python3 migrate_add_deposit.py --backfill  additionally recalculates the counters from the history
#
# mark the products first (bottles = 1, deposit return article = -1), only then run the backfill,
# otherwise there is nothing to count.


def add_column(cur, table, column, definition):
    cur.execute("PRAGMA table_info(%s);" % table)
    columns = [row[1] for row in cur.fetchall()]
    if column in columns:
        print("Column '%s' already exists in %s — skipping." % (column, table))
        return False
    cur.execute("ALTER TABLE %s ADD COLUMN %s %s;" % (table, column, definition))
    print("Added column '%s' to %s." % (column, table))
    return True


def backfill(con, cur):
    cur.execute("SELECT productId, deposit FROM products;")
    deposits = {row[0]: row[1] or 0 for row in cur.fetchall()}
    if not any(deposits.values()):
        print("\nNo product carries a deposit yet — mark the products first, then run --backfill again.")
        return

    cur.execute("SELECT userId, firstname, lastname FROM accounts;")
    accounts = cur.fetchall()
    negatives = []

    for userId, firstname, lastname in accounts:
        cur.execute("SELECT products FROM history WHERE userId=?;", (userId,))
        counter = 0
        for (productsJson,) in cur.fetchall():
            if not productsJson:
                continue
            try:
                bookedProducts = json.loads(productsJson)
            except (ValueError, TypeError):
                print("  skipped unreadable booking of user %s" % userId)
                continue
            for item in bookedProducts:
                counter += deposits.get(item.get('productId'), 0) * item.get('amount', 0)

        if counter < 0:
            negatives.append((userId, firstname, lastname, counter))
            counter = 0

        cur.execute("UPDATE accounts SET deposit=? WHERE userId=?;", (counter, userId))

    con.commit()
    print("\nRecalculated the deposit counter of %d accounts." % len(accounts))

    if not negatives:
        print("No account returned more deposit than it bought.")
        return

    print("\n%d accounts returned more deposit than they bought (set to 0):" % len(negatives))
    for userId, firstname, lastname, counter in negatives:
        print("  [%s] %s %s: %d" % (userId, firstname, lastname, counter))


db_path = Path(DB_NAME)
if not db_path.exists():
    print("%s not found — nothing to migrate." % DB_NAME)
    sys.exit(1)

con = sqlite3.connect(db_path)
cur = con.cursor()

add_column(cur, "products", "deposit", "INTEGER DEFAULT 0")
add_column(cur, "accounts", "deposit", "INTEGER DEFAULT 0")
con.commit()

if "--backfill" in sys.argv:
    backfill(con, cur)
else:
    print("\nRun with --backfill once the products are marked to recalculate the counters.")

con.close()
