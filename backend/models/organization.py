from enum import Enum
from pydantic import BaseModel

__authors__ = ["Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class OrganizationType(Enum):
    """
    Determines the type of the organization.
    """

    OPEN = 0
    APP = 1
    CLOSED = 2


class Organization(BaseModel):
    """
    Pydantic model to represent an `Organization`.

    This model is based on the `OrganizationEntity` model, which defines the shape
    of the `Organization` database in the PostgreSQL database.
    """

    id: int | None = None
    name: str
    shorthand: str
    slug: str
    logo: str
    short_description: str
    long_description: str
    website: str
    email: str
    instagram: str
    linked_in: str
    youtube: str
    heel_life: str
    public: bool
    org_type: OrganizationType
