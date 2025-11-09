import aiosqlite
from backend.config import settings


INIT_SQL = """
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  access_token TEXT UNIQUE NOT NULL,
  institution TEXT,
  cursor TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item_id INTEGER NOT NULL,
  plaid_txn_id TEXT UNIQUE NOT NULL,
  pending INTEGER NOT NULL,
  pending_transaction_id TEXT,
  amount REAL NOT NULL,
  currency TEXT,
  authorized_date TEXT,
  date TEXT,
  merchant_name TEXT,
  pfc_primary TEXT,
  pfc_detailed TEXT,
  raw_json TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(item_id) REFERENCES items(id)
);

CREATE TABLE IF NOT EXISTS tips (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pending_txn_id TEXT UNIQUE NOT NULL,
  expected_tip_amount REAL NOT NULL,
  expected_total REAL NOT NULL,
  actual_total REAL,
  posted_txn_id TEXT,
  is_overcharged INTEGER DEFAULT 0,
  overcharge_amount REAL DEFAULT 0,
  created_at TEXT NOT NULL,
  checked_at TEXT,
  FOREIGN KEY(pending_txn_id) REFERENCES transactions(plaid_txn_id),
  FOREIGN KEY(posted_txn_id) REFERENCES transactions(plaid_txn_id)
);
"""


async def get_db():
    """Get a database connection."""
    conn = await aiosqlite.connect(settings.DB_PATH)
    conn.row_factory = aiosqlite.Row
    return conn


async def init_db():
    """Initialize the database with tables."""
    conn = await get_db()
    try:
        await conn.executescript(INIT_SQL)
        await conn.commit()
    finally:
        await conn.close()
