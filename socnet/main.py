from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from socnet.etc.logger import create_logs_yaml
from socnet.routes import posts_route, users_route


def app_factory():
    """
    Initializes the DB,
    Fills the DB with dummy data,
    returns FastAPI object 
    """

    app = FastAPI()

    origins = [
        "http://localhost:3000",
        "localhost:3000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    # Includes routes to the app.
    app.include_router(users_route.router)
    app.include_router(posts_route.router)

    create_logs_yaml()

    return app


app = app_factory()
