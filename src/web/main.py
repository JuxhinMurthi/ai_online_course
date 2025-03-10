import uvicorn
from fastapi import FastAPI

from src.containers import ApplicationContainer
from src.web.routers.user import router as user_router
from src.web.routers.course import router as course_router
from src.web.routers.ai import router as ai_router


def create_app():
    container = ApplicationContainer()
    container.wire(packages=["src.web.routers"])
    app = FastAPI(title="AI-Powered Online Course Summary Generator")
    app.container = container

    app.include_router(user_router)
    app.include_router(course_router)
    app.include_router(ai_router)
    return app
app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
