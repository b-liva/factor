from django import template


def somefn():
    pass


def has_perm_or_is_owner(user_obj, permissions, instance=None, colleague=None):
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


register = template.Library()
# register.filter()


@register.filter
def hash(h, key):
    return h[key]
