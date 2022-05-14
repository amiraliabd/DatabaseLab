from .schemas import UserResponseSchema, DeleteUserSchema, GetUserSchema, UpdateUserSchema, InsertUserSchema
from model.repository import UserRepo


class UserController:
    def __init__(self):
        self.repo = UserRepo()

    def insert(self, **kwargs):
        user = InsertUserSchema().load(kwargs)
        self.repo.insert(user['f_name'], user['l_name'], user['email'])

    def list(self):
        user_objs = self.repo.list()
        return UserResponseSchema(many=True).dump_from_repo(repo_user=user_objs)

    def retrieve(self, **kwargs):
        user = GetUserSchema().load(kwargs)
        user_obj = self.repo.retrieve(user['id'])
        return UserResponseSchema().dump_from_repo(user_obj)

    def delete(self, **kwargs):
        user = DeleteUserSchema().load(kwargs)
        self.repo.delete(user['id'])

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value == '':
                kwargs[key] = None
        updated_user = UpdateUserSchema().load(kwargs)
        user_id = updated_user.pop('id')
        self.repo.update(user_id, updated_user)
