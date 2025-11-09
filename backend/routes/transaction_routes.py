from fastapi import APIRouter, Request

from backend.database import get_db
from backend.services.transaction_service import transactions_sync, get_items


router = APIRouter()


@router.post("/webhook")
async def plaid_webhook(request: Request):
    """Plaid Transactions webhook handler."""
    payload = await request.json()
    if payload.get("webhook_type") == "TRANSACTIONS" and payload.get("webhook_code") == "SYNC_UPDATES_AVAILABLE":
        items = await get_items()
        for it in items:
            await transactions_sync(it["id"], it["access_token"], it["cursor"])
    return {"ok": True}


@router.post("/sync")
async def manual_sync():
    """Manual trigger for transaction sync."""
    items = await get_items()
    for it in items:
        await transactions_sync(it["id"], it["access_token"], it["cursor"])
    return {"ok": True}


@router.get("/transactions/pending")
async def get_pending_transactions():
    """Get all pending transactions (potential restaurant charges)."""
    conn = await get_db()
    try:
        rows = await conn.execute(
            """
            SELECT plaid_txn_id, pending, amount, merchant_name, date, authorized_date
            FROM transactions
            WHERE pending = 1
            ORDER BY authorized_date DESC, date DESC
            """
        )
        txns = await rows.fetchall()
        return [dict(row) for row in txns]
    finally:
        await conn.close()
