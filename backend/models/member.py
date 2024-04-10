from enum import Enum
from pydantic import BaseModel

#Year enum
class MemberYear(Enum):
    FRESHMAN = 1
    SOPHOMORE = 2
    JUNIOR = 3
    SENIOR = 4
    FIFTH_YEAR = 5
    GRAD = 6

class Member(BaseModel):
    """
        Pydantic Model to represent a 'member' of an Organization.

        This model is based on the `MemberEntity` model, which defines the shape
        of the `Member` database in the PostgreSQL database
    """

    id: int | None = None
    user_id: int | None = None
    organization_id: int | None = None
    year: MemberYear
    description: str | None = None
    isLeader: bool
    position: str | None = "Member"
    major: str
    minor: str | None = None