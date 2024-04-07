from backend.models.member import Member
from backend.models.organization import Organization
from backend.models.user import User


class MemberDetails(Member):
    """
    Pydantic model to represent a `Member`.

    This model is based on the `MemberEntity` model, which defines the shape
    of the `Member` database in the PostgreSQL database.
    """

    user: User
    organization: Organization
    
