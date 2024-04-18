"Contains mock data to run tests on the member feature"

import pytest
from sqlalchemy.orm import Session

from backend.api import user
from ..reset_table_id_seq import reset_table_id_seq
from ....models.member import Member, MemberYear
from ....entities.member_entity import MemberEntity
from ..organization.organization_test_data import cads, cssg
from ..user_data import user, ambassador


sally_cads = Member(
    id=1,
    user_id=user.id,
    organization_id=cads.id,
    term="Spring 2024",
    year=MemberYear.FRESHMAN,
    description="My name is Sally and I am a Freshman Computer Science Major.",
    isLeader=False,
    position=None,
    major="Computer Science",
    minor=None,
)

amy_cads = Member(
    id=2,
    user_id=ambassador.id,
    organization_id=cads.id,
    term="Spring 2023",
    year=MemberYear.SOPHOMORE,
    description="My name is Amy and I am a Sophomore Computer Science Major. I am the VP of CADS.",
    isLeader=True,
    position="Vice President",
    major="Computer Science",
    minor="Business Administration",
)

members = [sally_cads, amy_cads]

to_add_cssg = Member(
    user_id=user.id,
    organization_id=cssg.id,
    term="Fall 2023",
    year=MemberYear.FRESHMAN,
    description="My name is Amy and I am a Freshman Computer Science Major.",
    isLeader=False,
    position=None,
    major="Computer Science",
    minor=None,
)

updated_sally_cads = Member(
    id=1,
    user_id=user.id,
    organization_id=cads.id,
    term="Spring 2024",
    year=MemberYear.FRESHMAN,
    description="My name is Sally and I am a Freshman Computer Science Major.",
    isLeader=True,
    position=None,
    major="Computer Science",
    minor=None,
)

updated_amy_cads = Member(
    id=2,
    user_id=ambassador.id,
    organization_id=cads.id,
    term="Spring 2023",
    year=MemberYear.SOPHOMORE,
    description="My name is Amy and I am a Sophomore Computer Science Major. I am the VP of CADS.",
    isLeader=True,
    position="Vice President",
    major="Computer Science",
    minor="Stats",
)


def insert_fake_data(session: Session):
    """Inserts fake member data into the test session."""

    global members

    # Create entities for test member data
    entities = []
    for member in members:
        member_entity = MemberEntity.from_model(member)
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
