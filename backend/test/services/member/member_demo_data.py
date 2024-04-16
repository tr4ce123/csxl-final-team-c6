from ....entities.member_entity import MemberEntity
import pytest
from sqlalchemy.orm import Session
from ..user_data import user, ambassador, leader, mark, tammy, vicky
from ..organization.organization_demo_data import cads, cssg
from ....models.member import MemberYear
from ..reset_table_id_seq import reset_table_id_seq

larry_cads = MemberEntity(
    id=2,
    user_id=leader.id,
    organization_id=cads.id,
    year=MemberYear.JUNIOR,
    description="My name is Larry and I am a Junior Computer Science Major.",
    isLeader=True,
    position="President",
    major="Computer Science",
    minor="Astronomy",
)

mark_cads = MemberEntity(
    id=3,
    user_id=mark.id,
    organization_id=cads.id,
    year=MemberYear.JUNIOR,
    description="My name is Mark and I am a Junior Computer Science Major.",
    isLeader=False,
    position=None,
    major="Computer Science",
    minor="Data Science",
)

mark_cssg = MemberEntity(
    id=4,
    user_id=mark.id,
    organization_id=cssg.id,
    year=MemberYear.JUNIOR,
    description="My name is Mark and I am a Junior Computer Science Major.",
    isLeader=False,
    position=None,
    major="Computer Science",
    minor="Data Science",
)

tammy_cads = MemberEntity(
    id=6,
    user_id=tammy.id,
    organization_id=cads.id,
    year=MemberYear.SENIOR,
    description="My name is Tammy and I am a Senior Computer Science Major.",
    isLeader=False,
    position="Treasurer",
    major="Computer Science",
    minor="Statistics",
)

vicky_cads = MemberEntity(
    id=7,
    user_id=vicky.id,
    organization_id=cads.id,
    year=MemberYear.GRAD,
    description="My name is Tammy and I am a Graduate Student Studying Computer Science.",
    isLeader=True,
    position="Vice President",
    major="Computer Science",
    minor=None,
)

amy_cssg = MemberEntity(
    id=8,
    user_id=ambassador.id,
    organization_id=cssg.id,
    year=MemberYear.SENIOR,
    description="My name is Tammy and I am a Senior Computer Science Major.",
    isLeader=True,
    position="President",
    major="Computer Science",
    minor=None,
)


members = [
    larry_cads,
    mark_cads,
    mark_cssg,
    tammy_cads,
    vicky_cads,
    amy_cssg,
]


def insert_fake_data(session: Session):
    """Inserts fake member data into the test session."""

    global members

    # Create entities for test member data
    entities = []
    for member_entity in members:
        session.add(member_entity)
        entities.append(member_entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, MemberEntity, MemberEntity.id, len(members) + 1)

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
