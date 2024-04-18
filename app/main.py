## API dev ##

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, posts, users, votes
from .database import engine
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models

#load API to local server:
#uvicorn main:app --reload



#ORM, if we use alembic, this line code is not necesary:
#models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#Routers
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


#Methods

@app.get("/")                                   # @<decorator>.METHOD(path)
async def root():                               #function
    return {'message':'This is the root'}

