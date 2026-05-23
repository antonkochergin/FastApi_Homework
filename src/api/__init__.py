from .auth import router as auth_router
from .category import router as category_router
from .comment import router as comment_router
from .location import router as location_router
from .post import router as post_router
from .user import router as user_router

__all__ = [
    "category_router",
    "comment_router",
    "location_router",
    "post_router",
    "user_router",
    "auth_router",
]
