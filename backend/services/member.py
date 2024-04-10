"""
The Member Service allows the API to manipulate member data in the database.
"""

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.entities.organization_entity import OrganizationEntity
from backend.models.member_details import MemberDetails
from backend.models.organization import Organization

from backend.models.user import User
from backend.services.exceptions import ResourceNotFoundException
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

    def get_member_by_id(
        self, id: int
    ) -> MemberDetails:
        """
        Retrieves a member based on its id 

        Parameters:
            id: the id of the member

        Returns:
            MemberDetails
        """

        member_entity =(
            self._session.query(MemberEntity)
            .filter(MemberEntity.id == id)
            .one_or_none()
        )

        # Check if result is null
        if member_entity is None:
            raise ResourceNotFoundException(f"No Member Entity found with matching ID: {id}")

        return member_entity.to_details_model()

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

    def add_member(
        self, subject: User, organization: Organization
    ) -> MemberDetails:
        """
        Creates a Member that acts as a relationship between a User and an Organization they want to join

        Parameters:
            subject: a valid User model representing the currently logged in user
            organization: the organization the user is becoming a member of

        Returns:
            MemberDetails
        """

        # If the member entity already exists for the given user and organization, raise an error
        existing_member = (
            self._session.query(MemberEntity)
            .filter_by(user_id=subject.id, organization_id=organization.id)
            .one_or_none()
        )

        if existing_member:
            raise HTTPException(status_code=400, detail="User is already a member of this organization.")

        member_entity = MemberEntity(
            user_id = subject.id,
            organization_id = organization.id,
            year = 0,
            description = "Default",
            isLeader = False
        )

        self._session.add(member_entity)
        self._session.commit()

        return member_entity.to_details_model()

    def remove_member(
        self, subject: User, organization: Organization
    ) -> None:
        """
        Removes a member from an organization

        Parameters:
            subject: a valid User model representing the currently logged in user
            organization: the organization the user is becoming a member of

        Returns:
            None
        """

        member_entity = (
            self._session.query(MemberEntity)
            .filter_by(user_id=subject.id, organization_id=organization.id)
            .one_or_none()
        )

        # If the member doesn't exist, raise exception
        if member_entity is None:
            raise ResourceNotFoundException

        self._session.delete(member_entity)
        self._session.commit()

    def update_member(
        self, member: Member
    ) -> Member:
        """
        Update the member's information

        Parameters:
            member: a valid Member

        Returns:
            Member
        """
        
        member_entity = (
            self._session.query(MemberEntity)
            .filter(MemberEntity.id == member.id)
            .one_or_none()
        )

        # If the member doesn't exist, raise exception
        if member_entity is None:
            raise ResourceNotFoundException

        member_entity.year = member.year
        member_entity.description = member.description
        member_entity.isLeader = member.isLeader
        member_entity.position = member.position
        member_entity.major = member.major
        member_entity.minor = member.minor


        self._session.commit()

        return member_entity.to_model()