from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # We need to update the table Votes
    user_id = current_user.id                                       # This is the user id

    # if no earlier vote present and upvote (1): insert
    # if no earlier vote present and downvote (0): reject as an exception - No such vote exists
    # if earlier vote is present and upvote (1): reject as exception
    # if earlier vote is present and downvote (0): delete

    # check if a record for this user and this post is present
    existing_vote_query = db.query(models.Votes).filter(models.Votes.user_id == user_id, models.Votes.post_id == vote.post_id)

    existing_vote = existing_vote_query.first()

    if not existing_vote:
        # There is no row
        if vote.dir == 1:                   # Upvote
            # Check of the post exists
            current_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
            if not current_post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such Post")

            new_vote = models.Votes(user_id = current_user.id, post_id = vote.post_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return Response(status_code=status.HTTP_201_CREATED)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such vote exists")
    else:
        # There is a vote already
        if vote.dir == 1:                   # Upvote
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Already Voted")
        else:
            existing_vote_query.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)