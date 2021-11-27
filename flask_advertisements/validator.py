import jsonschema
from flask import request
from models import User

import errors


def validate(source: str, req_schema: dict):
    """Валидатор входящих запросов"""

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                jsonschema.validate(
                    instance=getattr(request, source), schema=req_schema,
                )
            except jsonschema.ValidationError as e:
                raise errors.BadLuck

            result = func(*args, **kwargs)

            return result
        return wrapper
    return decorator


def validate_auth(request_post, advertisement):
    if request_post.headers.get('username') and request_post.headers.get('password'):
        user = User.query.filter_by(username=request_post.headers['username']).first()
        if user:
            if user.check_password(request_post.headers['password']):
                if request_post.method == 'POST':
                    advertisement.user_id = user.id
                elif request_post.method in ['DELETE', 'PUT']:
                    if user.id != advertisement.user_id:
                        raise errors.AuthError
            else:
                raise errors.AuthError
        else:
            raise errors.AuthError
    else:
        raise errors.AuthError
