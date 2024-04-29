from ....entities.member_entity import MemberEntity
import pytest
from sqlalchemy.orm import Session
from ..user_data import ambassador, leader, mark, tammy, vicky, morgan
from ..organization.organization_demo_data import (
    acm,
    cads,
    cssg,
)
from ..reset_table_id_seq import reset_table_id_seq

larry_cads = MemberEntity(
    id=1,
    user_id=leader.id,
    organization_id=cads.id,
    term="Spring 2024",
    year="Junior",
    description="My name is Larry and I am a Junior Computer Science Major.",
    isLeader=True,
    position="President",
    major="Computer Science",
    minor="Astronomy",
)

mark_cads = MemberEntity(
    id=2,
    user_id=mark.id,
    organization_id=cads.id,
    term="Spring 2024",
    year="Junior",
    description="My name is Mark and I am a Junior Computer Science Major.",
    isLeader=False,
    position=None,
    major="Computer Science",
    minor="Data Science",
)

mark_cssg = MemberEntity(
    id=3,
    user_id=mark.id,
    organization_id=cssg.id,
    term="Spring 2024",
    year="Junior",
    description="My name is Mark and I am a Junior Computer Science Major.",
    isLeader=False,
    position=None,
    major="Computer Science",
    minor="Data Science",
)

tammy_cads = MemberEntity(
    id=4,
    user_id=tammy.id,
    organization_id=cads.id,
    term="Spring 2024",
    year="Junior",
    description="My name is Tammy and I am a Senior Computer Science Major.",
    isLeader=False,
    position="Treasurer",
    major="Computer Science",
    minor="Statistics",
)

vicky_cads = MemberEntity(
    id=5,
    user_id=vicky.id,
    organization_id=cads.id,
    term="Spring 2024",
    year="Graduate",
    description="My name is Vicky and I am a Graduate Student Studying Computer Science.",
    isLeader=True,
    position="Vice President",
    major="Computer Science",
    minor=None,
)

amy_cssg = MemberEntity(
    id=6,
    user_id=ambassador.id,
    organization_id=cssg.id,
    term="Spring 2024",
    year="Senior",
    description="My name is Amy and I am a Senior Computer Science Major.",
    isLeader=True,
    position="President",
    major="Computer Science",
    minor=None,
)

amy_cssg_2023 = MemberEntity(
    id=7,
    user_id=ambassador.id,
    organization_id=cssg.id,
    term="Fall 2023",
    year="Senior",
    description="My name is Amy and I am a Senior Computer Science Major.",
    isLeader=False,
    position=None,
    major="Computer Science",
    minor=None,
)

morgan_acm = MemberEntity(
    id=8,
    user_id=morgan.id,
    organization_id=acm.id,
    term="Spring 2024",
    year="Senior",
    description="My name is Morgan and I am a Sophomore CS Major.",
    isLeader=False,
    position=None,
    major="Biology",
    minor="CS",
)

vicky_acm_F2023 = MemberEntity(
    id=9,
    user_id=vicky.id,
    organization_id=acm.id,
    term="Fall 2023",
    year="Graduate",
    description="My name is Vicky and I am a Graduate Student Studying Computer Science.",
    isLeader=False,
    position=None,
    major="Computer Science",
    minor=None,
)

mark_cads_F2023 = MemberEntity(
    id=10,
    user_id=mark.id,
    organization_id=cads.id,
    term="Fall 2023",
    year="Junior",
    description="My name is Mark and I am a Junior Computer Science Major.",
    isLeader=True,
    position="Vice President",
    major="Computer Science",
    minor="Data Science",
)

members = [
    larry_cads,
    mark_cads,
    mark_cssg,
    tammy_cads,
    vicky_cads,
    amy_cssg,
    amy_cssg_2023,
    morgan_acm,
    vicky_acm_F2023,
    mark_cads_F2023,
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
