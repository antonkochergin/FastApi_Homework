from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import (
    auth_router,
    category_router,
    comment_router,
    location_router,
    post_router,
    user_router,
)
from core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(root_path=settings.ROOT_PATH)

    # настройки (* - разрешает всё)
    app.add_middleware(
        # для логирования можно добавить свой мидлваре
        CORSMiddleware,  # type: ignore
        allow_origins=settings.origins_list,  # с каких айпи разрешен запрос
        allow_credentials=True,  # разрешение на использование токенов
        allow_methods=["*"],  # какие методы разрешены
        allow_headers=["*"],  # фильтр хэдеров
    )

    # подключаем роутеры
    app.include_router(router=auth_router, tags=["Auth"])
    app.include_router(router=user_router, tags=["Users"])
    app.include_router(router=post_router, tags=["Posts"])
    app.include_router(router=category_router, tags=["Categories"])
    app.include_router(router=location_router, tags=["Locations"])
    app.include_router(router=comment_router, tags=["Comments"])

    return app
