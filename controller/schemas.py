from marshmallow import Schema, fields, exceptions
from marshmallow.validate import Length


class GetUserSchema(Schema):
    id = fields.Integer(required=True)


class DeleteUserSchema(GetUserSchema):
    pass


class InsertUserSchema(Schema):
    f_name = fields.String(required=True, validate=Length(2, 20))
    l_name = fields.String(required=True, validate=Length(2, 20))
    email = fields.Email(required=True, validate=Length(2, 20))


class UpdateUserSchema(GetUserSchema):
    f_name = fields.String(allow_none=True, validate=Length(2, 20))
    l_name = fields.String(allow_none=True, validate=Length(2, 20))
    email = fields.Email(allow_none=True, validate=Length(2, 20))

    def load(self, *args, **kwargs):
        values = super(UpdateUserSchema, self).load(*args, **kwargs)
        copy_values = values.copy()
        copy_values.pop('id')
        if set(copy_values.values()) == {None}:
            raise exceptions.ValidationError('You should at least change one item for update')
        return values


class UserResponseSchema(GetUserSchema):
    f_name = fields.String(required=True, validate=Length(2, 20))
    l_name = fields.String(required=True, validate=Length(2, 20))
    email = fields.Email(required=True, validate=Length(2, 20))

    def dump_from_repo(self, repo_user):
        if self.many:
            data = []
            for user in repo_user:
                data.append(dict(
                    id=user[0],
                    f_name=user[1],
                    l_name=user[2],
                    email=user[3]
                ))
        else:
            user = repo_user[0]
            data = dict(
                id=user[0],
                f_name=user[1],
                l_name=user[2],
                email=user[3]
            )

        return self.dump(data)