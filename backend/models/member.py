from pydantic import BaseModel

class Member(BaseModel):
    """
    Pydantic Model to represent a 'member' of an Organization.

    This model is based on the `MemberEntity` model, which defines the shape
    of the `Member` database in the PostgreSQL database
    """

    id: int | None = None
    user_id: int | None = None
    organization_id: int | None = None
    term: str
    year: str | None = None
    description: str | None = None
    isLeader: bool
    position: str | None = "Member"
    major: str | None = None
    minor: str | None = None
