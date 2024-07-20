import enum
from sqlalchemy import MetaData, Table, Column, JSON, String, UUID
from sqlalchemy.types import Enum


metadata = MetaData()


class State(str, enum.Enum):
    NEW = "NEW"
    INSTALLING = "INSTALLING"
    RUNNING = "RUNNING"


apps = Table(
    "apps",
    metadata,
    Column("uuid", UUID, primary_key=True),
    Column("kind", String, nullable=False),
    Column("name", String, nullable=False),
    Column("version", String, nullable=False),
    Column("description", String),
    Column("state", Enum(State), default="NEW"),
    Column("json", JSON, nullable=False),
)
