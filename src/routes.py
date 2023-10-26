"""Main app router combining all entities routers."""

from __future__ import annotations

from fastapi import APIRouter

import src.account.routes
import src.auth.routes
import src.friendship.routes
import src.health.routes
import src.profile.routes
from src.session import session


router = APIRouter()

router.include_router(src.account.routes.router)
router.include_router(src.auth.routes.router)
router.include_router(src.friendship.routes.router)
router.include_router(src.health.routes.router)
router.include_router(src.profile.routes.router)


@session("some-session")
def route(session=None):
    """This function is a router/repository/whatever callable which uses session provided by `session` decorator."""
    return session
