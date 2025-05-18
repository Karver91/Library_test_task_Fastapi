from fastapi import APIRouter

from app.auth.routers import router as auth_router
from app.modules.book.routers import router as book_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(book_router)
