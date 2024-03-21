from pydantic import BaseModel


class HealthCheckSchema(BaseModel):
    detail: str
    version: str
