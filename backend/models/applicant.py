from enum import Enum
from pydantic import BaseModel


class ApplicantStatus(Enum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = -1


class Applicant(BaseModel):
    """
    Pydantic Model to represent an 'applicant' of an Organization.

    This model is based on the `MemberEntity` model, which defines the shape
    of the `Member` database in the PostgreSQL database
    """

    id: int
    user_id: int | None = None
    organization_id: int | None = None
    status: ApplicantStatus
    name: str
    email: str
    major: str
    minor: str | None = None
    year: str
    pronouns: str
    interest: str
