from fastapi import APIRouter, Depends, HTTPException
from backend.models.applicant import Applicant
from backend.models.applicant_details import ApplicantDetails
from backend.models.organization import Organization
from backend.models.user import User

from backend.services.organization import OrganizationService
from backend.services.user import UserService
from backend.services.applicant import ApplicantService
from ..api.authentication import registered_user


api = APIRouter(prefix="/api/applicants")
openapi_tags = {
    "name": "Applicants",
    "description": "Add, remove applicants of Organizations.",
}


@api.get("/{slug}", response_model=list[ApplicantDetails], tags=["Applicants"])
def get_organization_applicants(
    slug: str,
    organization_service: OrganizationService = Depends(),
    application_service: ApplicantService = Depends(),
) -> list[ApplicantDetails]:

    organization = organization_service.get_by_slug(slug)
    return application_service.get_applicants_of_organization(organization)


@api.get("/id/{id}", response_model=ApplicantDetails, tags=["Applicants"])
def get_organization_applicants_by_id(
    id: int,
    application_service: ApplicantService = Depends(),
) -> ApplicantDetails:

    return application_service.get_applicant_by_id(id)

@api.get("/applications/{user_id}", response_model=list[ApplicantDetails], tags=["Applicants"])
def get_user_applications(
    user_id: int,
    application_service: ApplicantService = Depends(),
    user_service: UserService = Depends()
) -> list[ApplicantDetails]:

    user = user_service.get_by_id(user_id)
    return application_service.get_user_applications(user)


@api.post("/{slug}", response_model=ApplicantDetails, tags=["Applicants"])
def new_applicant(
    slug: str,
    application: Applicant,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
    applicant_service: ApplicantService = Depends(),
) -> ApplicantDetails:

    organization = organization_service.get_by_slug(slug)
    return applicant_service.add_applicant_of_organization(
        subject, organization, application
    )


@api.put("/{id}", response_model=ApplicantDetails, tags=["Applicants"])
def update_applicant(
    id: int, application: Applicant, applicant_service: ApplicantService = Depends()
):
    return applicant_service.update_applicant_of_organization(id, application)


@api.delete("/{id}", response_model=None, tags=["Applicants"])
def delete_applicant(
    id: int,
    subject: User = Depends(registered_user),
    applicant_service: ApplicantService = Depends(),
):
    applicant_service.remove_applicant_of_organization(subject, id)
