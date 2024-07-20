import importlib
from fastapi import FastAPI

from services import get_router_names


app = FastAPI(
    title="JSON parser"
)


routers: list[str] = get_router_names()

for router in routers:
    globals()[router] = importlib.import_module(f"rest.routes.{router}.router")
    app.include_router(globals()[router].router)
