from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette.middleware.sessions import SessionMiddleware
from app import database
from app.operations.homepage import UsernameAndPasswordProvider
from app.router import auth, blog, users

from .models import models


SECRET = "1234567890"
def fast_api_app():
    app = FastAPI()
    app.include_router(auth.router)
    app.include_router(blog.router)
    app.include_router(users.router)
    return app

def starlette_app():
    app = Starlette()
    admin = Admin(
        database.engine, 
        title = "BLOG", 
    auth_provider=UsernameAndPasswordProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=SECRET)]
    )
    admin.add_view(models.PostView(models.Posts))
    admin.add_view(ModelView(models.User))
    admin.mount_to(app)
    return app


