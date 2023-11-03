from fastapi import FastAPI

from domain.board import board_router
from domain.post import post_router
from domain.user import user_router

app = FastAPI()

app.include_router(board_router.router, tags=["Board"])
app.include_router(post_router.router, tags=["Post"])
app.include_router(user_router.router, tags=["User"])
