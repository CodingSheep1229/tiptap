from typing import Optional
from pydantic import BaseModel


# Link and Exchange Models
class LinkTokenResp(BaseModel):
    link_token: str


class ExchangeReq(BaseModel):
    public_token: str


class ExchangeResp(BaseModel):
    item_id: int


# Tip Tracking Models
class RecordTipReq(BaseModel):
    pending_txn_id: str
    tip_amount: float


class TipRecord(BaseModel):
    id: int
    pending_txn_id: str
    expected_tip_amount: float
    expected_total: float
    actual_total: Optional[float]
    posted_txn_id: Optional[str]
    is_overcharged: bool
    overcharge_amount: float
    merchant_name: Optional[str]
    pending_amount: float
    created_at: str
    checked_at: Optional[str]


# Transaction Models
class Transaction(BaseModel):
    plaid_txn_id: str
    pending: bool
    amount: float
    merchant_name: Optional[str]
    date: Optional[str]
    authorized_date: Optional[str]
