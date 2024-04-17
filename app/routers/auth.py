from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2



router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    #filter user by email and username:
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    
    #verify is credentials are correct:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )
    
    #verify password given by login
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid Credentials'
        )
    
    #create token
    access_token = oauth2.create_access_token(data={'user_id': user.id})


    #return token, check access token on jwt.io 
    return {'access_token': access_token, 'token_type': 'bearer'}