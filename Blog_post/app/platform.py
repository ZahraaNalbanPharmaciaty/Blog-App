from fastapi import FastAPI
from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

from app import database
from app.router import auth, blog, users

from .models import models



def fast_api_app():
    app = FastAPI()
    app.include_router(auth.router)
    app.include_router(blog.router)
    app.include_router(users.router)
    return app

def starlette_app():
    app = Starlette()
    admin = Admin(database.engine, title = "BLOG")
    admin.add_view(models.PostView(models.Posts))
    admin.add_view(ModelView(models.User))
    admin.mount_to(app)
    return app


