"""Swagger related stuff shared by different application components."""

from __future__ import annotations

from fastapi import status

from src.shared import exceptions, schemas


responses = {  # pylint: disable=consider-using-namedtuple-or-dataclass
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
    status.HTTP_403_FORBIDDEN: {
        "description": "Provided tokens or credentials don't grant you enough access rights.",
        "model": schemas.NotAllowedResponse,
        "content": {
            "application/json": {
                "example": {
                    "action": "<requested action description will be here>",
                    "description": exceptions.NotAllowedException.description,
                    "details": exceptions.NotAllowedException.details,
                },
            },
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Requested resource doesn't exist.",
        "model": schemas.NotFoundResponse,
        "content": {
            "application/json": {
                "example": {
                    "resource": "<requested resource description will be here>",
                    "description": exceptions.NotFoundException.description,
                    "details": exceptions.NotFoundException.details,
                },
            },
        },
    },
    status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
        "description": "Request payload is too large.",
        "model": schemas.TooLargeResponse,
        "content": {
            "application/json": {
                "example": {
                    "resource": "<requested resource description will be here>",
                    "description": exceptions.TooLargeException.description,
                    "details": exceptions.TooLargeException.details,
                },
            },
        },
    },
}
