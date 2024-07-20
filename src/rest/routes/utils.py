from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from uuid import UUID
import json

from models import Apps, State


async def get_kind(uuid: UUID, db: Session):
    kind = db.query(Apps).filter(Apps.uuid == uuid).first()
    if kind and isinstance(kind.json, str):
        kind.json = json.loads(kind.json)

    return kind


async def delete_kind(kind: Apps, db: Session):
    db.delete(kind)
    db.commit()


async def update_kind_state(new_state: State, kind: Apps, db: Session) -> State:
    kind.state = new_state
    db.commit()
    db.refresh(kind)

    return kind.state


async def update_kind(new_kind: Apps, db: Session):
    flag_modified(new_kind, "json")
    db.commit()
    db.refresh(new_kind)

    return new_kind
