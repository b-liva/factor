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
        if user_obj == instance.owner:
            if hasattr(instance, 'is_active'):
                return instance.is_active
            else:
                return True
        if hasattr(instance, 'customer') and not hasattr(instance, 'xpref_id'):
            if user_obj == instance.customer.user:
                return True
        elif hasattr(instance, 'req_id') and hasattr(instance.req_id, 'customer'):
            print('03')
            if user_obj == instance.req_id.customer.user \
                    or user_obj == instance.req_id.owner \
                    or user_obj in instance.req_id.colleagues.all():
                return True
        elif hasattr(instance, 'xpref_id') and hasattr(instance.xpref_id.req_id, 'customer'):
            print('04')
            if user_obj == instance.xpref_id.req_id.customer.user \
                    or user_obj in instance.xpref_id.req_id.colleagues.all() \
                    or user_obj == instance.xpref_id.req_id.owner:
                return True
        if instance.__class__.__name__ == 'User':
            return user_obj == instance
        if instance.__class__.__name__ == 'Payment':
            print("payment model")
    return user_obj.has_perm(permissions)


register = template.Library()
# register.filter()


@register.filter
def hash(h, key):
    return h[key]
