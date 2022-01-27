from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import os

try:
    postgres_user = 'postgres'
    postgres_password = 'postgres'
    if 'POSTGRES_USER' in os.environ:
        postgres_user = os.environ['POSTGRES_USER']
        logging.info("Postgres username found in environ")
    if 'POSTGRES_PASSWORD' in os.environ:
        postgres_password = os.environ['POSTGRES_PASSWORD']
    SQLALCHEMY_DATABASE_URL =  f"postgresql+psycopg2://{postgres_user}:{postgres_password}@postgres:5432/trinibytes_db"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()
except Exception as exc:
    logging.error("Error",exc_info=exc)