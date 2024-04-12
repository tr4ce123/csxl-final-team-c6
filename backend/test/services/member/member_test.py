"""Tests for the MemberService class."""

# PyTest
from fastapi import HTTPException
import pytest
from unittest.mock import create_autospec

from backend.models.member_details import MemberDetails
from backend.services.exceptions import (
    ResourceNotFoundException,
)

# Tested Dependencies
from backend.services.member import MemberService
from backend.services.organization import OrganizationService
from backend.services.user import UserService

# Injected Service Fixtures
from backend.test.services.fixtures import member_svc_integration
from backend.test.services.fixtures import organization_svc_integration
from backend.test.services.fixtures import user_svc_integration

from backend.test.services.core_data import setup_insert_data_fixture


# Data Models for Fake Data Inserted in Setup
from backend.test.services.member.member_test_data import (
    sally_cads,
    to_add_cssg,
    updated_sally_cads,
)


# Test Functions

# Test 'MemberService.get_members_of_organization()'


def test_get_members_of_organization(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
):
    """Test that all members of a given organization can be retrieved."""
    organization = organization_svc_integration.get_by_slug("cads")
    fetched_members = member_svc_integration.get_members_of_organization(organization)
    assert fetched_members is not None
    assert len(fetched_members) == 2
    assert isinstance(fetched_members[0], MemberDetails)


# Test 'MemberService.get_member_by_id()'


def test_get_member_by_id(member_svc_integration: MemberService):
    """Test that members can be retrieved based on their ID."""
    fetched_member = member_svc_integration.get_member_by_id(1)
    assert fetched_member is not None
    assert isinstance(fetched_member, MemberDetails)
    assert fetched_member.id == sally_cads.id

def test_get_member_by_id_does_not_exist(member_svc_integration: MemberService):
    """Test that you cannot retrieve a member with an ID that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        member_svc_integration.get_member_by_id(10000)


# Test 'MemberService.add_member()'


def test_add_member(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
    user_svc_integration: UserService,
):
    """Test that a member is able to be created."""
    user = user_svc_integration.get_by_id(3)
    organization = organization_svc_integration.get_by_slug("cssg")
    created_member = member_svc_integration.add_member(user, organization)
    assert created_member is not None
    assert created_member.id is not None
    assert created_member.organization_id is not None
    assert created_member.user_id is not None


def test_add_member_already_exists(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
    user_svc_integration: UserService,
):
    """Test that a member cannot be created if it already exists."""
    user = user_svc_integration.get_by_id(3)
    organization = organization_svc_integration.get_by_slug("cads")
    with pytest.raises(HTTPException):
        member_svc_integration.add_member(user, organization)


# Test 'MemberService.remove_member()'


def test_remove_member(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
    user_svc_integration: UserService,
):
    """Test that a member is able to be deleted."""
    user = user_svc_integration.get_by_id(3)
    organization = organization_svc_integration.get_by_slug("cads")
    member_svc_integration.remove_member(user, organization)
    with pytest.raises(ResourceNotFoundException):
        member_svc_integration.get_member_by_id(1)


def test_remove_member_does_not_exist(
    member_svc_integration: MemberService,
    organization_svc_integration: OrganizationService,
    user_svc_integration: UserService,
):
    """Test removing a member that does not exist"""
    user = user_svc_integration.get_by_id(3)
    organization = organization_svc_integration.get_by_slug("cssg")
    with pytest.raises(ResourceNotFoundException):
        member_svc_integration.remove_member(user, organization)

# Test 'MemberService.update_member()'


def test_update_member(
    member_svc_integration: MemberService,
):
    """Test that a member is properly updated."""
    member_svc_integration.update_member(updated_sally_cads)
    assert member_svc_integration.get_member_by_id(1).isLeader == True


def test_update_member_does_not_exist(member_svc_integration: MemberService):
    """Test updating a member that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        member_svc_integration.update_member(to_add_cssg)