from pydantic import BaseModel
from typing import Optional


class CustomerSchema(BaseModel):
    id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[bool] = True
