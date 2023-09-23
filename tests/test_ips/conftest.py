import pytest

from src.ips.models import FloatingIP, Instance


@pytest.fixture
def db_with_instances_and_ips(db_empty_sync):
    session = db_empty_sync

    session.add(Instance(id=1, role="master"))
    session.add(Instance(id=2, role="master"))
    session.add(Instance(id=3, role="replica"))
    session.add(Instance(id=4, role="sync"))

    session.add(FloatingIP(ip="1.1", role="master"))
    session.add(FloatingIP(ip="1.2", role="master"))
    session.add(FloatingIP(ip="1.3", role="replica"))
    session.add(FloatingIP(ip="1.4", role="sync"))

    session.commit()
    return session
