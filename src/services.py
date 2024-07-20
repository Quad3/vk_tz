from database import engine, Base, session
import models


def create_tables():
    return Base.metadata.create_all(bind=engine)
