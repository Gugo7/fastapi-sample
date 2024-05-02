import pytest
from .database import client, session
from app import schemas
from app.config import settings
from jose import jwt



@pytest.mark.parametrize('username, email, password',[
    ('user1','user1@mai.com','1234'),
    ('user2','user2@mai.com','1234'),
    ('user3','user3@mai.com','1234'),
    ('user4','user4@mai.com','1234'),
])
def test_create_user(client, username, email, password):
    res = client.post('/users/', json={"username":username, "email":email, "password":password})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == email
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post('/login', data={"username":test_user['username'], "password":test_user['password']})

    #implement oauth:
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')

    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize('username, password, status_code', [
    ('user1', '12344', 403),
    ('user2', '1234', 403),
    ('user2', '11234', 403),
    (None, '1234', 422),
    ('user1', None, 422),
])
def test_incorrect_login(client, test_user, username, password, status_code):
    res = client.post('/login', data={'username':username, 'password': password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials'
