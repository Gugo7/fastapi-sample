from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from .config import settings as st
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET KEY, openssl rand -hex 32 on CMD
#ALGORITHM
#ExpirationTime

SECRET_KEY = st.secret_key
ALGORITHM = st.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = st.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    print(datetime.now(timezone.utc))

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id  = str(payload.get('user_id'))

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status.HTTP_403_FORBIDDEN,
                                          detail='Could not validate credentials',
                                          headers={'WWW-Authenticate': 'Bearer'})
    verified_token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == verified_token.id).first()

    return user