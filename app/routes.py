from fastapi import APIRouter

from app.auth.routers import router as auth_router
from app.modules.book.routers import router as book_router
from app.modules.reader.routers import router as reader_router
from app.modules.borrowing.routers import router as borrowing_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(book_router)
router.include_router(reader_router)
router.include_router(borrowing_router)
