"Contains mock data to run tests on the applicant feature"

import pytest
from sqlalchemy.orm import Session

from backend.api import user
from backend.models.organization import Organization
from backend.test.services.reset_table_id_seq import reset_table_id_seq
from backend.models.applicant import Applicant, ApplicantStatus
from backend.entities.applicant_entity import ApplicantEntity
from backend.test.services.organization.organization_test_data import cads, cssg
from backend.test.services.user_data import user, ambassador


sally_cads = Applicant(
    id=1,
    user_id=user.id,
    organization_id=cads.id,
    status=ApplicantStatus.PENDING,
    name=f"{user.first_name} {user.last_name}",
    email=user.email,
    major="Computer Science",
    minor=None,
    year="Sophomore",
    pronouns="she/her",
    interest="I really like cads",
)

amy_cads = Applicant(
    id=2,
    user_id=ambassador.id,
    organization_id=cads.id,
    status=ApplicantStatus.PENDING,
    name=f"{user.first_name} {user.last_name}",
    email=user.email,
    major="Computer Science",
    minor="Stats",
    year="Senior",
    pronouns="they/them",
    interest="I want to join",
)

applicants = [sally_cads, amy_cads]

to_add_cssg = Applicant(
    id=3,
    user_id=user.id,
    organization_id=cssg.id,
    status=ApplicantStatus.ACCEPTED,
    name=f"{user.first_name} {user.last_name}",
    email=user.email,
    major="Computer Science",
    minor=None,
    year="Sophomore",
    pronouns="she/her",
    interest="I really like cssg",
)

# Identical to sally_cads except it's been accepted
to_update_cads = Applicant(
    id=1,
    user_id=user.id,
    organization_id=cads.id,
    status=ApplicantStatus.ACCEPTED,
    name=f"{user.first_name} {user.last_name}",
    email=user.email,
    major="Computer Science",
    minor=None,
    year="Sophomore",
    pronouns="she/her",
    interest="I really like cads",
)

bad_org = Organization(
    id=1000,
    name="Bad Not Existing Org",
    shorthand="BNEO",
    slug="NON_EXISTING_ORG",
    logo="none",
    short_description="none",
    long_description="none",
    website="none",
    email="none",
    instagram="none",
    linked_in="none",
    youtube="none",
    heel_life="none",
    public=False,
    org_type=1,  # Application-Based but doesn't matter
)


def insert_fake_data(session: Session):
    """Inserts fake applicant data into the test session."""

    global applicants

    # Create entities for test applicant data
    entities = []
    for applicant in applicants:
        applicant_entity = ApplicantEntity.from_model(applicant)
        session.add(applicant_entity)
        entities.append(applicant_entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session, ApplicantEntity, ApplicantEntity.id, len(applicants) + 1
    )

    # Commit all changes
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when test is run.
    Note:
        This function runs automatically due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield
