from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from backend.database import get_db
from backend.models import RecordTipReq


router = APIRouter()


@router.post("/tips")
async def record_tip(body: RecordTipReq):
    """Record the tip amount the user chose for a pending transaction."""
    conn = await get_db()
    try:
        # Get the pending transaction amount
        row = await conn.execute(
            "SELECT amount FROM transactions WHERE plaid_txn_id = ? AND pending = 1",
            (body.pending_txn_id,)
        )
        txn = await row.fetchone()
        if not txn:
            raise HTTPException(status_code=404, detail="Pending transaction not found")

        pending_amount = txn["amount"]
        expected_total = pending_amount + body.tip_amount

        # Insert tip record
        await conn.execute(
            """
            INSERT INTO tips (pending_txn_id, expected_tip_amount, expected_total, created_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(pending_txn_id) DO UPDATE SET
                expected_tip_amount = excluded.expected_tip_amount,
                expected_total = excluded.expected_total
            """,
            (body.pending_txn_id, body.tip_amount, expected_total, datetime.now(timezone.utc).isoformat())
        )
        await conn.commit()
        return {"ok": True, "expected_total": expected_total}
    finally:
        await conn.close()


@router.get("/tips")
async def get_tip_records():
    """Get all tip records with overcharge detection status."""
    conn = await get_db()
    try:
        rows = await conn.execute(
            """
            SELECT
                t.id,
                t.pending_txn_id,
                t.expected_tip_amount,
                t.expected_total,
                t.actual_total,
                t.posted_txn_id,
                t.is_overcharged,
                t.overcharge_amount,
                t.created_at,
                t.checked_at,
                pt.merchant_name,
                pt.amount as pending_amount
            FROM tips t
            JOIN transactions pt ON t.pending_txn_id = pt.plaid_txn_id
            ORDER BY t.created_at DESC
            """
        )
        records = await rows.fetchall()
        return [dict(row) for row in records]
    finally:
        await conn.close()
