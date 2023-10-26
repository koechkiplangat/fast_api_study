from fastapi import status , HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..schemas import Post, Postr
from ..database import get_db 

router = APIRouter(tags = ['POSTS'])

@router.get('/table', response_model = Postr)
def get_tableposts(db: Session = Depends(get_db)):
    posts4 = db.query(models.Post).all()
    return posts4

    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #return {"data": posts}

@router.get('/sqlalchemy')
def test_posts (db: Session = Depends(get_db)):
    postss = db.query(models.Post).all()
    return  postss

@router.post('/post',status_code= status.HTTP_201_CREATED, response_model= Postr)
def create_posts(user_post: Post, current_user : int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    #cursor.execute ("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """, 
                   #(post1.title, post1.content))
    #new_post = cursor.fetchone()

    #conn.commit()
    new_post = models.Post(owner_id = current_user.id, **user_post.model_dump()) # post1.dict() 
    db.add(new_post) 
    db.commit()
    db.refresh(new_post)

    return  new_post

 
@router.get('/posts/{id}')
def get_post(id : int, response : Response, user_id : int = Depends(oauth2.get_current_user),
              db:Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = %s """, ((str(id))))
    #posta = cursor.fetchone()
    specific_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not specific_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'{id} not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
    return specific_post


@router.delete('/delete_posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int, current_user : int = Depends(oauth2.get_current_user), db:Session =  Depends(get_db)):
    #cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING* """, (str(id)))
    #conn.commit()

    #deleted_post = cursor.fetchone()   
    post_to_delete  = db.query(models.Post).filter(models.Post.id == id).first()
 
    if post_to_delete == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail= f' Post {id} doesnt exist')
    print (type(current_user.id))
    print (type(post_to_delete.owner_id))
    if int(post_to_delete.owner_id) != int(current_user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "You are forbidden from performing the requested action")
    db.delete(post_to_delete)
    db.commit()

    return Response (status_code=status.HTTP_204_NO_CONTENT)
  


   
@router.put('/post/{id}')
def update_post(id:int, post2:Post, db:Session = Depends(get_db)):
    #cursor.execute("""UPDATE posts SET title = %s, content= %s WHERE id = %s RETURNING *""", 
                   #(post2.title, post2.content, id))

    #updated_post  = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id) #Querries the whole database

    post = post_query.first() # stores  the very first match of passed id to variable post
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'{id} not found')
    post_query.update(post2.dict(),synchronize_session = False)

    db.commit()
    
    return post_query.first