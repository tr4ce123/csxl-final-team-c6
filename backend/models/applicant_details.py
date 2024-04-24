from backend.models.applicant import Applicant
from backend.models.organization import Organization
from backend.models.user import User

class ApplicantDetails(Applicant):
    """
    Pydantic model to represent an `Applicant`.

    This model is based on the `ApplicantEntity` model, which defines the shape
    of the `Applicant` database in the PostgreSQL database.
    """

    user: User
    organization: Organization