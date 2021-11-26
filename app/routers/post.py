from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)


#@router.get("/", response_model=List[schemas.Post])                 # Check this, it does not have the Authentication lock
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
# -- This is the database code
#    cursor.execute("""SELECT * FROM posts """)         -- So we are now commenting out the raw SQL part too!
#    posts = cursor.fetchall()
#    print(posts)

#    posts = db.query(models.Post).all()                    # Commented when we introduced limit

#    posts = db.query(models.Post).limit(limit).all()        # This will limit the number of posts returned to limit

#    posts = db.query(models.Post).limit(limit).offset(skip).all()        # So postgres returns a set of results. In which order? we do not know
                                                                        # SQLAlchemy decides to skip first "skip" records

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # ^^ Pre count, left outer join version!

    # This was a crazy exercise to find out where the extraction of User data is being done.
    # posts_q = db.query(models.Post)
    # print(posts_q) => Where is the user join here? NOT THERE! SELECT smposts.id AS smposts_id, smposts.title AS smposts_title, smposts.content AS smposts_content, smposts.published AS smposts_published, smposts.created_at AS smposts_created_at, smposts.owner_id AS smposts_owner_id FROM smposts
    # posts = posts_q.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # But this shows up owner!: {"title": "Fun in StPetersberg-Tampa Baay", ..., "owner": { "id": 30,"email": "ghosti1ly@test.com","created_at": "2021-11-20T16:34:59.201278+05:30"}}
    # Where is it coming from?!
    # In models we have defined relationship with User. In Schemas we have added an instance variable of type User.
    # But where is SQL?! Fun!
    
    # This is the additional of the Votes count to the result query.
    # Not entirely convincing excercise of changing the return model. Rather than just adding votes count, we are changing the way the results were being sent...

    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #print(results)

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)    # Another way of setting the correct status code
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
# -- This is the database code
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(new_post)
# -- Now commented as we are moving on with the ORM - sqlalchemy
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)   # This is fine, but too wordy
    # Imagine having to resolve 50 such columns for an insert..
    # Note: post, the parameter being sent in, is a Pydantic structure.
    # So we can 'unpack' it.

    new_post = models.Post(owner_id=current_user.id,  **post.dict())
    db.add(new_post)                                    # This is likely the insert action
    db.commit()                                         # This is the commit to DB
    db.refresh(new_post)                                # This is the select to get it back, or the returning clause

    return new_post
# Added the authentication step


#retrieve a single post
@router.get("/{id}", response_model=schemas.PostOut)                             # {id} is a path parameter, it is returned as a str!
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
# -- This is raw SQL way
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id ={id} not found")
# -- This is now ORM way

#    post = db.query(models.Post).filter(models.Post.id == id).first()
    # ^^ Pre count, left outer join version

    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id ={id} not found")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
# -- This is raw SQL way
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))  # Hit by the strange problem being solved by a trailing pointless comma!
    # post = cursor.fetchone()
    # conn.commit()
# -- This is now ORM way
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
# -- This is raw SQL way
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # if updated_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    # conn.commit()
# -- This is now ORM way
    post_query = db.query(models.Post).filter(models.Post.id == id)

    selected_post = post_query.first()
    if selected_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id={id} not found")
    
    if selected_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()                                         # This is the commit to DB
    db.refresh(selected_post)

    return selected_post
