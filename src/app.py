"""Main fastapi application."""

from __future__ import annotations

from fastapi import FastAPI

import src.routes


app = FastAPI(
    title="WLSS API",
    description="Backend API for Wish List Sharing Service.",
    openapi_tags=[
        {
            "name": "service",
            "description": "Maintenace related functionality.",
        },
    ],
)

app.include_router(src.routes.router)
