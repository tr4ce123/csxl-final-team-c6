"""Definition of SQLAlchemy table-backed object mapping entity for Members."""

from typing import Self
from sqlalchemy import Integer, String, Boolean, Enum
import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from backend.models.applicant import Applicant, ApplicantStatus
from backend.models.applicant_details import ApplicantDetails
from backend.models.organization import Organization
from backend.models.user import User
from .entity_base import EntityBase


class ApplicantEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Member` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "applicant"

    # Organization properties (columns in the database table)

    # Primary key for the applicant table
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    # These fields establish a foreign keys and relationship fields for a one-to-many relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserEntity"] = relationship(back_populates="applicants")

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))
    organization: Mapped["OrganizationEntity"] = relationship(
        back_populates="applicants"
    )

    # Status of application (Pending, Accepted, Rejected)
    status: Mapped[ApplicantStatus] = mapped_column(
        Enum(ApplicantStatus), nullable=False
    )

    # Name of the applicant
    name: Mapped[str] = mapped_column(String)

    # Email of the applicant
    email: Mapped[str] = mapped_column(String)

    # Major of the applicant
    major: Mapped[str] = mapped_column(String)

    # Minor of the Applicant
    minor: Mapped[str] = mapped_column(String, nullable=True)

    # Year of the applicant
    year: Mapped[str] = mapped_column(String)

    # Pronoun(s) of applicant
    pronouns: Mapped[str] = mapped_column(String)

    # Interest of the applicant
    interest: Mapped[str] = mapped_column(String)

    def to_model(self) -> ApplicantDetails:

        return ApplicantDetails(
            id=self.id,
            user_id=self.user_id,
            organization_id=self.organization_id,
            status=self.status,
            name=self.name,
            email=self.email,
            major=self.major,
            minor=self.minor,
            year=self.year,
            pronouns=self.pronouns,
            interest=self.interest,
            user=self.user.to_model(),
            organization=self.organization.to_model(),
        )

    @classmethod
    def from_model(cls, model: Applicant) -> Self:
        """
        Class method converts a 'Member' model into a 'MemberEntity'

        Parameters:
            - model (Applicant): Model to convert to an entity
        Returns:
            ApplicantEntity: Entity created from model
        """

        return cls(
            id=model.id,
            user_id=model.user_id,
            organization_id=model.organization_id,
            status=model.status,
            name=model.name,
            email=model.email,
            major=model.major,
            minor=model.minor,
            year=model.year,
            pronouns=model.pronouns,
            interest=model.interest,
        )
