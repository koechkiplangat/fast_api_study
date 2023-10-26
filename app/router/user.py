from fastapi import status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session


from .. import utils, models, oauth2
from ..schemas import UserResponse,  UserDetail
from ..database import get_db


router = APIRouter(prefix= '/user', tags=['USERS']) # You can use prefix here i.e router = APIRouter(prefix = "/users") also tags to improve on documentation
   
@router.post('/sign_up', status_code=status.HTTP_201_CREATED, response_model= UserResponse)
def create_users(user: UserDetail, db:Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 

@router.get('/registered_user/{id}', response_model=UserResponse)
def get_users(id:int, user_id : int = Depends(oauth2.get_current_user), db:Session = Depends (get_db)):

    specific_user = db.query(models.Users).filter(models.Users.id == id).first()
    
    if not specific_user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User NOT found")
    return specific_user

