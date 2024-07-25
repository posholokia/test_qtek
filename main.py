from src.api.router import router
from src.config import settings
from src.core.constructor.exceptions import BaseHttpException

from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import JSONResponse


def create_app() -> FastAPI:
    app = FastAPI(
        title="Айтек тестовое задание",
        docs_url="/api/docs",
        description="Test",
        debug=settings.DEBUG,
    )

    @app.exception_handler(BaseHttpException)
    async def custom_http_exception_handler(
        request: Request, exc: BaseHttpException
    ):
        """
        Переопределен хэндлер, чтобы кастомные
        эксепшены выводились в ответ сервера
        """
        return JSONResponse(
            status_code=exc.code,
            content={"detail": exc.message},
        )

    app.include_router(router)
    return app
