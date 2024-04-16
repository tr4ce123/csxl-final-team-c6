"""
The Applicant Service allows the API to manipulate applicant data in the database.
"""

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from backend.entities.organization_entity import OrganizationEntity
from backend.entities.applicant_entity import ApplicantEntity
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
        self._session = session

    def get_applicants_of_organization(
        self, organization: OrganizationDetails
    ) -> list[ApplicantDetails]:
        """Gets all pending applicants of an organization."""

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
        """Gets application by its unique id."""
        applicant = (
            self._session.query(ApplicantEntity)
            .where(ApplicantEntity.id == id)
            .one_or_none()
        )

        if not applicant:
            raise ResourceNotFoundException("No applicant with this ID found.")

        return applicant.to_model()

    def add_applicant_of_organization(
        self, subject: User, organization: OrganizationDetails, application: Applicant
    ) -> ApplicantDetails:
        """Adds application to the given organization to the database."""
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
        Updates application in the database
        Only takes in Applicant because can't change the user_id or org_id
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
        """Removes application."""
        app = (
            self._session.query(ApplicantEntity)
            .where(ApplicantEntity.id == id)
            .one_or_none()
        )

        if app is None:
            raise ResourceNotFoundException("No applicant with this id exists")

        self._session.delete(app)
        self._session.commit()