from fastapi import APIRouter, status, Response, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session, Query


from api.v1.payments.schemas import PaymentsSchema
from core.utils.responses import PaginationParams, default_pagination_params, EnvelopeResponse
from db.models import CustomerORM, PaymentsORM, LoanORM
from db.session import get_session

from src.core.utils.datetime import LocalTime

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/retrieve/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def retrieve_payment(id: int = 0, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        payment = db.query(PaymentsORM).filter(PaymentsORM.id == id).first()

        if payment is None:
            raise Exception("Record not found")

        result = PaymentsSchema(
            id=payment.id, customer_id=payment.customer_id, amount=payment.amount, status=payment.status
        )

        response.body = result
    except Exception as exc:
        response.errors = str(exc)

    return response



@router.get("/list", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def list_payments(
        filter: str = '', status: bool = Query(True), db: Session = Depends(get_session),
        params: PaginationParams = Depends(default_pagination_params)
    ):
    response = EnvelopeResponse()

    try:
        payments = db.query(PaymentsORM).join(CustomerORM).order_by(PaymentsORM.id).filter(PaymentsORM.status == status)

        if filter != '':
            payments = payments.filter(
                CustomerORM.full_name.ilike(f'%{filter}%') | CustomerORM.email.ilike(f'%{filter}%')
            )

        # Working but not receiving query params to alter amounts
        records = paginate(payments, params=params)

        # Convert models to schemas
        result = [PaymentsSchema(**item.dict()) for item in records.items]

        response.body = result
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=EnvelopeResponse)
async def create_payment(payment: PaymentsSchema, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate customer account existence
        loan = db.query(CustomerORM).filter(LoanORM.id == payment.loan_id).first()

        if loan is None:
            raise Exception("Customer not found")

        # Validate parameters' content
        if payment.customer_id is None or payment.amount is None:
            raise Exception("Missing parameter")

        amount = payment.amount + ((payment.amount*.15) * 1.16)

        # Generate customer record
        new_payment = PaymentsORM(loan_id=payment.loan_id, amount=amount, issued=LocalTime.now())

        # Insert new record
        db.add(new_payment)
        db.commit()

        # Recover new data
        db.refresh(new_payment)

        # Convert from model to schema
        new_payment = PaymentsSchema(
            id=new_payment.id, customer_id=new_payment.customer_id, amount=new_payment.amount, status=new_payment.status
        )

        response.body = new_payment
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def delete_payment(id: int, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate record existence
        record = db.query(PaymentsORM).where(PaymentsORM.id == id).first()

        if record is None:
            raise Exception("Record not found")

        # Physical deletion
        db.delete(record)

        # Update record on DB
        db.commit()

        # Convert from model to schema
        deleted_customer = PaymentsSchema(
            id=record.id, customer_id=record.customer_id, amount=record.amount, status=record.status
        )

        response.body = deleted_customer
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.delete("/disable/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def disable_payment(id: int, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate record existence
        record = db.query(PaymentsORM).where(PaymentsORM.id == id).first()

        if record is None:
            raise Exception("Record not found")

        # Logical deletion
        record.status = False

        # Update record on DB
        db.commit()

        # Recover new data
        db.refresh(record)

        # Convert from model to schema
        disabled_customer = PaymentsSchema(
            id=record.id, customer_id=record.customer_id, amount=record.amount, status=record.status
        )

        response.body = disabled_customer
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.patch("/enable/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def enable_customer(id: int, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate record existence
        record = db.query(PaymentsORM).where(PaymentsORM.id == id).first()

        if record is None:
            raise Exception("Record not found")

        # Record restoration
        record.status = True

        # Update record on DB
        db.commit()

        # Recover new data
        db.refresh(record)

        # Convert from model to schema
        enabled_customer = PaymentsSchema(
            id=record.id, customer_id=record.customer_id, amount=record.amount, status=record.status
        )

        response.body = enabled_customer
    except Exception as exc:
        response.errors = str(exc)

    return response
