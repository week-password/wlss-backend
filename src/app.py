"""Main fastapi application."""

from __future__ import annotations

from fastapi import FastAPI

import src.routes


app = FastAPI()

app.include_router(src.routes.router)
