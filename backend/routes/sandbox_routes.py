from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from backend.config import settings
from backend.database import get_db
from backend.plaid_client import plaid_client
from backend.services.transaction_service import (
    transactions_sync,
    get_items,
    trigger_transactions_refresh
)


router = APIRouter(prefix="/sandbox")


@router.post("/create_test_item")
async def create_test_item():
    """Create a test item with dynamic transactions for testing."""
    if settings.PLAID_ENV.lower() != "sandbox":
        raise HTTPException(status_code=400, detail="Only available in sandbox mode")

    try:
        # Create a public token for the dynamic transactions test user
        req = SandboxPublicTokenCreateRequest(
            institution_id="ins_109508",  # First Platypus Bank (non-OAuth)
            initial_products=[Products("transactions")],
            options={
                "override_username": "user_transactions_dynamic"
            }
        )
        resp = plaid_client.sandbox_public_token_create(req)
        public_token = resp.to_dict()["public_token"]

        # Exchange for access token
        ex_req = ItemPublicTokenExchangeRequest(public_token=public_token)
        ex_resp = plaid_client.item_public_token_exchange(ex_req).to_dict()
        access_token = ex_resp["access_token"]

        # Store in database
        conn = await get_db()
        try:
            await conn.execute(
                "INSERT OR IGNORE INTO items (access_token, institution, cursor, created_at) VALUES (?, ?, ?, ?)",
                (access_token, "First Platypus Bank (TEST)", None, datetime.now(timezone.utc).isoformat()),
            )
            await conn.commit()
            row = await conn.execute("SELECT id FROM items WHERE access_token=?", (access_token,))
            item_row = await row.fetchone()
            item_id = item_row["id"]
        finally:
            await conn.close()

        # Initial sync to get the 50 pending + 50 posted transactions
        await transactions_sync(item_id, access_token, None)

        return {
            "ok": True,
            "item_id": item_id,
            "message": "Test item created with 50 pending and 50 posted transactions. Use /sandbox/simulate_transaction_update to simulate pending→posted transitions and tip changes."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/simulate_transaction_update")
async def simulate_transaction_update():
    """Trigger /transactions/refresh to simulate new transaction activity."""
    if settings.PLAID_ENV.lower() != "sandbox":
        raise HTTPException(status_code=400, detail="Only available in sandbox mode")

    items = await get_items()
    if not items:
        raise HTTPException(status_code=404, detail="No items found. Create a test item first.")

    results = []
    for item in items:
        try:
            # Trigger the refresh
            await trigger_transactions_refresh(item["access_token"])

            # Sync to get the updated transactions
            await transactions_sync(item["id"], item["access_token"], item["cursor"])

            results.append({
                "item_id": item["id"],
                "status": "refreshed"
            })
        except Exception as e:
            results.append({
                "item_id": item["id"],
                "status": "error",
                "error": str(e)
            })

    return {
        "ok": True,
        "results": results,
        "message": "Transaction updates simulated. Check your pending transactions - some should now be posted!"
    }
