from pydantic import BaseModel
from .user import User
from .organization import Organization

class Member(BaseModel):
    """
        Pydantic Model to represent a 'member' of an Organization.

        This model is based on the `MemberEntity` model, which defines the shape
        of the `Member` database in the PostgreSQL database
    """

    user_id: int
    organization_id: int
    year: int
    description: str
    isLeader: bool
    user: User
    organization: Organization