"""Tests for the ApplicantService class."""

# PyTest
from fastapi import HTTPException
import pytest

from backend.models.applicant import ApplicantStatus
from backend.models.applicant_details import ApplicantDetails
from backend.services.exceptions import (
    ResourceNotFoundException,
)

# Tested Dependencies
from backend.services.organization import OrganizationService
from backend.services.user import UserService
from backend.services import ApplicantService

# Injected Service Fixtures
from backend.test.services.fixtures import applicant_svc_integration
from backend.test.services.fixtures import organization_svc_integration
from backend.test.services.fixtures import user_svc_integration

from backend.test.services.core_data import setup_insert_data_fixture


# Data Models for Fake Data Inserted in Setup
from backend.test.services.applicant.applicant_test_data import (
    sally_cads,
    amy_cads,
    to_add_cssg,
    to_update_cads,
    bad_org,
)


# Test Functions


def test_get_applicants_of_organization(
    applicant_svc_integration: ApplicantService,
    organization_svc_integration: OrganizationService,
):
    """Test that all applicants of a given organization can be retrieved."""
    organization = organization_svc_integration.get_by_slug("cads")
    applicants = applicant_svc_integration.get_applicants_of_organization(organization)
    assert applicants is not None
    assert len(applicants) == 2
    assert isinstance(applicants[0], ApplicantDetails)


def test_get_applicants_of_organization_does_not_exist(
    applicant_svc_integration: ApplicantService,
):
    """Test that you cannot retrieve applicants for a non-existing organization."""
    with pytest.raises(ResourceNotFoundException):
        applicant_svc_integration.get_applicants_of_organization(bad_org)


def test_get_applicant_by_id(applicant_svc_integration: ApplicantService):
    """Test that applicants can be retrieved based on their ID"""
    applicant = applicant_svc_integration.get_applicant_by_id(1)
    assert applicant
    assert isinstance(applicant, ApplicantDetails)
    assert applicant.id == sally_cads.id


def test_get_applicant_by_id_does_not_exist(
    applicant_svc_integration: ApplicantService,
):
    """Test that you cannot retrieve an applicant with an ID that does not exist."""
    with pytest.raises(ResourceNotFoundException):
        applicant_svc_integration.get_applicant_by_id(1000)


def test_add_applicant(
    applicant_svc_integration: ApplicantService,
    organization_svc_integration: OrganizationService,
    user_svc_integration: UserService,
):
    """Test that an applicant is able to be created."""
    user = user_svc_integration.get_by_id(3)
    organization = organization_svc_integration.get_by_slug("cssg")
    applicant = applicant_svc_integration.add_applicant_of_organization(
        user, organization, to_add_cssg
    )
    assert applicant
    assert applicant.id
    assert applicant.organization_id == organization.id
    assert applicant.user_id == user.id


def test_add_applicant_already_exists(
    applicant_svc_integration: ApplicantService,
    organization_svc_integration: OrganizationService,
    user_svc_integration: UserService,
):
    """Test that an applicant cannot be created if it already exists."""
    user = user_svc_integration.get_by_id(3)
    organization = organization_svc_integration.get_by_slug("cads")
    with pytest.raises(HTTPException):
        applicant = applicant_svc_integration.add_applicant_of_organization(
            user, organization, sally_cads
        )


def test_update_applicant(applicant_svc_integration: ApplicantService):
    """Test that an applicant is able to be updated."""
    app = applicant_svc_integration.update_applicant_of_organization(1, to_update_cads)
    assert app
    assert app.id == sally_cads.id
    assert app.user_id == sally_cads.user_id
    assert app.organization_id == sally_cads.organization_id
    assert app.name == sally_cads.name
    assert app.year == sally_cads.year
    assert app.major == sally_cads.major
    assert app.minor == sally_cads.minor
    assert app.pronouns == sally_cads.pronouns
    assert app.interest == sally_cads.interest
    # Check status was updated
    assert app.status == ApplicantStatus.ACCEPTED


def test_update_not_exists(applicant_svc_integration: ApplicantService):
    """Test that updating a non-existing application fails."""
    with pytest.raises(ResourceNotFoundException):
        applicant_svc_integration.update_applicant_of_organization(
            10000, to_update_cads
        )


def test_remove_applicant(
    applicant_svc_integration: ApplicantService,
    user_svc_integration: UserService,
):
    """Test that an applicant is able to be deleted."""
    user = user_svc_integration.get_by_id(3)
    applicant_svc_integration.remove_applicant_of_organization(user, 1)
    with pytest.raises(ResourceNotFoundException):
        applicant_svc_integration.get_applicant_by_id(1)


def test_remove_applicant_that_does_not_exist(
    applicant_svc_integration: ApplicantService,
    user_svc_integration: UserService,
):
    """Test that an applicant that does not exist is not able to be deleted."""
    user = user_svc_integration.get_by_id(3)
    with pytest.raises(ResourceNotFoundException):
        applicant = applicant_svc_integration.remove_applicant_of_organization(
            user, 100000
        )
