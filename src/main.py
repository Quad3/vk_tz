from fastapi import FastAPI

from rest.routes.something.router import router

app = FastAPI(
    title="something"
)

app.include_router(router)