from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import _SessionClassMethods

from.config import settings

#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:pgadmin@localhost/fastapi'

SQLALCHEMY_DATABASE_URL= settings.database_urlbase + settings.database_username + ":" + settings.database_password + "@" + settings.database_hostname + ":" + settings.database_port + "/" + settings.database_name
# A better approach could have been:
# -- SQLALCHEMY_DATABASE_URL= f"{settings.database_urlbase}{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
