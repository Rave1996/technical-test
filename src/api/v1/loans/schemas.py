from pydantic import BaseModel
from typing import Optional


class LoanSchema(BaseModel):
    id: Optional[int] = None
    customer_id: Optional[int] = None
    amount: Optional[float] = None
    status: Optional[bool] = True
