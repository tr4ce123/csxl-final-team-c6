"""
The Member Service allows the API to manipulate member data in the database.
"""

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.models.member_details import MemberDetails
from backend.models.organization import Organization

from backend.models.user import User
from backend.services.exceptions import ResourceNotFoundException
from ..database import db_session
from ..entities.member_entity import MemberEntity
from ..models.member import Member
from ..models.organization_details import OrganizationDetails

import datetime


def get_current_term() -> str:
    """Returns the current academic term in format "Term YYYY"."""
    ### Not sure how inefficient this is
    ### Realistically, it should be fine since members won't be added extremely consistently
    ### But still a consideration

    # Get current time
    now = datetime.datetime.now()

    # Check month. Map Jan-June -> Spring, July-Dec -> Fall
    # Maymester/Summer should not be necessary because organizations only update rosters in Spring/Fall (to our knowledge)
    if 1 <= now.month <= 6:
        term = "Spring"
    else:
        term = "Fall"

    return f"{term} {now.year}"


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

        # Query the members with matching organization slug
        member_entities = (
            self._session.query(MemberEntity)
            .where(MemberEntity.organization_id == organization.id)
            .all()
        )

        return [entity.to_details_model() for entity in member_entities]

    def get_members_of_organization_by_term(
        self, organization: OrganizationDetails, term: str
    ) -> list[MemberDetails]:
        """
        Retrieves all of the members of an organization for the given term

        Parameters:
            organization (OrganizationDetails): Organization to retrieve members of
            term: string in format "Spring YYYY" or "Fall YYYY"

        Returns:
            list[MemberDetails]: List of all 'Member Details' that matches the organization's id
        """

        # Query the members with matching organization slug
        member_entities = (
            self._session.query(MemberEntity)
            .where(MemberEntity.organization_id == organization.id)
            .where(MemberEntity.term == term)
            .all()
        )

        return [entity.to_details_model() for entity in member_entities]

    def get_user_memberships(self, subject: User) -> list[MemberDetails]:
        """
        Retrieves all of the member objects associated with a user

        Parameters:
            subject: A valid user

        Returns:
            list[MemberDetails]: List of all 'Member Details' that matches the users's id
        """

        member_entities = (
            self._session.query(MemberEntity)
            .where(MemberEntity.user_id == subject.id)
            .all()
        )

        return [entity.to_details_model() for entity in member_entities]

    def get_user_memberships_by_term(
        self, subject: User, term: str
    ) -> list[MemberDetails]:
        """
        Retrieves all of the member objects associated with a user by term

        Parameters:
            subject: A valid user
            term: string in format "Spring YYYY" or "Fall YYYY"

        Returns:
            list[MemberDetails]: List of all 'Member Details' that matches the users's id
        """

        member_entities = (
            self._session.query(MemberEntity)
            .where(MemberEntity.user_id == subject.id)
            .where(MemberEntity.term == term)
            .all()
        )

        return [entity.to_details_model() for entity in member_entities]

    def get_member_by_user_and_org(
        self, subject: User, organization: Organization
    ) -> MemberDetails:
        """
        Retrieves the member object if the user is a member of the organization this term.

        Parameters:
            subject: the user we are requesting
            organization: the organiztion we are requesting

        Returns:
            MemberDetails
        """
        # For permissions, If ROOT, create Leader Model
        if subject.id == 1:
            return MemberDetails(
                id=None,
                user_id=subject.id,
                organization_id=organization.id,
                year=None,
                term=get_current_term(),
                description=None,
                isLeader=True,
                position=None,
                major=None,
                minor=None,
                user=subject,
                organization=organization,
            )

        member_entity = (
            self._session.query(MemberEntity)
            .filter(MemberEntity.user_id == subject.id)
            .filter(MemberEntity.organization_id == organization.id)
            .filter(MemberEntity.term == get_current_term())
            .one_or_none()
        )

        # Check if result is null
        if member_entity is None:
            raise ResourceNotFoundException(
                f"User {subject.id} not a member of organization {organization.id}"
            )

        return member_entity.to_details_model()

    def get_member_by_id(self, id: int) -> MemberDetails:
        """
        Retrieves a member based on its id

        Parameters:
            id: the id of the member

        Returns:
            MemberDetails
        """

        member_entity = (
            self._session.query(MemberEntity)
            .filter(MemberEntity.id == id)
            .one_or_none()
        )

        # Check if result is null
        if member_entity is None:
            raise ResourceNotFoundException(
                f"No Member Entity found with matching ID: {id}"
            )

        return member_entity.to_details_model()

    def add_member(
        self, subject: User, organization: Organization, term: str
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
            .filter_by(user_id=subject.id, organization_id=organization.id, term=term)
            .one_or_none()
        )

        if existing_member:
            raise HTTPException(
                status_code=400, detail="User is already a member of this organization."
            )

        member_entity = MemberEntity(
            user_id=subject.id,
            organization_id=organization.id,
            term=term,
            year=None,
            description=None,
            isLeader=False,
            position=None,
            major=None,
            minor=None,
        )

        self._session.add(member_entity)
        self._session.commit()

        return member_entity.to_details_model()

    def remove_member(
        self, subject: User, organization: Organization, term: str
    ) -> None:
        """
        Removes a member from an organization

        Parameters:
            subject: a valid User model representing the currently logged in user
            organization: the organization the user is becoming a member of
            term: string in format "Spring YYYY" or "Fall YYYY"

        """

        member_entity = (
            self._session.query(MemberEntity)
            .filter_by(user_id=subject.id, organization_id=organization.id)
            .where(MemberEntity.term == term)
            .one_or_none()
        )

        # If the member doesn't exist, raise exception
        if member_entity is None:
            raise ResourceNotFoundException

        self._session.delete(member_entity)
        self._session.commit()

    def update_member(self, member: Member) -> Member:
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

        if (
            member_entity.user_id != member.user_id
            or member_entity.organization_id != member.organization_id
        ):
            raise HTTPException(
                status_code=400,
                detail="Attempt to change member entity's user or organization.",
            )

        # Do not allow updates to memberships in past terms
        # We think this is the right idea, but it's subject to change
        if member_entity.term != get_current_term():
            raise HTTPException(
                status_code=400,
                detail="Attempt to update member profile from previous term.",
            )

        member_entity.year = member.year
        member_entity.description = member.description
        member_entity.isLeader = member.isLeader
        member_entity.position = member.position
        member_entity.major = member.major
        member_entity.minor = member.minor

        self._session.commit()

        return member_entity.to_model()
