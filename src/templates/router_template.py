import uuid as uuid_pkg
import json

from typing import Annotated
from fastapi import APIRouter, Depends, File, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from database import get_async_session

from rest.models.{{ kind }}.model import Model as Kind_model, Configuration, Settings, Specification
from models import apps, State


router = APIRouter(
    prefix="/{{ kind }}",
    tags=["{{ kind }}"]
)


@router.post("", status_code=201, response_model=uuid_pkg.UUID)
async def create_kind(file: Annotated[bytes, File()], session: AsyncSession = Depends(get_async_session)):
    try:
        kind_model = Kind_model.model_validate_json(file)
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()})
        )

    new_kind = kind_model.dict()
    new_kind["uuid"] = uuid_pkg.uuid4()

    file = json.loads(file)
    new_kind["json"] = file

    response_object = new_kind.copy()
    response_object.pop("json")
    new_kind.pop("configuration")

    stmt = insert(apps).values(new_kind)
    await session.execute(stmt)
    await session.commit()

    return new_kind["uuid"]


@router.put("/{uuid}/configuration", response_model=Kind_model)
async def update_kind_configuration(
        uuid: str, configuration: Configuration, session: AsyncSession = Depends(get_async_session)):

    update_configuration_encoded = jsonable_encoder(configuration)

    try:
        Settings.model_validate(update_configuration_encoded["settings"])
        Specification.model_validate(update_configuration_encoded["specification"])
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()})
        )

    query = select(apps).where(apps.c.uuid == uuid_pkg.UUID(uuid))
    result = await session.execute(query)
    result = result.first()

    db_json = result[6]
    db_json['configuration']['settings'] = update_configuration_encoded["settings"]
    db_json['configuration']['specification'] = update_configuration_encoded["specification"]

    update_stmt = update(apps).where(apps.c.uuid == uuid_pkg.UUID(uuid)).values(json=db_json)
    await session.execute(update_stmt)
    await session.commit()

    return Kind_model(kind=result[1],
                      name=result[2],
                      version=result[3],
                      configuration=db_json["configuration"],
                      description=result[4])


@router.put("/{uuid}/settings", response_model=Kind_model)
async def update_kind_settings(uuid: str, settings: Settings, session: AsyncSession = Depends(get_async_session)):
    update_settings_encoded = jsonable_encoder(settings)

    try:
        Settings.model_validate(update_settings_encoded)
    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()})
        )

    query = select(apps).where(apps.c.uuid == uuid_pkg.UUID(uuid))
    result = await session.execute(query)
    result = result.first()

    db_json = result[6]
    db_json['configuration']['settings'] = update_settings_encoded

    update_stmt = update(apps).where(apps.c.uuid == uuid_pkg.UUID(uuid)).values(json=db_json)
    await session.execute(update_stmt)
    await session.commit()

    return Kind_model(kind=result[1],
                      name=result[2],
                      version=result[3],
                      configuration=db_json["configuration"],
                      description=result[4])


@router.put("/{uuid}/state", response_model=State)
async def update_kind_state(uuid: str, state: State, session: AsyncSession = Depends(get_async_session)):

    update_stmt = update(apps).where(apps.c.uuid == uuid_pkg.UUID(uuid)).values(state=state)
    await session.execute(update_stmt)
    await session.commit()

    return state


@router.delete("/{uuid}")
async def delete_kind(uuid: str, session: AsyncSession = Depends(get_async_session)) -> None:

    stmt = delete(apps).where(apps.c.uuid == uuid_pkg.UUID(uuid))
    await session.execute(stmt)
    await session.commit()

    return None


@router.get("/{uuid}", response_model=Kind_model)
async def get_kind(uuid: str, session: AsyncSession = Depends(get_async_session)):

    query = select(apps).where(apps.c.uuid == uuid_pkg.UUID(uuid))
    result = await session.execute(query)
    result = result.first()

    return Kind_model(kind=result[1],
                      name=result[2],
                      version=result[3],
                      configuration=result[6]["configuration"],
                      description=result[4])


@router.get("/{uuid}/state", response_model=State)
async def get_kind_state(uuid: str, session: AsyncSession = Depends(get_async_session)):

    query = select(apps).where(apps.c.uuid == uuid_pkg.UUID(uuid))
    result = await session.execute(query)
    result = result.first()

    state = result[5]

    return state
