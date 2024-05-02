from fastapi.testclient import TestClient
from app.main import app
from app import schemas, models
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings as st
from app.database import get_db, Base
from app.oauth2 import create_access_token
# from alembic import command, if you want to use alembic to create tables

'''
(scope=module) makes functions dependent from the first one. 
If we change order of functions might cause error in our code.

'''


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



@pytest.fixture
def test_user(client):
    user_data = {"username":'user1', "email":'user1@mail.com', "password":'1234'}
    res = client.post('/users/', json=user_data)
    
    assert res.status_code == 201
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"username":'user2', "email":'user2@mail.com', "password":'1234'}
    res = client.post('/users/', json=user_data)
    
    assert res.status_code == 201
    
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})



@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f"Bearer {token}" 
    }
    
    return client



@pytest.fixture
def test_post(test_user, session, test_user2):
    posts_data = [
        {
        'title':'1st title',
        'content':'1st content',
        'owner_id': test_user['id']
        },
        {
        'title':'2nd title',
        'content':'2nd content',
        'owner_id': test_user['id']
        },
        {
        'title':'3rd title',
        'content':'3rd content',
        'owner_id': test_user['id']
        },
         {
        'title':'4th title',
        'content':'4th content',
        'owner_id': test_user2['id']
        },
    ]

    # session.add_all([models.Post(title='1st title', content='1st content', owner_id=test_user['id'])])
    
    def create_post_model(post):
        return models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts_list = list(posts_map)

    session.add_all(posts_list)
    session.commit()

    posts = session.query(models.Post).all()
    return posts