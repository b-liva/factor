from rest_framework.permissions import BasePermission


class HasPermOrIsOwner(BasePermission):
    message = "You have not enough perms..."

    def has_object_permission(self, request, view, instance, *args, **kwargs):
        # print(args)
        # print(kwargs)
        user_obj = request.user
        colleague = None
        permissions = None
        if 'colleague' in kwargs:
            colleague = kwargs['colleague']
            print(colleague)
        if permissions in kwargs:
            permissions = kwargs['permissions']
        if user_obj.is_superuser:
            return True
        if colleague is not None and colleague:
            if hasattr(instance, 'is_active'):
                return instance.is_active
            else:
                return colleague
        if instance is not None:
            print(user_obj)
            print(instance.owner)
            if user_obj == instance.owner:
                if hasattr(instance, 'is_active'):
                    return instance.is_active
                else:
                    return True
            if hasattr(instance, 'customer'):
                if user_obj == instance.customer.user:
                    return True
            elif hasattr(instance, 'req_id') and hasattr(instance.req_id, 'customer'):
                if user_obj == instance.req_id.customer.user:
                    return True
            elif hasattr(instance, 'xpref_id') and hasattr(instance.xpref_id.req_id, 'customer'):
                if user_obj == instance.xpref_id.req_id.customer.user:
                    return True
            if instance.__class__.__name__ == 'User':
                return user_obj == instance
        return user_obj.has_perm(permissions)
