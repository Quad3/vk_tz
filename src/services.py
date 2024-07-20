from database import engine, Base, session
import models


def create_tables():
    return Base.metadata.create_all(bind=engine)


def get_router_names() -> list[str]:
    filename = "router_names.txt"

    with open(filename, 'r') as f:
        router_names = f.read().splitlines()

    return router_names
