"""Definition of SQLAlchemy table-backed object mapping entity for Members."""

from typing import Self
from sqlalchemy import Integer, String, Boolean, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from backend.models.member import Member
from backend.models.member_details import MemberDetails
from backend.models.member import MemberYear
from .entity_base import EntityBase


class MemberEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Member` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "member"

    # Organization properties (columns in the database table)

    # Unique ID for the Member Entity
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # These fields establish a foreign keys and relationship fields for a many-to-many relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user: Mapped["UserEntity"] = relationship(back_populates="members")

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organization.id"), primary_key=True
    )
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="members")

    # Academic Term
    term: Mapped[str] = mapped_column(String, nullable=False, default="")

    # Year of the student
    year: Mapped[MemberYear] = mapped_column(SQLAlchemyEnum(MemberYear), nullable=False)

    # Description of the student
    description: Mapped[str] = mapped_column(String, nullable=True, default="")

    # Is the member a leader in the organization
    isLeader: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # String description of a members role ie President, Treasurer, etc.
    position: Mapped[str] = mapped_column(String, nullable=True, default="Member")

    # Member major
    major: Mapped[str] = mapped_column(String, nullable=False)

    # Member minor
    minor: Mapped[str] = mapped_column(String, nullable=True)

    def to_model(self) -> Member:
        """
        Converts a 'Member Entity' object into a 'Member' model object

        Returns:
            Member: 'Member' object from the entity
        """

        return Member(
            id=self.id,
            user_id=self.user_id,
            organization_id=self.organization_id,
            term=self.term,
            year=self.year,
            description=self.description,
            isLeader=self.isLeader,
            position=self.position,
            major=self.major,
            minor=self.minor,
        )

    def to_details_model(self) -> MemberDetails:

        return MemberDetails(
            id=self.id,
            user_id=self.user_id,
            organization_id=self.organization_id,
            year=self.year,
            term=self.term,
            description=self.description,
            isLeader=self.isLeader,
            position=self.position,
            major=self.major,
            minor=self.minor,
            user=self.user.to_model(),
            organization=self.organization.to_model(),
        )

    @classmethod
    def from_model(cls, model: Member) -> Self:
        """
        Class method converts a 'Member' model into a 'MemberEntity'

        Parameters:
            - model (Member): Model to convert to an entity
        Returns:
            MemberEntity: Entity created from model
        """

        return cls(
            id=model.id,
            user_id=model.user_id,
            organization_id=model.organization_id,
            term=model.term,
            year=model.year,
            description=model.description,
            isLeader=model.isLeader,
            position=model.position,
            major=model.major,
            minor=model.minor,
        )
