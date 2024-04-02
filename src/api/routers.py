from fastapi import APIRouter

from api.healthcheck.endpoints import router as healthcheck_endpoints
from api.v1.customers.endpoints import router as customer_endpoints
from api.v1.loans.endpoints import router as loan_endpoints
from api.v1.payments.endpoints import router as payments_endpoints
from core.settings import settings

healthcheck_router = APIRouter()
healthcheck_router.include_router(healthcheck_endpoints)

api_v1_router = APIRouter(prefix=f"/{settings.API_V1}")
api_v1_router.include_router(customer_endpoints)
api_v1_router.include_router(loan_endpoints)
api_v1_router.include_router(payments_endpoints)
