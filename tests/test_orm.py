import pytest

from lib import orm
from pytest import fixture


class SimpleModel(orm.Model):
    name: str = orm.CharField(min_length=1, max_length=100)
    age: int = orm.IntegerField(min_value=0)


@fixture
def init_table(init_db):
    init_db.create_tables([SimpleModel])
    SimpleModel.Meta.database = init_db
    yield init_db._con


def test_create_table(init_table):
    with init_table:
        tables = init_table.execute(
            "select name from sqlite_master where type='table'"
        ).fetchall()

    assert tables == [("simple_model",)]


def test_insert_some_data(init_table):
    cur = init_table.cursor()
    cur.execute("insert into simple_model values (?, ?)", ("Amadeus", 24))
    records = cur.execute("select * from simple_model").fetchall()

    assert records == [("Amadeus", 24)]


def test_create(init_table):
    cur = init_table.cursor()
    amadeus = SimpleModel.create(name="Amadeus", age=24)
    records = cur.execute("select * from simple_model").fetchall()

    assert records == [("Amadeus", 24)]
    assert amadeus == orm.Row(name="Amadeus", age=24)


def test_select(init_table):
    cur = init_table.cursor()
    cur.execute(
        "insert into simple_model values (?, ?), (?, ?), (?, ?)",
        ("Amadeus", 24, "August", 33, "Amadeus", 36),
    )
    amadeuses = []
    for amad in SimpleModel.select(name="Amadeus"):
        amadeuses.append(amad)

    assert amadeuses[0].age == 24
    assert amadeuses[1].age == 36
    assert amadeuses == [
        orm.Row(name="Amadeus", age=24),
        orm.Row(name="Amadeus", age=36),
    ]


@pytest.mark.parametrize(
    'name, age',
    [
        ('', 1),
        ('a' * 101, 1),
        ('Amadeus' * 101, 0),
    ]
)
def test_validation(name, age, init_table):
    cur = init_table.cursor()
    cur.execute('insert into simple_model values (?, ?)', (name, age))

    with pytest.raises(orm.ValidationError):
        SimpleModel.create(name=name, age=age)

    with pytest.raises(orm.ValidationError):
        SimpleModel.select(age=age)
