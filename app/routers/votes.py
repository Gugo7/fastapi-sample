from fastapi import APIRouter, status, HTTPException, Depends
from typing import Text, List, Optional
from .. import models, schemas, oauth2, database
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import delete, update



#create a router
router = APIRouter(prefix=f'/vote',
                   tags=['Vote'],
                   responses={status.HTTP_404_NOT_FOUND: {'message': 'Not Found'}})




@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
               current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                            models.Vote.user_id == current_user.id)
    
    found_vote = vote_query.first()

    if (vote.dir == True):
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User {current_user.id} has already like the post with id: {vote.post_id}'
            )
        
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {'message':'Successfully liked a post'}
    
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Like does not exist'
            )
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message':'Successfylly deleted like'}