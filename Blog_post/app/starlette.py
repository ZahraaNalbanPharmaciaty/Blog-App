"""
********************************************************************

BLOG APPLICATION USING FASTAPI
Author: Zahraa Nalban

********************************************************************
"""


from starlette.middleware import Middleware
from app.operations import homepage
from app.operations.crud import create_posts, create_user, delete_post, update_post
from app.router.auth import login_for_access
from app.router.blog import retrieve_post_by_tag, retrieve_posts
from app.router.users import read_users_me, retrieve_post_by_author
from starlette.routing import Route
from app.platform import starlette_app
from starlette.middleware.authentication import AuthenticationMiddleware

route = [
    Route("/api/users/token", endpoint = login_for_access, methods = ["POST"]),
    Route("/api/users/me/", endpoint = read_users_me, methods = ["GET"]),
    Route("/api/users/me/", endpoint = read_users_me, methods = ["GET"]),
    Route("/api/posts", endpoint = retrieve_posts, methods = ["GET"]),
    Route("/api/posts", endpoint = create_posts, methods = ["POST"]),
    Route("/api/users/posts", endpoint = retrieve_post_by_author, methods = ["GET"]),
    Route("/api/posts/{tag}", endpoint = retrieve_post_by_tag, methods = ["GET"]),
    Route("/api/posts/{id}", endpoint = delete_post, methods = ["DELETE"]),
    Route("/api/posts/{id}", endpoint = update_post, methods = ["PUT"]),
    Route("/api/users/create", endpoint = create_user, methods = ["POST"]),
]

app = starlette_app()
