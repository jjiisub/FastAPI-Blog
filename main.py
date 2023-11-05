from fastapi import FastAPI

from src.domain.board import board_router
from src.domain.post import post_router
from src.domain.user import user_router

app = FastAPI()

app.include_router(user_router.router, tags=["User"])
app.include_router(board_router.router, tags=["Board"])
app.include_router(post_router.router, tags=["Post"])
