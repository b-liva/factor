from django import template


def somefn():
    pass


def has_perm_or_is_owner(user_obj, permissions, instance=None):
    if instance is not None:
        if user_obj == instance.owner:
            return True
    return user_obj.has_perm(permissions)


register = template.Library()
# register.filter()


@register.filter
def hash(h, key):
    return h[key]
