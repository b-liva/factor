from django.shortcuts import redirect
from django.contrib import messages


def check_perm(perm, acl):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            request = args[0]
            obj = None
            lookup = kwargs.get(acl.lookup, None)
            if lookup:
                if not acl.model.objects.filter(pk=lookup):
                    messages.error(request, 'Nothin found')
                    return redirect('errorpage')
                obj = acl.model.objects.get(pk=lookup)
            is_allowed = acl(request.user, perm, obj=obj).allow()
            if not is_allowed:
                messages.error(request, 'عدم دسترسی کافی')
                return redirect('errorpage')

            # print('is allowd: ', is_allowed)
            #
            # print(perm, acl, acl.model)
            # print(args)
            # print(kwargs)
            return fn(*args, **kwargs)
        return wrapper
    return decorator