import enum
from sqlalchemy import Column, JSON, String, UUID
from sqlalchemy.types import Enum

from database import Base


class State(str, enum.Enum):
    NEW = "NEW"
    INSTALLING = "INSTALLING"
    RUNNING = "RUNNING"


class Apps(Base):
    __tablename__ = "apps"

    uuid = Column(UUID, primary_key=True)
    kind = Column(String(32), nullable=False)
    name = Column(String(128), nullable=False)
    version = Column(String, nullable=False)
    description = Column(String(4096))
    state = Column(Enum(State), default="NEW")
    json = Column(JSON, nullable=False)
