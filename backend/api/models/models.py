from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re


class ProfileSubscription(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sum: float = Field(..., gt=0)
    currency: str = Field(default="RUB", pattern=r'^[A-Z]{3}$')
    return_url: str = Field(..., min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)

    @field_validator('return_url')
    @classmethod
    def validate_return_url(cls, v: str) -> str:
        if not v.startswith(('http://', 'https://')):
            raise ValueError('return_url must start with http:// or https://')
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('пустое имя')
        return v.strip()


class RefundProfileSubscription(BaseModel):
    sum: float = Field(..., gt=0)
    currency: str = Field(default="RUB", pattern=r'^[A-Z]{3}$')
    id_operations: str = Field(..., min_length=1)

    @field_validator('id_operations')
    @classmethod
    def validate_id_operations(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('id_operations не может быть пустым')
        return v.strip()