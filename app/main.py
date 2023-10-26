from fastapi import FastAPI
import psycopg2
import time
from . database import engine
from . import models
from .router import post, user, auth, vote


models.Base.metadata.create_all(bind = engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres')
        cursor = conn.cursor()
        print('Database connection succesful')
        break
    except Exception as errorr:
        print(errorr)
        time.sleep(5)


my_posts  = [{'tittle': 'Best Football teams',  'content':'Arsenal', 'id' : 10,
                'tittle': 'Best Football teams',  'content':'Arsenal.2', 'id' : 30}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index(id):
     for i, p in enumerate(my_posts):
        if  p['id'] == id:
            return i
        


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#path operation
@app.get('/') #Decorator passing specific http method
async def root(): #Function
    return {'message': 'effort'} 












