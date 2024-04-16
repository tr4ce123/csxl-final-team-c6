from backend.entities.applicant_entity import ApplicantEntity
from ....models.applicant import ApplicantStatus
import pytest
from sqlalchemy.orm import Session
from backend.test.services.user_data import user, ambassador, leader
from backend.test.services.organization.organization_demo_data import cads, cssg
from backend.test.services.reset_table_id_seq import reset_table_id_seq


sally_cads = ApplicantEntity(
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

sally_cssg = ApplicantEntity(
    id=2,
    user_id=user.id,
    organization_id=cssg.id,
    status=ApplicantStatus.PENDING,
    name=f"{user.first_name} {user.last_name}",
    email=user.email,
    major="Computer Science",
    minor=None,
    year="Sophomore",
    pronouns="she/her",
    interest="I really like cssg",
)

amy_cads = ApplicantEntity(
    id=3,
    user_id=ambassador.id,
    organization_id=cads.id,
    status=ApplicantStatus.PENDING,
    name=f"{ambassador.first_name} {ambassador.last_name}",
    email=ambassador.email,
    major="Computer Science",
    minor="Stats",
    year="Senior",
    pronouns="they/them",
    interest="I want to join",
)

amy_cssg = ApplicantEntity(
    id=4,
    user_id=ambassador.id,
    organization_id=cssg.id,
    status=ApplicantStatus.ACCEPTED,
    name=f"{ambassador.first_name} {ambassador.last_name}",
    email=ambassador.email,
    major="Computer Science",
    minor="Stats",
    year="Senior",
    pronouns="they/them",
    interest="I want to join",
)

larry_cssg = ApplicantEntity(
    id=5,
    user_id=leader.id,
    organization_id=cssg.id,
    status=ApplicantStatus.REJECTED,
    name=f"{leader.first_name} {leader.last_name}",
    email=leader.email,
    major="Math",
    minor="Music",
    year="Freshman",
    pronouns="she/her",
    interest="I really really want to join cssg",
)

applicants = [sally_cads, sally_cssg, amy_cads, amy_cssg, larry_cssg]


def insert_fake_data(session: Session):
    """Inserts fake member data into the test session."""

    global applicants

    # Create entities for test applicant data
    entities = []
    for applicant in applicants:
        session.add(applicant)
        entities.append(applicant)

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
