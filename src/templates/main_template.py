from fastapi import FastAPI

from rest.routes.{{ kind }}.router import router

app = FastAPI(
    title="{{ kind }}"
)

app.include_router(router)
