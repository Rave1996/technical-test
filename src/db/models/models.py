from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class Customer(BaseModel):
    __tablename__ = "customers"

    full_name = Column(String(length=200), nullable=False)
    email = Column(String(length=100), unique=True, nullable=False)

    def __str__(self) -> str:
        return f"Customer(id='{self.id}', full_name='{self.full_name}', email='{self.email}')"


class Loan(BaseModel):
    __tablename__ = "loans"

    amount = Column(Numeric(19, 2), nullable=False)
    customer_id = Column(ForeignKey(Customer.id, deferrable=True, initially="DEFERRED"), nullable=False, index=True)

    customer = relationship(Customer, primaryjoin="Loan.customer_id == Customer.id")

    def __str__(self) -> str:
        return f"Loan(id='{self.id}', customer_id='{self.customer_id}')"
