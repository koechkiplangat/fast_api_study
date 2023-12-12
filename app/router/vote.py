from fastapi import status, Depends, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from  .. import oauth2, schemas, database, models

router = APIRouter (tags=['VOTE'])

@router.post("/vote", status_code=status.HTTP_201_CREATED)
async def send_vote(vote: schemas.Vote, db : Session  = Depends(database.get_db), 
                    current_user:  int  = Depends (oauth2.get_current_user)):
     
     vote_query = db.query (models.Votes).filter (models.Votes.post_id == vote.post_id , 
                                                       models.Votes.user_id == current_user.id)
     
     found_vote = vote_query.first()
    
     if (vote.dir == 1):
          
          if found_vote:
               raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                                   detail = "Attempted action is forbiddenn!")
          
          new_vote = models.Votes(**vote.model_dump())
          #(post_id = vote.post_id, user_id = current_user.id)
          
          db.add(new_vote)
          db.commit()
    
     else:
          
          if found_vote is None:
               raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                                   detail = "Attempted action is forbidden!")
               
          vote_query.delete(synchronize_session = False)
          db.commit()
                    
     

          

        