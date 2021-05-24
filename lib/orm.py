import sqlite3
from abc import ABC, abstractmethod
from typing import Dict, List, Type, Optional, Any, Callable

from funcy import first

from .util import camel_to_snake_case


class Database:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self._con = None

    def connect(self):
        self._con = sqlite3.Connection(self.database_name)

    def close(self):
        self._con.close()

    def create_tables(self, models: List[Type["Model"]]):
        with self._con:
            for model in models:
                table_fields = ",".join(
                    f"{name} {field_type.sql_type}"
                    for name, field_type in model._get_model_fields().items()
                )

                # 1. I think it's safe.
                # You can't declare class "'; drop database foo; --" in python.
                # 2. No way to pass variables into create table statement.
                self._con.execute(
                    "create table if not exists "
                    f"{model._get_table_name()}({table_fields})"
                )


class Field(ABC):
    @classmethod
    def EMPTY_CHECK(cls):
        return True

    def __init__(self, **constraints: Callable[[Any], bool]):
        self._constraints = constraints

    @property
    @abstractmethod
    def sql_type(self) -> str:
        pass

    def validate(self, data):
        for constraint, check in self._constraints.items():
            if not check(data):
                raise ValidationError(
                    f'Constraint mismatch: {type(self).__name__} {constraint} for value "{data}"'
                )


class ModelManager:
    def __init__(self, model: Type["Model"]):
        self.model = model

    def create(self, **fields) -> Type["Model"]:
        self._validate_fields(**fields)

        row = tuple(value for _, value in fields.items())
        values = ",".join("?" for _ in range(len(row)))

        self.model.Meta.database._con.execute(
            f"insert into {self.model._get_table_name()} values ({values})", row
        )
        return self.model(**fields)

    def select(self, **fields) -> list:
        def make_row(row):
            init_fields = {field: row for field, row in zip(self.model._get_model_fields(), row)}
            self._validate_fields(**init_fields)
            return self.model(**init_fields)

        cond = "and ".join(f"{f}='{v}'" for f, v in fields.items())
        where = f'where {cond}' if fields else ''
        rows = self.model.Meta.database._con.execute(
            f"select * from {self.model._get_table_name()} {where}"
        )
        return [make_row(row) for row in rows]

    def _validate_fields(self, **fields):
        model_fields = self.model._get_model_fields()
        for field_name, value in fields.items():
            model_fields[field_name].validate(value)


class Meta:
    pass


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        attrs['Meta'] = attrs.get('Meta') or mcs.get_parent_attribute('Meta', bases) or Meta()

        _class: Type["Model"] = super().__new__(mcs, name, bases, attrs)
        _class.objects = attrs.get('objects') or ModelManager(_class)

        return _class

    @staticmethod
    def get_parent_attribute(attr: str, bases) -> Any:
        return first(getattr(base, attr) for base in bases if hasattr(base, 'Meta'))


class Model(metaclass=ModelMeta):
    objects: "ModelManager"

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        fields = ", ".join(f"{k}={v}" for k, v in self._get_instance_fields().items())
        return f"{type(self).__name__}({fields})"

    def __str__(self):
        return ' | '.join(str(v) for _, v in self._get_instance_fields().items())

    def __eq__(self, other: "Model"):
        return self._get_instance_fields() == other._get_instance_fields()

    @classmethod
    def _get_table_name(cls):
        return camel_to_snake_case(cls.__name__)

    @classmethod
    def _get_model_fields(cls) -> Dict[str, Field]:
        return {
            field_name: field
            for field_name, field in vars(cls).items()
            if not field_name.startswith("_") and isinstance(field, Field)
        }

    def _get_instance_fields(self) -> Dict[str, Any]:
        return {k: v for k, v in vars(self).items() if not k.startswith("_")}


class ValidationError(Exception):
    pass


class IntegerField(Field):
    sql_type = "integer"

    def __init__(self, min_value: Optional[int] = None):
        super().__init__(
            min_value=lambda data: min_value <= data if min_value is not None else self.EMPTY_CHECK,
        )


class CharField(Field):
    sql_type = "text"

    def __init__(self, max_length: Optional[int] = None, min_length: Optional[int] = None):
        super().__init__(
            min_length=lambda data: min_length <= len(data) if min_length is not None else self.EMPTY_CHECK,
            max_length=lambda data: len(data) <= max_length if max_length is not None else self.EMPTY_CHECK,
        )
