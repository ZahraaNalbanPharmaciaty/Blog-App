from app.models.models import Posts, User
from ..utils import convert_title_to_url
from starlette_admin.contrib.sqla import ModelView
from starlette.requests import Request
from ..operations.crud import delete_post, delete_user

class PostView(ModelView):
    exclude_fields_from_create = [Posts.URL, Posts.deleted, Posts.author]
    exclude_fields_from_edit = [Posts.URL]
    exclude_fields_from_detail = [Posts.author]
    async def before_create(self, request: Request, data, obj: Posts):
        users = request.state.user
        obj.URL = convert_title_to_url(title=obj.title)
        obj.author = users.username

    async def delete(self, request: Request, pks: list):
        db = request.state.session
        user = request.state.user
        id = int(pks[0])
        delete_post(db, id, user.username)

    def can_edit(self, request: Request):
        return False
    

class UsersView(ModelView):
    exclude_fields_from_create = [User.disabled]
    exclude_fields_from_list = exclude_fields_from_detail = [User.password, User.id]
    exclude_fields_from_edit = [User.disabled, User.password]
    async def before_create(self, request: Request, data, obj: User):
        obj.disabled = False
    async def delete(self, request: Request, pks: list):
        db = request.state.session
        user = request.state.user
        id = int(pks[0])
        delete_user(db, id, user.username)
    
    # def can_delete(self, request: Request):
    #     return False
    # def can_edit(self, request: Request):
    #     return False