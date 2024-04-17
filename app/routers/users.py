from fastapi import APIRouter, status, HTTPException, Depends
from typing import Text, List
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import delete, update



#create a router
router = APIRouter(prefix='/users',
                   tags=['Users'],
                   responses={status.HTTP_404_NOT_FOUND: {'message': 'Not Found'}})



#Test Method ORM with sqlalchemy
@router.get('/', response_model=List[schemas.UserOut])
async def test_get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}',response_model=schemas.UserOut)
async def test_a_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    
    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def test_create_user(user:schemas.CreateUser, db: Session = Depends(get_db)):
    user_username = db.query(models.User).filter(models.User.username == user.username)
    user_email = db.query(models.User).filter(models.User.email == user.email)

    if user_username.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username already exist'
        )
    
    if user_email.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='email already used'
        )
        

    #hash the password from user.password:
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def test_delete_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)

    user_query = user.first()
    if not user_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    
    user.delete(synchronize_session=False)
    db.commit()

    return user_query


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User)
async def test_edit_user(id:int, user:schemas.EditUser, db: Session = Depends(get_db)):
    new_user = db.query(models.User).filter(models.User.id == id)

    if not new_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    
    new_user.update(user.model_dump(),
                    synchronize_session=False)
    db.commit()

    return new_user.first()