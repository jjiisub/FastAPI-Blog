from fastapi import FastAPI

from domain.board import board_router
from domain.post import post_router

app = FastAPI()

app.include_router(board_router.router, tags=["Board"])
app.include_router(post_router.router, tags=["Post"])

@app.get("/hello")
def hello():
    return {"message": "hihi good morning"}