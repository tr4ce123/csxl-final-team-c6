"""Definition of SQLAlchemy table-backed object mapping entity for Members."""

from typing import Self
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from backend.models.member import Member
from .entity_base import EntityBase

class MemberEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Member` table"""

    # Name for the organizations table in the PostgreSQL database
    __tablename__ = "member"

    # Organization properties (columns in the database table)

    # These fields establish a foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primarykey=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"), primarykey=True)

    # Year of the student
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    # Description of the student
    description: Mapped[str] = mapped_column(String, nullablle=True, default="")

    #Is the member a leader in the organization
    isLeader: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    #Relationship fields
    user: Mapped["UserEntity"] = relationship(back_populates="member")
    organization: Mapped["OrganizationEntity"] = relationship(back_populates="member")


    def to_model(self) -> Member:
        """
        Converts a 'Member Entity' object into a 'Member' model object

        Returns: 
            Member: 'Member' object from the entity
        """

        return Member(
            user_id=self.user_id,
            organization_id=self.organization_id,
            year=self.year,
            description=self.description,
            isLeader=self.isLeader,
            user=self.user,
            organization=self.organization
        )

    @classmethod
    def from_model(cls, model: Member) -> Self:
        """
        Class method converts a 'Member' model into a 'MemberEntity'

        Parameters:
            - model (Member): Model to convert to an entity
        Returns:
            OrganizationEntity: Entity created from model
        """
        return cls(
            user_id=model.user_id,
            organization_id=model.organization_id,
            year=model.year,
            description=model.description,
            isLeader=model.isLeader,
            user=model.user,
            organization=model.organization
        )