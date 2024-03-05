from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI
from fastapi.responses import JSONResponse

import src.routes
from src.shared.exceptions import (
    BadRequestException,
    NotAllowedException,
    NotAuthenticatedException,
    NotFoundException,
    TooLargeException,
)


if TYPE_CHECKING:
    from fastapi import Request


app = FastAPI(
    title="WLSS API",
    description="Backend API for Wish List Sharing Service.",
    openapi_tags=[
        {
            "name": "account",
            "description": "Account-related functionality for managing accounts.",
        },
        {
            "name": "auth",
            "description": "Auth-related functionality for Signing Up/In/Out.",
        },
        {
            "name": "file",
            "description": "File related functionality for downloading and uploading files.",
        },
        {
            "name": "friendship",
            "description": "Friendship and friendship request related functionality.",
        },
        {
            "name": "profile",
            "description": "Profile related functionality for managing profiles.",
        },
        {
            "name": "service",
            "description": "Maintenace related functionality.",
        },
        {
            "name": "wish",
            "description": "Wish and wish booking related functionality.",
        },
    ],
)

app.include_router(src.routes.router)


@app.exception_handler(BadRequestException)
async def handle_bad_request(_: Request, exception: BadRequestException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "action": exception.action,
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(NotAllowedException)
async def handle_not_allowed(_: Request, exception: NotAllowedException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "action": exception.action,
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(NotAuthenticatedException)
async def handle_not_authenticated(_: Request, exception: NotAuthenticatedException) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "description": exception.description,
            "details": exception.details,
        },
    )


@app.exception_handler(NotFoundException)
async def handle_not_found(_: Request, exception: NotFoundException) -> JSONResponse:
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
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "resource": exception.resource,
            "description": exception.description,
            "details": exception.details,
        },
    )
