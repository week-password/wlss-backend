"""Main app router combining all entities routers."""

from fastapi import APIRouter

import src.entity.routes
import src.health.routes


router = APIRouter()

router.include_router(src.entity.routes.router)
router.include_router(src.health.routes.router)
