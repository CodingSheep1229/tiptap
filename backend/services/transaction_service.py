import json
import asyncio
from datetime import datetime, timezone
from typing import Optional, List

from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_refresh_request import TransactionsRefreshRequest

from backend.database import get_db
from backend.plaid_client import plaid_client


async def upsert_transactions(item_id: int, txns: List[dict]):
    """Insert or update transactions in the database."""
    conn = await get_db()
    try:
        for t in txns:
            # Convert date objects to strings for JSON serialization
            raw_json_data = {}
            for key, value in t.items():
                if hasattr(value, 'isoformat'):  # date or datetime object
                    raw_json_data[key] = value.isoformat()
                else:
                    raw_json_data[key] = value

            # Extract date fields as strings
            authorized_date = t.get("authorized_date")
            if hasattr(authorized_date, 'isoformat'):
                authorized_date = authorized_date.isoformat()

            date_field = t.get("date")
            if hasattr(date_field, 'isoformat'):
                date_field = date_field.isoformat()

            await conn.execute(
                """
                INSERT INTO transactions (
                  item_id, plaid_txn_id, pending, pending_transaction_id, amount, currency,
                  authorized_date, date, merchant_name, pfc_primary, pfc_detailed, raw_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(plaid_txn_id) DO UPDATE SET
                  pending = excluded.pending,
                  pending_transaction_id = excluded.pending_transaction_id,
                  amount = excluded.amount,
                  currency = excluded.currency,
                  authorized_date = excluded.authorized_date,
                  date = excluded.date,
                  merchant_name = excluded.merchant_name,
                  pfc_primary = excluded.pfc_primary,
                  pfc_detailed = excluded.pfc_detailed,
                  raw_json = excluded.raw_json
                """,
                (
                    item_id,
                    t["transaction_id"],
                    1 if t.get("pending") else 0,
                    t.get("pending_transaction_id"),
                    t["amount"],
                    (t.get("iso_currency_code") or t.get("unofficial_currency_code")),
                    authorized_date,
                    date_field,
                    t.get("merchant_name"),
                    (t.get("personal_finance_category", {}) or {}).get("primary"),
                    (t.get("personal_finance_category", {}) or {}).get("detailed"),
                    json.dumps(raw_json_data),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
        await conn.commit()
    finally:
        await conn.close()


async def set_cursor(item_id: int, cursor: Optional[str]):
    """Update the cursor for an item."""
    conn = await get_db()
    try:
        await conn.execute("UPDATE items SET cursor=? WHERE id=?", (cursor, item_id))
        await conn.commit()
    finally:
        await conn.close()


async def get_items():
    """Get all items from the database."""
    conn = await get_db()
    try:
        rows = await conn.execute("SELECT * FROM items")
        return await rows.fetchall()
    finally:
        await conn.close()


async def check_for_overcharges(posted_txns: List[dict]):
    """Check if any posted transactions show tip overcharges."""
    conn = await get_db()
    try:
        for txn in posted_txns:
            # Skip if this isn't a posted transaction with a link to a pending one
            if txn.get("pending") or not txn.get("pending_transaction_id"):
                continue

            pending_id = txn["pending_transaction_id"]
            posted_id = txn["transaction_id"]
            actual_total = txn["amount"]

            # Get the original pending transaction amount
            pending_row = await conn.execute(
                "SELECT amount FROM transactions WHERE plaid_txn_id = ?",
                (pending_id,)
            )
            pending_txn = await pending_row.fetchone()
            pending_amount = pending_txn["amount"] if pending_txn else None

            # Check if we have a tip record for this pending transaction
            row = await conn.execute(
                "SELECT * FROM tips WHERE pending_txn_id = ? AND checked_at IS NULL",
                (pending_id,)
            )
            tip_record = await row.fetchone()

            if tip_record:
                expected_total = tip_record["expected_total"]
                overcharge_amount = actual_total - expected_total
                is_overcharged = overcharge_amount > 0.01  # Allow 1 cent tolerance for rounding

                # Update the tip record
                await conn.execute(
                    """
                    UPDATE tips
                    SET actual_total = ?,
                        posted_txn_id = ?,
                        is_overcharged = ?,
                        overcharge_amount = ?,
                        checked_at = ?
                    WHERE pending_txn_id = ?
                    """,
                    (actual_total, posted_id, 1 if is_overcharged else 0,
                     overcharge_amount if is_overcharged else 0,
                     datetime.now(timezone.utc).isoformat(), pending_id)
                )

                # Log detailed information
                print(f"\n{'='*60}")
                print(f"Transaction: {txn.get('merchant_name')}")
                print(f"Pending ID: {pending_id}")
                print(f"Posted ID:  {posted_id}")
                print(f"Pending Amount: ${abs(pending_amount):.2f}" if pending_amount else "N/A")
                print(f"Expected Tip:   ${tip_record['expected_tip_amount']:.2f}")
                print(f"Expected Total: ${abs(expected_total):.2f}")
                print(f"Actual Total:   ${abs(actual_total):.2f}")
                print(f"Difference:     ${overcharge_amount:.2f}")

                if is_overcharged:
                    print(f"⚠️  STATUS: OVERCHARGED by ${overcharge_amount:.2f}")
                else:
                    print(f"✓ STATUS: VERIFIED (no overcharge)")
                print(f"{'='*60}\n")

        await conn.commit()
    finally:
        await conn.close()


async def transactions_sync(item_id: int, access_token: str, cursor: Optional[str]):
    """Use /transactions/sync with a cursored loop and upsert results."""
    has_more = True
    local_cursor = cursor
    new_pending = []
    new_posted = []

    while has_more:
        # Build request - only include cursor if we have one
        req_params = {"access_token": access_token}
        if local_cursor:
            req_params["cursor"] = local_cursor

        req = TransactionsSyncRequest(**req_params)
        resp = plaid_client.transactions_sync(req).to_dict()
        await upsert_transactions(item_id, resp.get("added", []))
        await upsert_transactions(item_id, resp.get("modified", []))

        # Collect for pretty console output
        for t in resp.get("added", []):
            (new_pending if t.get("pending") else new_posted).append(t)
        for t in resp.get("modified", []):
            (new_pending if t.get("pending") else new_posted).append(t)

        local_cursor = resp.get("next_cursor")
        has_more = bool(resp.get("has_more"))

    await set_cursor(item_id, local_cursor)

    # Check for tip overcharges on newly posted transactions
    await check_for_overcharges(new_posted)

    # Print pending→posted pairings for inspection
    posted_by_pending = {
        t.get("pending_transaction_id"): t for t in new_posted if t.get("pending_transaction_id")
    }
    if posted_by_pending:
        print("\n=== Pending → Posted matches (by pending_transaction_id) ===")
        for p in new_pending:
            if not p.get("pending"):
                continue
            pend_id = p["transaction_id"]
            match = posted_by_pending.get(pend_id)
            if match:
                print(f"* {p.get('merchant_name')}  "
                      f"pending ${p['amount']} on {p.get('authorized_date') or p.get('date')}  ->  "
                      f"posted ${match['amount']} on {match.get('date')}  "
                      f"(pending_txn_id carried over)")
    else:
        if new_posted:
            print("\n(no pending→posted links in this batch; may be historical or already matched)")

    # Print FOOD_AND_DRINK transactions
    food_posted = [
        t for t in (new_pending + new_posted)
        if (t.get("personal_finance_category") or {}).get("primary") == "FOOD_AND_DRINK"
    ]
    if food_posted:
        print("\n=== FOOD_AND_DRINK transactions observed ===")
        for t in food_posted:
            state = "PENDING" if t.get("pending") else "POSTED"
            print(f"[{state}] {t.get('merchant_name')} ${t['amount']}  "
                  f"{t.get('authorized_date') or t.get('date')}  "
                  f"PFC={ (t.get('personal_finance_category') or {}).get('detailed') }")


async def trigger_transactions_refresh(access_token: str):
    """Trigger Plaid to refresh transactions (sandbox only)."""
    refresh_req = TransactionsRefreshRequest(access_token=access_token)
    plaid_client.transactions_refresh(refresh_req)
    await asyncio.sleep(2)  # Wait for Plaid to process
