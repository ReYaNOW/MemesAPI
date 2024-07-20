from fastapi import FastAPI

from memesapi.memes.router import router as memes_router

app = FastAPI(title='MemesAPI')

app.include_router(memes_router)
