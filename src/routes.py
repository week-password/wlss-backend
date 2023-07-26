"""Main app router combining all entities routers."""

from __future__ import annotations

from fastapi import APIRouter

import src.auth.routes
import src.health.routes


router = APIRouter()

router.include_router(src.auth.routes.router)
router.include_router(src.health.routes.router)
