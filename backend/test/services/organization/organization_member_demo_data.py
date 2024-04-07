from backend.models.member import Member
from backend.models.member_details import MemberDetails
from backend.models.user import User
from ....entities.member_entity import MemberEntity
import pytest
from sqlalchemy.orm import Session
from ..user_data import user, ambassador, leader
from ..organization.organization_demo_data import cads, cssg
from ..reset_table_id_seq import reset_table_id_seq

sally_cads = MemberEntity(
    user_id = user.id,
    organization_id = cads.id,
    year = 2026,
    description = "My name is Sally and I am a Sophomore Computer Science Major.",
    isLeader = False
)

sally_cssg = MemberEntity(
    user_id = user.id,
    organization_id = cssg.id,
    year = 2026,
    description = "My name is Amy and I am a Senior Computer Science Major.",
    isLeader = False
)

amy_cads = MemberEntity(
    user_id = ambassador.id,
    organization_id = cads.id,
    year = 2024,
    description = "My name is Amy and I am a Senior Computer Science Major. I am the VP of CADS.",
    isLeader = True
)

amy_cssg = MemberEntity(
    user_id = ambassador.id,
    organization_id = cssg.id,
    year = 2024,
    description = "My name is Amy and I am a Senior Computer Science Major. I am the Treasurer for CSSG.",
    isLeader = True
)

larry_cssg = MemberEntity(
    user_id = leader.id,
    organization_id = cssg.id,
    year = 2025,
    description = "My name is Larry and I am a Junior Computer Science Major. I am the President of CSSG.",
    isLeader = True
)



members = [sally_cads, sally_cssg, amy_cads, amy_cssg, larry_cssg]

def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global members

    # Create entities for test member data
    entities = []

    for member_entity in members:
        session.add(member_entity)
        entities.append(member_entity)

    session.add(member_entity)


    # # Reset table IDs to prevent ID conflicts
    # reset_table_id_seq(
    #     session, MemberEntity, MemberEntity.id, len(members) + 1
    # )

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
