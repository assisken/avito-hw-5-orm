from pytest import fixture
from lib import orm


@fixture
def init_db():
    db = orm.Database(':memory:')
    db.connect()

    yield db

    db.close()
