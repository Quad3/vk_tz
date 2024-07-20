import uuid as uuid_pkg
import json

from typing import Annotated
from fastapi import APIRouter, Depends, File, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_db

from rest.models.{{ kind }}.model import Model as Kind_model, Configuration, Settings, Specification
from models import Apps, State
from rest.routes import utils


router = APIRouter(
    prefix="/{{ kind }}",
    tags=["{{ kind }}"]
)


@router.post("", status_code=201, response_model=uuid_pkg.UUID)
async def create_kind(file: Annotated[bytes, File()], db: Session = Depends(get_db)):
    try:
        kind_model = Kind_model.parse_raw(file)
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()})
        )

    kind_model_dict = kind_model.dict()
    kind_model_dict.pop("configuration")

    new_kind = Apps(**kind_model_dict)
    new_kind.uuid = uuid_pkg.uuid4()

    new_kind.json = json.loads(file)

    db.add(new_kind)
    db.commit()

    return new_kind.uuid


@router.put("/{uuid}/configuration", response_model=Kind_model)
async def update_kind_configuration(uuid: str, configuration: Configuration, db: Session = Depends(get_db)):

    update_configuration_encoded = jsonable_encoder(configuration)

    try:
        Settings.parse_obj(update_configuration_encoded["settings"])
        Specification.parse_obj(update_configuration_encoded["specification"])
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()})
        )

    kind = await utils.get_kind(uuid=uuid_pkg.UUID(uuid), db=db)

    kind.json['configuration']['settings'] = update_configuration_encoded["settings"]
    kind.json['configuration']['specification'] = update_configuration_encoded["specification"]

    kind = await utils.update_kind(new_kind=kind, db=db)

    return {
        "kind": kind.kind,
        "name": kind.name,
        "description": kind.description,
        "version": kind.version,
        "configuration": kind.json["configuration"]
    }


@router.put("/{uuid}/settings", response_model=Kind_model)
async def update_kind_settings(uuid: str, settings: Settings, db: Session = Depends(get_db)):

    update_settings_encoded = jsonable_encoder(settings)

    try:
        Settings.parse_obj(update_settings_encoded)
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()})
        )

    kind = await utils.get_kind(uuid=uuid_pkg.UUID(uuid), db=db)

    kind.json['configuration']['settings'] = update_settings_encoded

    kind = await utils.update_kind(new_kind=kind, db=db)
    kind.configuration = kind.json["configuration"]

    return {
        "kind": kind.kind,
        "name": kind.name,
        "description": kind.description,
        "version": kind.version,
        "configuration": kind.json["configuration"]
    }


@router.put("/{uuid}/state", response_model=State)
async def update_kind_state(uuid: str, state: State, db: Session = Depends(get_db)):

    kind = await utils.get_kind(uuid=uuid_pkg.UUID(uuid), db=db)
    if kind is None:
        raise HTTPException(status_code=404, detail="Does not exist")

    new_state = await utils.update_kind_state(kind=kind, new_state=state, db=db)

    return new_state


@router.delete("/{uuid}")
async def delete_kind(uuid: str, db: Session = Depends(get_db)) -> None:

    kind = await utils.get_kind(uuid=uuid_pkg.UUID(uuid), db=db)
    if kind is None:
        raise HTTPException(status_code=404, detail="Does not exist")

    await utils.delete_kind(kind=kind, db=db)

    return None


@router.get("/{uuid}", response_model=Kind_model)
async def get_kind(uuid: str, db: Session = Depends(get_db)):

    kind = await utils.get_kind(uuid=uuid_pkg.UUID(uuid), db=db)
    if kind is None:
        raise HTTPException(status_code=404, detail="Does not exist")

    return {
        "kind": kind.kind,
        "name": kind.name,
        "description": kind.description,
        "version": kind.version,
        "configuration": kind.json["configuration"]
    }


@router.get("/{uuid}/state", response_model=State)
async def get_kind_state(uuid: str, db: Session = Depends(get_db)):

    kind = await utils.get_kind(uuid=uuid_pkg.UUID(uuid), db=db)
    if kind is None:
        raise HTTPException(status_code=404, detail="Does not exist")

    return kind.state
