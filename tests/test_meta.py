from lib import orm


class ParentModel(orm.Model):
    class Meta:
        db = 'foo'


def test_meta_was_overrited():
    class OverrideMeta(ParentModel):
        class Meta:
            db = 'bar'

    assert OverrideMeta.Meta.db == 'bar'


def test_meta_was_not_overrited():
    class InheritMeta(ParentModel):
        pass

    assert InheritMeta.Meta.db == 'foo'
