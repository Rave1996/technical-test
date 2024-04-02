from sqlalchemy import Column, ForeignKey, Numeric, String, Integer, Identity, Boolean, DateTime
from sqlalchemy.orm import relationship

from db.models.base import BaseModel

class CustomerORM(BaseModel):
    __tablename__ = "customers"

    id = Column(Integer, Identity(start=1), primary_key=True)
    full_name = Column(String(length=200), nullable=False)
    email = Column(String(length=100), unique=True, nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    loans = relationship("LoanORM", back_populates="customer", cascade="all, delete-orphan")

    class Config:
        orm_mode = True

    def __str__(self) -> str:
        return f"Customer(id='{self.id}', full_name='{self.full_name}', email='{self.email}')"

class LoanORM(BaseModel):
    __tablename__ = "loans"

    id = Column(Integer, Identity(start=1), primary_key=True)
    customer_id = Column(ForeignKey(CustomerORM.id, deferrable=True, initially="DEFERRED"), nullable=False, index=True)
    amount = Column(Numeric(19, 2), nullable=False)
    issued = Column(DateTime, nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    customer = relationship("CustomerORM", back_populates="loans", primaryjoin="LoanORM.customer_id == CustomerORM.id")

    payments = relationship("PaymentsORM", back_populates="loans", cascade="all, delete-orphan")

    class Config:
        orm_mode = True

    def __str__(self) -> str:
        return f"Loan(id='{self.id}', customer_id='{self.customer_id}')"

class PaymentsORM(BaseModel):
    __tablename__ = "payments"

    id = Column(Integer, Identity(start=1), primary_key=True)
    loan_id = Column(ForeignKey(LoanORM.id, deferrable=True, initially="DEFERRED"), nullable=False, index=True)
    amount = Column(Numeric(19, 2), nullable=False)
    issued = Column(DateTime, nullable=False)
    status = Column(Boolean, nullable=False, default=True)

    loan = relationship("LoanORM", back_populates="payments", primaryjoin="PaymentsORM.loan_id == LoanORM.id")

    class Config:
        orm_mode = True

    def __str__(self) -> str:
        return f"Payment(id='{self.id}', loan_id='{self.loan_id}')"