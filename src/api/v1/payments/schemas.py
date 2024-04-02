from pydantic import BaseModel
from typing import Optional


class PaymentsSchema(BaseModel):
    id: Optional[int] = None
    loan_id: Optional[int] = None
    amount: Optional[float] = None
    issued: Optional[int] = None
    status: Optional[bool] = True
