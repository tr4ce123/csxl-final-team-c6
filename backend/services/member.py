"""
The Member Service allows the API to manipulate member data in the database.
"""

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.entities.organization_entity import OrganizationEntity
from backend.entities.user_entity import UserEntity
from backend.models.member_details import MemberDetails
from backend.models.organization import Organization
from backend.models.public_user import PublicUser

from backend.models.user import User
from ..database import db_session
from ..entities.member_entity import MemberEntity
from ..models.member import Member
from ..models.organization_details import OrganizationDetails

class MemberService:
    """Service that performs all of the actions on the 'Members' table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        self._session = session


    def get_members_of_organization(
        self, organization: OrganizationDetails
    ) -> list[MemberDetails]:

        """
        Retrieves all of the members of an organization 

        Parameters:
            organization (OrganizationDetails): Organization to retrieve members of

        Returns:
            list[MemberDetails]: List of all 'Member Details' that matches the organization's id 
        """
        
        # Query the member with matching organization slug
        member_entities = (
            self._session.query(MemberEntity)
            .where(MemberEntity.organization_id == organization.id)
            .all()
        )

        return [entity.to_details_model() for entity in member_entities]

    def get_organizations_for_user(
        self, subject: User | None = None
    ) -> list[Organization]:

        """
        Retrieves all of the organizations a user is a part of  

        Parameters:
            subject: a valid User model representing the currently logged in user

        Returns:
            list[Organization]: List of all 'Organizations' that matches the organization's id 
        """

        organization_entities = (
            self._session.query(OrganizationEntity)
            .where(MemberEntity.user_id == subject.id)
            .all()
        )

        return [entity.to_model() for entity in organization_entities]

    def add_member_to_organization(
        self, user_id: int, organization_id: int, year: int, description: str = "", isLeader: bool = False 
    ) -> Member:

        existing_member = (
            self._session.query(MemberEntity)
            .filter_by(user_id=user_id, organization_id=organization_id)
            .first()
        )
        if existing_member:
            raise HTTPException(status_code=400, detail="User is already a member of this organization.")

        new_member = MemberEntity(
            user_id=user_id,
            organization_id=organization_id,
            year=year,
            description=description,
            isLeader=isLeader
        )

        self._session.add(new_member)
        self._session.commit()

        return new_member.to_model()

