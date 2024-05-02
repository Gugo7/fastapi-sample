from fastapi import APIRouter, status, HTTPException, Depends
from typing import Text, List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, func


#CONST:
#CURRENT_USER:str = Depends(oauth2.get_current_user)
#USERNAME = CURRENT_USER.username



#create a router
router = APIRouter(prefix=f'/posts',
                   tags=['Posts'],
                   responses={status.HTTP_404_NOT_FOUND: {'message': 'Not Found'}})



#Test Method ORM with sqlalchemy

#GET
@router.get('/', response_model=List[schemas.PostOut]) #past a query parameter add '?': .../post?limit=3
async def test_get_posts(db: Session = Depends(get_db),
                         current_user: int = Depends(oauth2.get_current_user),
                         limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    
    #posts = db.query(models.Post).filter(
    #    models.Post.owner_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #postgrest and sql use outer join, but sqlaclchemy use inner join. we need to use outer join:
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('likes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.owner_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


@router.get('/{id}',response_model=schemas.PostOut)
async def test_a_post(id: int, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label('likes')).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id, models.Post.owner_id == current_user.id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    
    return post



#POST
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def test_create_post(post:schemas.CreatePost,
                           db:Session = Depends(get_db),
                           current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



#DELETE
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def test_delete_post(id: int,
                           db: Session = Depends(get_db),
                           current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    post_query = post.first()

    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    
    if post_query.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action'
        )
    
    post.delete(synchronize_session=False)
    db.commit()

    return post_query



#PUT
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def test_edit_post(id: int, post:schemas.UpdatedPost,
                         db: Session = Depends(get_db),
                         current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_update = post_query.first()

    if not post_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    
    if post_update.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authorized to perform requested action'
        )
    
    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()

    return post_query.first()