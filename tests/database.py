from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings as st
from app.database import get_db, Base
# from alembic import command, if you want to use alembic to create tables



SQLALCHEMY_DATABASE_URL = f'postgresql://{st.database_username}:{st.database_password}@{st.database_hostname}:{st.database_port}/{st.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)

#Dependancy:
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()



@pytest.fixture()
def session():
    #with alembic:
    # command.downgrade('head')
    # command.upgrade('head')

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)



'''
(scope=module) makes functions dependent from the first one. 
If we change order of functions might cause error in our code.

'''