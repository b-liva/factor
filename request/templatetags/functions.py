from django import template


def somefn():
    pass


def has_perm_or_is_owner(user_obj, permissions, instance=None, colleague=None):

    print(f' c is: {colleague}')
    if colleague is not None and colleague:
        print(f' c is: {colleague}')
        return colleague
    if instance is not None:
        if user_obj == instance.owner:
            return True
    return user_obj.has_perm(permissions)


register = template.Library()
# register.filter()


@register.filter
def hash(h, key):
    return h[key]
