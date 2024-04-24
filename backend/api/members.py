"""Members API

Member routes are used to add, remove, and update Members of Organizations."""

from fastapi import APIRouter, Depends
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
    member_service: MemberService = Depends(),
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


@api.get("/{slug}/{term}", response_model=list[MemberDetails], tags=["Members"])
def get_organization_members_by_term(
    slug: str,
    term: str,
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
) -> list[MemberDetails]:
    """
    Get the members of a specific organization by term.

    Args:
        slug: the slug of the organization
        term: academic term in form "Spring YYYY" or "Fall YYYY"
        organization_service: the service to query organizations
        member_service: the backing service

    Returns:
        list[MemberDetails]
    """

    organization = organization_service.get_by_slug(slug)
    return member_service.get_members_of_organization_by_term(organization, term)


@api.get("/id/id/{id}", response_model=MemberDetails, tags=["Members"])
def get_member_by_id(
    id: int, member_service: MemberService = Depends()
) -> MemberDetails:
    """
    Get a member by its ID

    Args:
        id: the ID of the member to get
        member_service: the backing service

    Returns:
        MemberDetails
    """

    return member_service.get_member_by_id(id)

@api.get(
    "/user/memberships/{user_id}", response_model=list[MemberDetails], tags=["Members"]
)
def get_user_memberships(
    user_id: int,
    member_service: MemberService = Depends(),
    user_service: UserService = Depends(),
) -> list[MemberDetails]:
    """
    Get all members associated with a user

    Args:
        user_id: the ID of the user to get the members of
        member_service: the backing service
        user_service: the backing service

    Returns:
        MemberDetails
    """

    user = user_service.get_by_id(user_id)
    return member_service.get_user_memberships(user)

@api.get(
    "/user/memberships/{user_id}/{term}", response_model=list[MemberDetails], tags=["Members"]
)
def get_user_memberships_by_term(
    user_id: int,
    term: str,
    member_service: MemberService = Depends(),
    user_service: UserService = Depends(),
) -> list[MemberDetails]:
    """
    Get all members associated with a user by term

    Args:
        user_id: the ID of the user to get the members of
        term: academic term in form "Spring YYYY" or "Fall YYYY"
        member_service: the backing service
        user_service: the backing service

    Returns:
        MemberDetails
    """

    user = user_service.get_by_id(user_id)
    return member_service.get_user_memberships_by_term(user, term)

@api.post("/{slug}/create/{user_id}/{term}", response_model=MemberDetails, tags=["Members"])
def add_member(
    slug: str,
    user_id: int,
    term: str,
    user_service: UserService = Depends(),
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
) -> MemberDetails:
    """
    Have a user become a member of an organization

    Args:
        slug: the slug of the organization
        user_id: the id of the user
        term: academic term in form "Spring YYYY" or "Fall YYYY"
        user_service: a valid User Service
        organization_service: a valid Organization Service
        member_service: the backing service

    Returns:
        list[MemberDetails]
    """

    user = user_service.get_by_id(user_id)
    organization: Organization = organization_service.get_by_slug(slug)

    return member_service.add_member(user, organization, term)


@api.delete("/{slug}/delete/{user_id}/{term}", response_model=None, tags=["Members"])
def remove_member(
    slug: str,
    user_id: int,
    term: str,
    user_service: UserService = Depends(),
    organization_service: OrganizationService = Depends(),
    member_service: MemberService = Depends(),
):
    """
    Remove a user from an organization

    Args:
        slug: the slug of the organization
        user_id: the id of the user
        term: academic term in form "Spring YYYY" or "Fall YYYY"
        user_service: a valid User Service
        organization_service: a valid Organization Service
        member_service: the backing service

    Returns:
        None
    """

    user = user_service.get_by_id(user_id)
    organization: Organization = organization_service.get_by_slug(slug)

    return member_service.remove_member(user, organization, term)


@api.put("", responses={404: {"model": None}}, response_model=Member, tags=["Members"])
def update_member(member: Member, member_service: MemberService = Depends()) -> Member:
    """
    Updates a member

    Args:
        member: the member to be updated
        member_service: the backing service

    Returns:
        Member
    """

    return member_service.update_member(member)
