"""Main app router combining all entities routers."""

from __future__ import annotations

from fastapi import APIRouter

import src.account.routes
import src.auth.routes
import src.health.routes
import src.profile.routes


router = APIRouter()

router.include_router(src.account.routes.router)
router.include_router(src.auth.routes.router)
router.include_router(src.health.routes.router)
router.include_router(src.profile.routes.router)
