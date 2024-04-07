"""Members API

Member routes are used to add, remove, and update Members of Organizations."""

from fastapi import APIRouter, Depends, HTTPException
from backend.models.member_details import MemberDetails
from backend.models.organization import Organization

from backend.services.organization import OrganizationService
from backend.services.user import UserService
from ..models.member import Member
from backend.services.member import MemberService

api = APIRouter(prefix="/api/members")
openapi_tags = {
    "name": "Members",
    "description": "Add, remove, and update Members of Organizations.",
}

@api.get("/{slug}", response_model=list[MemberDetails], tags=["Members"])
def get_organization_members(
    slug: str,
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends()
) -> list[MemberDetails]:
    """
    Get the members of a specific organization.

    Args:
        slug: the slug of the organization
        organization_service: the service to query organizations
        member_service: the backing service

    Returns:
        list[MemberDetails]
    """

    organization = organization_service.get_by_slug(slug)
    return member_service.get_members_of_organization(organization)