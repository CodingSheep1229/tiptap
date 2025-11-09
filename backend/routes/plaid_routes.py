from datetime import datetime, timezone
from fastapi import APIRouter

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from backend.config import settings
from backend.database import get_db
from backend.models import LinkTokenResp, ExchangeReq, ExchangeResp
from backend.plaid_client import plaid_client


router = APIRouter()


@router.post("/link/token", response_model=LinkTokenResp)
async def create_link_token():
    """Create a Link token (backend step)."""
    req = LinkTokenCreateRequest(
        user=LinkTokenCreateRequestUser(client_user_id="demo-user-123"),
        client_name="TipTap - Tip Tracker",
        products=[Products("transactions")],
        country_codes=[CountryCode(x.strip()) for x in settings.PLAID_COUNTRY_CODES.split(",")],
        language="en",
    )
    resp = plaid_client.link_token_create(req)
    return LinkTokenResp(link_token=resp.to_dict()["link_token"])


@router.post("/exchange", response_model=ExchangeResp)
async def exchange_public_token(body: ExchangeReq):
    """Exchange public_token -> access_token and store new Item."""
    ex_req = ItemPublicTokenExchangeRequest(public_token=body.public_token)
    ex_resp = plaid_client.item_public_token_exchange(ex_req).to_dict()
    access_token = ex_resp["access_token"]

    conn = await get_db()
    try:
        await conn.execute(
            "INSERT OR IGNORE INTO items (access_token, institution, cursor, created_at) VALUES (?, ?, ?, ?)",
            (access_token, None, None, datetime.now(timezone.utc).isoformat()),
        )
        await conn.commit()
        row = await conn.execute("SELECT id FROM items WHERE access_token=?", (access_token,))
        item_row = await row.fetchone()
        return ExchangeResp(item_id=item_row["id"])
    finally:
        await conn.close()
