from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from config.configuration import (
    DATABASE_NAME,
    DATABASE_USERNAME,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT
)

def get_uri():
    return f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

Base = declarative_base()

postgresql_uri = get_uri()
engine = create_engine(postgresql_uri)
SessionLocal = sessionmaker(bind=engine)