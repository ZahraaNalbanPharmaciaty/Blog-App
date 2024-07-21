"""
********************************************************************

BLOG APPLICATION USING FASTAPI
Author: Zahraa Nalban

********************************************************************
"""

from database import init_db
from .platform import fast_api_app, starlette_app

app = fast_api_app()

#On application startup
@app.on_event("startup")
def application_startup():
    # Attempt database initialisation on application startup
    init_db()

