"""
The Applicant Service allows the API to manipulate applicant data in the database.
"""

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.entities.organization_entity import OrganizationEntity
from backend.entities.applicant_entity import ApplicantEntity
from backend.entities.user_entity import UserEntity
from backend.models.applicant_details import ApplicantDetails
from backend.models.applicant import Applicant, ApplicantStatus
from backend.models.organization import Organization
from backend.models.organization_details import OrganizationDetails


from backend.models.user import User
from backend.services.exceptions import ResourceNotFoundException
from ..database import db_session
from ..entities.applicant_entity import ApplicantEntity


class ApplicantService:
    """Service that performs all of the actions on the 'Applicant' table"""

    def __init__(self, session: Session = Depends(db_session)):
        """Initializes the `ApplicantService` session"""
        self._session = session

    def get_applicants_of_organization(
        self, organization: OrganizationDetails
    ) -> list[ApplicantDetails]:
        """
        Retrieves all of the applicants of an organization

        Parameters: organization (OrganizationDetails): Organization to retrieve members of

        Returns:
            list[ApplicationDetails]: List of all `Applicants`

        Raises:
            ResourceNotFoundException if no organization is found with the corresponding slug
        """

        # Ensure organization exists
        org = (
            self._session.query(OrganizationEntity).where(
                OrganizationEntity.id == organization.id
            )
        ).one_or_none()
        if not org:
            raise ResourceNotFoundException(
                f"No organization with id {organization.id} exists."
            )

        # Get applications
        applicant_entities = (
            self._session.query(ApplicantEntity)
            .where(ApplicantEntity.organization_id == organization.id)
            .where(
                ApplicantEntity.status == ApplicantStatus.PENDING
            )  ### May want to do all and have frontend filter
            .all()
        )

        return [entity.to_model() for entity in applicant_entities]

    def get_applicant_by_id(self, id: int) -> ApplicantDetails:
        """
        Retrieves an applicant based on its id

        Parameters:
            id: the id of the applicant

        Returns:
            Application: Object with corresponding id

        Raises:
            ResourceNotFoundException if no applicant is found with the corresponding id
        """
        applicant = (
            self._session.query(ApplicantEntity)
            .where(ApplicantEntity.id == id)
            .one_or_none()
        )

        if not applicant:
            raise ResourceNotFoundException(f"No applicant with matching ID: {id}")

        return applicant.to_model()

    def get_user_applications(self, subject: User) -> list[ApplicantDetails]:
        """Gets all applications associated with a user."""

        user = (
            self._session.query(UserEntity).where(
                UserEntity.id == subject.id
            )
        ).one_or_none()
        if not user:
            raise ResourceNotFoundException(
                f"No uesr with id {subject.id} exists."
            )

        applicant_entities = (
            self._session.query(ApplicantEntity)
            .where(ApplicantEntity.user_id == subject.id)
            .all()
        )

        return [entity.to_model() for entity in applicant_entities]

    def add_applicant_of_organization(
        self, subject: User, organization: OrganizationDetails, application: Applicant
    ) -> ApplicantDetails:
        """
        Adds application to the given organization to the database
        If the applicant's ID is unique to the table, a new entry is added.
        If the applicant's ID already exists in the table, it raises an error.

        Parameters:
            subject: a valid User model representing the currently logged in User
            organization (OrganizationDetails): Organization to retrieve members of
            application (Applicant): Applicant to add to table

        Returns:
            ApplicantDetails: Add application object

        Raises:
            HTTPException: If the user has already applied to the organization
        """

        applicant_entities = (
            self._session.query(ApplicantEntity)
            .where(ApplicantEntity.organization_id == organization.id)
            .where(ApplicantEntity.user_id == subject.id)
            .all()
        )

        if applicant_entities:
            raise HTTPException(
                status_code=400, detail="Already applied to organization."
            )

        new_applicant = ApplicantEntity(
            user_id=subject.id,
            organization_id=organization.id,
            status=application.status,
            name=application.name,
            email=application.email,
            major=application.major,
            minor=application.minor,
            year=application.year,
            pronouns=application.pronouns,
            interest=application.interest,
        )

        self._session.add(new_applicant)
        self._session.commit()

        return new_applicant.to_model()

    def update_applicant_of_organization(
        self, id: int, application: Applicant
    ) -> ApplicantDetails:
        """
        Updates an existing application in the database

        Parameters:
            id: an int representing the id of the application to be updated
            application (Applicant): Applicant to add to table

        Returns:
            ApplicantDetails: Updated application object

        Raises:
            ResourceNotFoundException: If no applicant is found with the corresponding id
        """
        app = (
            self._session.query(ApplicantEntity)
            .where(ApplicantEntity.id == id)
            .one_or_none()
        )

        if app is None:
            raise ResourceNotFoundException(f"No applicant with id {id} exists.")

        app.status = application.status
        app.name = application.name
        app.major = application.major
        app.minor = application.minor
        app.year = application.year
        app.pronouns = application.pronouns
        app.interest = application.interest

        self._session.commit()

        return app.to_model()

    def remove_applicant_of_organization(self, subject: User, id: int):
        """
        Removes an application from the organization

        Parameters:
            subject: a valid User model representing the currently logged in User
            id: an int representing the id of the application to be removed

        Raises:
            ResourceNotFoundException: If no applicant is found with the corresponding id
        """
        app = (
            self._session.query(ApplicantEntity)
            .where(ApplicantEntity.id == id)
            .one_or_none()
        )

        if app is None:
            raise ResourceNotFoundException("No applicant with this id exists")

        self._session.delete(app)
        self._session.commit()
