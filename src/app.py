"""Main fastapi application."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.responses import JSONResponse

import src.routes
from src.shared.exceptions import BadRequestException, NotFoundException, TooLargeException


if TYPE_CHECKING:
    from fastapi import Request


app = FastAPI(
    title="WLSS API",
    description="Backend API for Wish List Sharing Service.",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Auth-related functionality for Signing Up/In/Out.",
        },
        {
            "name": "service",
            "description": "Maintenace related functionality.",
        },
    ],
)

app.include_router(src.routes.router)


@app.exception_handler(BadRequestException)
async def handle_bad_request(_: Request, exception: BadRequestException) -> JSONResponse:
    """Handle BadRequestException."""
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "action": exception.action,
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(NotFoundException)
async def handle_not_found(_: Request, exception: NotFoundException) -> JSONResponse:
    """Handle NotFoundException."""
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "resource": exception.resource,
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(TooLargeException)
async def handle_too_large(_: Request, exception: TooLargeException) -> JSONResponse:
    """Handle TooLargeException."""
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "resource": exception.resource,
            "description": exception.description,
            "details": exception.details,
        },
    )
