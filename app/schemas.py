from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    phone: PhoneNumber
    email: EmailStr
    comment: str = Field(..., min_length=5)


class ContactResponse(BaseModel):
    message: str


class MetricsResponse(BaseModel):
    total_requests: int
    positive: int
    neutral: int
    negative: int
    unknown: int
