import enum
from sqlalchemy import MetaData,Column, JSON, String, UUID
from sqlalchemy.types import Enum

from database import Base


metadata = MetaData()


class State(str, enum.Enum):
    NEW = "NEW"
    INSTALLING = "INSTALLING"
    RUNNING = "RUNNING"


class Apps(Base):
    __tablename__ = "apps"

    uuid = Column(UUID, primary_key=True)
    kind = Column(String, nullable=False)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    description = Column(String)
    state = Column(Enum(State), default="NEW")
    json = Column(JSON, nullable=False)
