from django import template


def has_perm_or_is_owner(user_obj, permissions, instance=None, colleague=None):
    if user_obj.is_superuser:
        return True
    if colleague is not None and colleague:
        if hasattr(instance, 'is_active'):
            return instance.is_active
        else:
            return colleague
    if instance is not None:
        # print('*&*&*&*&: ', instance.owner.username, user_obj.username)
        if user_obj == instance.owner:
            if hasattr(instance, 'is_active'):
                return instance.is_active and user_obj.has_perm(permissions)
            else:
                return user_obj.has_perm(permissions)
        if hasattr(instance, 'customer') and not hasattr(instance, 'xpref_id'):
            if user_obj == instance.customer.user or user_obj in instance.colleagues.all():
                return True
            else:
                return False
        elif hasattr(instance, 'req_id') and hasattr(instance.req_id, 'customer'):
            if user_obj == instance.req_id.customer.user \
                    or user_obj == instance.req_id.owner \
                    or user_obj in instance.req_id.colleagues.all():
                return True
            else:
                return False
        elif hasattr(instance, 'xpref_id') and hasattr(instance.xpref_id.req_id, 'customer'):
            if user_obj == instance.xpref_id.req_id.customer.user \
                    or user_obj in instance.xpref_id.req_id.colleagues.all() \
                    or user_obj == instance.xpref_id.req_id.owner:
                return True
        if instance.__class__.__name__ == 'User':
            return user_obj == instance
        if instance.__class__.__name__ == 'Payment':
            return user_obj == instance.owner
    return user_obj.has_perm(permissions)


register = template.Library()
# register.filter()


@register.filter
def hash(h, key):
    return h[key]
