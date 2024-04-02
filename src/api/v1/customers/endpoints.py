from fastapi import APIRouter, status, Response, Depends, HTTPException, Query
from fastapi_pagination.ext.sqlalchemy import paginate
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from core.utils.exceptions import *

from api.v1.customers.schemas import CustomerSchema
from core.utils.responses import PaginationParams, default_pagination_params, EnvelopeResponse
from db.models import CustomerORM
from db.session import get_session

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/retrieve/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def retrieve_customer(id: int = 0, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        customer = db.query(CustomerORM).filter(CustomerORM.id == id).first()

        if customer is None:
            raise Exception("Record not found")

        result = CustomerSchema(
            id=customer.id, full_name=customer.full_name, email=customer.email, status=customer.status
        )

        response.body = result

    except Exception as exc:
        response.errors = str(exc)

    return response


@router.get("/list", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def list_customers(
        filter: str = '', status: bool = Query(True), db: Session = Depends(get_session),
        params: PaginationParams = Depends(default_pagination_params)
    ):
    response = EnvelopeResponse()

    try:
        customers = db.query(CustomerORM).order_by(CustomerORM.id).filter(CustomerORM.status == status)

        if filter != '':
            customers = customers.filter(
                CustomerORM.full_name.ilike(f'%{filter}%') | CustomerORM.email.ilike(f'%{filter}%')
            )

        # Working but not receiving query params to alter amounts
        records = paginate(customers, params=params)

        # Convert models to schemas
        result = [CustomerSchema(**item.dict()) for item in records.items]

        response.body = result
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=EnvelopeResponse)
async def create_customer(customer: CustomerSchema, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate parameters' content
        if customer.full_name is None or customer.email is None:
            raise Exception("Missing parameter")

        # Validate email format
        email = validate_email(customer.email, check_deliverability=False)

        # Validate email unique record
        validation = select(CustomerORM).filter(CustomerORM.email == email.normalized)
        already_registered = db.execute(validation).first()

        if already_registered:
            raise Exception("Email already registered")

        # Generate customer record
        new_record = CustomerORM(full_name=customer.full_name, email=email.normalized)

        # Insert new record
        db.add(new_record)
        db.commit()

        # Recover new data
        db.refresh(new_record)

        # Convert from model to schema
        new_customer = CustomerSchema(
            id=new_record.id, full_name=new_record.full_name, email=new_record.email, status=new_record.status
        )

        response.body = new_customer
    except EmailNotValidError:
        response.errors = "Invalid email address"
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.put("/update", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def update_customer(customer: CustomerSchema, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate record existence
        record = db.query(CustomerORM).filter(CustomerORM.id == customer.id).first()

        if record is None:
            raise Exception("Record not found")

        # Validate email format
        email = validate_email(customer.email, check_deliverability=False)

        # Validate email duplication
        duplicated = db.query(func.count(CustomerORM.email)).filter(CustomerORM.email == email.normalized).scalar()

        if duplicated > 1:
            raise Exception("Email already registered")

        # Change customer data
        if customer.full_name is not None:
            record.full_name = customer.full_name

        if customer.email is not None:
            record.email = email.normalized

        # Update record on DB
        db.commit()

        # Recover new data
        db.refresh(record)

        # Convert from model to schema
        updated_customer = CustomerSchema(
            id=record.id, full_name=record.full_name, email=record.email, status=record.status
        )

        response.body = updated_customer
    except EmailNotValidError:
        response.errors = "Invalid email address"
    except Exception as exc:
        response.errors = str(exc)

    return response


@router.delete("/delete/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def delete_customer(id: int, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate record existence
        record = db.query(CustomerORM).filter(CustomerORM.id == id).first()

        if record is None:
            raise Exception("Record not found")

        # Physical deletion
        db.delete(record)

        # Update record on DB
        db.commit()

        # Convert from model to schema
        deleted_customer = CustomerSchema(
            id=record.id, full_name=record.full_name, email=record.email, status=False
        )

        response.body = deleted_customer
    except Exception as exc:
        response.errors = str(exc)
    finally:
        db.close()

    return response


@router.delete("/disable/{id}", status_code=status.HTTP_200_OK, response_model=EnvelopeResponse)
async def disable_customer(id: int, db: Session = Depends(get_session)):
    response = EnvelopeResponse()

    try:
        # Validate record existence
        record = db.query(CustomerORM).filter(CustomerORM.id == id).first()

        if record is None:
            raise Exception("Record not found")

        # Logical deletion
        record.status = False

        # Update record on DB
        db.commit()

        # Recover new data
        db.refresh(record)

        # Convert from model to schema
        disabled_customer = CustomerSchema(
            id=record.id, full_name=record.full_name, email=record.email, status=record.status
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
        record = db.query(CustomerORM).filter(CustomerORM.id == id).first()

        if record is None:
            raise Exception("Record not found")

        # Record restoration
        record.status = True

        # Update record on DB
        db.commit()

        # Recover new data
        db.refresh(record)

        # Convert from model to schema
        enabled_customer = CustomerSchema(
            id=record.id, full_name=record.full_name, email=record.email, status=record.status
        )

        response.body = enabled_customer
    except Exception as exc:
        response.errors = str(exc)

    return response
