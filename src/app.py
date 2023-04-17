"""Main fastapi application."""

from fastapi import FastAPI

import src.routes


app = FastAPI()

app.include_router(src.routes.router)
