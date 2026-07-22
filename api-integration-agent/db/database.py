from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
from sqlalchemy import MetaData
import os

load_dotenv()

# The connection URL is supplied by the environment rather than source control.
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# Create independent database sessions for individual requests.
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False
)

# Keep application tables in their own PostgreSQL schema.
metadata = MetaData(schema="agent_db_schema")

class Base(DeclarativeBase):
    # Every ORM model inherits this metadata, including the schema setting above.
    metadata = metadata
    
def get_db():
    """Provide one database session per request and always close it afterward."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
