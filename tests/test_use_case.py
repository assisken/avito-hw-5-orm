from lib import orm

db = orm.Database(":memory:")
db.connect()


class BaseModel(orm.Model):
    class Meta:
        database = db


class Advert(BaseModel):
    title = orm.CharField(max_length=180)
    price = orm.IntegerField(min_value=0)


db.create_tables([Advert])


def test_use_case():
    Advert.create(title="iPhone X", price=100)
    adverts = Advert.select()

    assert str(adverts[0]) == "iPhone X | 100"
