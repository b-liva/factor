from enum import Enum
from typing import Iterable, Union
from functools import wraps
from graphql_relay import from_global_id
from graphql_jwt.decorators import context
from graphql_jwt import exceptions


def permission_required(perm: Union[Enum, Iterable[Enum]]):
    def decorator(func):
        @wraps(func)
        @context(func)
        def wrapper(context, *args, **kwargs):
            is_owner_perm = is_colleague_perm = False
            obj = None
            if len(args) > 0:
                cls = args[0]
                new_args = args[1:]
                if 'input' in kwargs and hasattr(cls, 'get_form_kwargs'):
                    form = cls.get_form_kwargs(*new_args, **kwargs['input'])
                    if 'instance' in form:
                        obj = form['instance']
                elif hasattr(cls._meta, 'model'):
                    obj = cls._meta.model._default_manager.get(pk=args[2])
                else:
                    obj = kwargs['input'].model._default_manager.get(
                        pk=from_global_id(kwargs['input'].id)[1]
                    )

                if obj is not None:
                    is_owner_perm = is_owner(context.user, obj)
                    is_colleague_perm = is_colleague(context.user, obj)
                else:
                    is_owner_perm = True

            if check_perms(context) and (is_owner_perm or is_colleague_perm) or context.user.is_superuser:
                return func(*args, **kwargs)
            raise exceptions.PermissionDenied()

        return wrapper

    def check_perms(context):
        perms = perm
        perms_list = [
            p.value for p in perms
        ]
        if context.user.has_perms(perms_list):
            return True
        return False

    def is_owner(user, obj):
        if obj.owner == user:
            return True
        return False

    def is_colleague(user, obj):
        if hasattr(obj, 'colleagues'):
            return user in obj.colleagues.all()
        return False

    return decorator

