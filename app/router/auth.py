from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..database import get_db
from app.oauth2 import create_access_token
#from ..schemas import UserLogin
from .. import models, utils

router = APIRouter(tags= ['AUTHENTICATION'])

@router.post('/login')
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid credentials entered")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid credentials entered")
    
    acess_token = create_access_token(data = {'user_id': user.id} )

    return {'acess_token': acess_token , 'token_type':'Bearer'}


    
    

    
