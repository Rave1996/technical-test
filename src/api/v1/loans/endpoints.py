from fastapi import APIRouter, status, Response, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from api.v1.loans.schemas import LoanSchema
from core.utils.responses import PaginationParams, default_pagination_params, EnvelopeResponse
from db.models import CustomerORM, LoanORM
from db.session import get_session

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get("/retrieve/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def retrieve_loan(id: int = 0, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        loan = db.query(LoanORM).filter(LoanORM.id == id).first()

        if loan is None:
            raise Exception("Record not found")

        result = LoanSchema(
            id=loan.id, customer_id=loan.customer_id, amount=loan.amount, status=loan.status
        )

        response.body = result
    except Exception as exc:
        response.errors = str(exc)

    return response


# to check
@router.get("/list", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def list_customers(filter: str = '', status: bool = True, db: Session = Depends(get_session),
                         params: PaginationParams = Depends(default_pagination_params)):
    response = EnvelopeResponse()

    try:
        loans = db.query(LoanORM).join(CustomerORM).order_by(LoanORM.id).filter(CustomerORM.status == status)

        if filter != '':
            loans = loans.filter(
                CustomerORM.full_name.ilike(f'%{filter}%') | CustomerORM.email.ilike(f'%{filter}%')
            )

        # Working but not receiving query params to alter amounts
        records = paginate(loans, params=params)

        # Convert models to schemas
        result = [LoanSchema(**item.dict()) for item in records.items]

        response.body = result
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=EnvelopeResponse)
async def create_loan(loan: LoanSchema, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate customer account existence
        customer = db.query(CustomerORM).filter(CustomerORM.id == loan.customer_id).first()

        if customer is None:
            raise Exception("Customer not found")

        # Validate parameters' content
        if loan.customer_id is None or loan.amount is None:
            raise Exception("Missing parameter")

        # Generate customer record
        new_loan = LoanORM(customer_id=loan.customer_id, amount=loan.amount)

        # Insert new record
        db.add(new_loan)
        db.commit()

        # Recover new data
        db.refresh(new_loan)

        # Convert from model to schema
        new_loan = LoanSchema(
            id=new_loan.id, customer_id=new_loan.customer_id, amount=new_loan.amount, status=new_loan.status
        )

        response.body = new_loan
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def delete_loan(id: int, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate record existence
        record = db.query(LoanORM).where(LoanORM.id == id).first()

        if record is None:
            raise Exception("Record not found")

        # Physical deletion
        db.delete(record)

        # Update record on DB
        db.commit()

        # Convert from model to schema
        deleted_customer = LoanSchema(
            id=record.id, customer_id=record.customer_id, amount=record.amount, status=record.status
        )

        response.body = deleted_customer
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.delete("/disable/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def disable_loan(id: int, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate record existence
        record = db.query(LoanORM).where(LoanORM.id == id).first()

        if record is None:
            raise Exception("Record not found")

        # Logical deletion
        record.status = False

        # Update record on DB
        db.commit()

        # Recover new data
        db.refresh(record)

        # Convert from model to schema
        disabled_customer = LoanSchema(
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
        record = db.query(LoanORM).where(LoanORM.id == id).first()

        if record is None:
            raise Exception("Record not found")

        # Record restoration
        record.status = True

        # Update record on DB
        db.commit()

        # Recover new data
        db.refresh(record)

        # Convert from model to schema
        enabled_customer = LoanSchema(
            id=record.id, customer_id=record.customer_id, amount=record.amount, status=record.status
        )

        response.body = enabled_customer
    except Exception as exc:
        response.errors = str(exc)

    return response
