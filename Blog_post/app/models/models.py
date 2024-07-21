from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base
from ..utils import convert_title_to_url
from starlette_admin.contrib.sqla import ModelView
from starlette.requests import Request

#User Database Model
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    disabled = Column(Boolean, index=True)

# Post Database Model
class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index = True)
    title = Column(String, index = True)
    description = Column(String, index = True)
    URL = Column(String, index=True)
    tags = Column(String, index = True)
    author = Column(String, index=True)
    deleted = Column(Boolean, index = True, default=False)

class PostView(ModelView):
    exclude_fields_from_create = [Posts.URL, Posts.deleted]
    exclude_fields_from_edit = [Posts.URL]
    exclude_fields_from_detail = [Posts.author]
    async def before_create(self, request: Request, data, obj: Posts):
        obj.URL = convert_title_to_url(title=obj.title)
    async def delete(self, request: Request, pks: list):
        db = request.state.session
        id = int(pks[0])
        blog = db.query(Posts).filter(Posts.id == id).first()
        from ..operations.crud import delete_post
        delete_post(db, id, blog.author)
 
class UsersView(ModelView):
    exclude_fields_from_create = [Posts.URL, Posts.deleted]
    exclude_fields_from_edit = [Posts.URL]
    exclude_fields_from_detail = [Posts.author]
    async def before_create(self, request: Request, data, obj: Posts):
        obj.URL = convert_title_to_url(title=obj.title)
    async def delete(self, request: Request, pks: list):
        db = request.state.session
        id = int(pks[0])
        blog = db.query(Posts).filter(Posts.id == id).first()
        from ..operations.crud import delete_post
        delete_post(db, id, blog.author)