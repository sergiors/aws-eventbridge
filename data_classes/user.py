from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import constr

from .enums import ListEnum, StrEnum


class Status(ListEnum, StrEnum):
    CREATING = 'CREATING'
    CREATED = 'CREATED'
    CONFIRMED = 'CONFIRMED'
    UNCONFIRMED = 'UNCONFIRMED'
    COMPROMISED = 'COMPROMISED'


class User(BaseModel):
    class Config:
        validate_assignment = True

    id: constr(strip_whitespace=True)  # type: ignore
    name: str
    email: str
    cpf: Optional[str] = None
    mobile_number: Optional[str] = Field(alias='mobileNumber')
    email_deliverable: bool = Field(False, alias='emailDeliverable')
    email_verified: bool = Field(False, alias='emailVerified')
    status: Status = Status.CREATING
