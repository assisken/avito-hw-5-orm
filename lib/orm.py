import sqlite3
from abc import ABC, abstractmethod
from typing import Dict, List, Type, Optional, Any, Callable

from funcy import first

from .util import camel_to_snake_case


class Database:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.__con = None

    @property
    def _con(self) -> sqlite3.Connection:
        return self.__con

    @_con.setter
    def _con(self, value: sqlite3.Connection):
        self.__con = value

    def connect(self):
        self._con = sqlite3.Connection(self.database_name)

    def close(self):
        self._con.close()

    def create_tables(self, models: List[Type["Model"]]):
        with self._con:
            for model in models:
                table_fields = ",".join(
                    f"{name} {field_type.sql_type}"
                    for name, field_type in model._get_fields().items()
                )

                # 1. I think it's safe.
                # You can't declare class "'; drop database foo; --" in python.
                # 2. No way to pass variables into create table statement.
                self._con.execute(
                    "create table if not exists "
                    f"{model._get_table_name()}({table_fields})"
                )


class Row:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        fields = ", ".join(f"{k}={v}" for k, v in self.__get_fields().items())
        return f"{type(self).__name__}({fields})"

    def __str__(self):
        return ' | '.join(str(v) for _, v in self.__get_fields().items())

    def __eq__(self, other: "Row"):
        return self.__get_fields() == other.__get_fields()

    def __get_fields(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


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


class Meta:
    pass


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        meta = first(base.Meta for base in bases if hasattr(base, 'Meta'))
        attrs['Meta'] = attrs.get('Meta') or meta or Meta()
        return type.__new__(mcs, name, bases, attrs)


class Model(metaclass=ModelMeta):
    _table_name = ""

    @classmethod
    def create(cls, **fields) -> "Model":
        cls._validate_fields(**fields)
        row = tuple(value for _, value in fields.items())
        values = ",".join("?" for _ in range(len(row)))
        cls.Meta.database._con.execute(
            f"insert into {cls._get_table_name()} values ({values})", row
        )
        return Row(**fields)

    @classmethod
    def select(cls, **fields) -> List["Model"]:
        def make_row(row):
            init_fields = {field: row for field, row in zip(cls._get_fields(), row)}
            cls._validate_fields(**init_fields)
            return Row(**init_fields)

        cond = "and ".join(f"{f}='{v}'" for f, v in fields.items())
        where = f'where {cond}' if fields else ''
        rows = cls.Meta.database._con.execute(
            f"select * from {cls._get_table_name()} {where}"
        )
        return [make_row(row) for row in rows]

    @classmethod
    def _get_table_name(cls):
        if cls._table_name:
            return cls._table_name
        return camel_to_snake_case(cls.__name__)

    @classmethod
    def _get_fields(cls) -> Dict[str, Field]:
        return {
            field_name: field
            for field_name, field in vars(cls).items()
            if not field_name.startswith("_") and isinstance(field, Field)
        }

    @classmethod
    def _validate_fields(cls, **fields):
        model_fields = cls._get_fields()
        for field_name, value in fields.items():
            model_fields[field_name].validate(value)


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
