from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .config import settings
from .database import engine
from .routers import auth, post, user, vote

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# These are called path operations
@app.get("/")
async def root():
    return {"message": "App deployed successfully on Ubuntu Server using CI/CD"}
