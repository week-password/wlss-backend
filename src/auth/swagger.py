"""Swagger definitions related stuff."""

from __future__ import annotations

from fastapi import status

from src.auth import exceptions, schemas


responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Provided tokens or credentials are invalid or missing.",
        "model": schemas.NotAuthenticatedResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": exceptions.NotAuthenticatedException.description,
                    "details": exceptions.NotAuthenticatedException.details,
                },
            },
        },
    },
}
